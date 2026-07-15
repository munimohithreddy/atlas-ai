import unittest

from bootstrap import configure_test_environment

configure_test_environment()

from app.api.v1.brands import create, get_by_id, list_all  # noqa: E402
from app.schemas.brand import BrandCreate  # noqa: E402


class FakeBrandQuery:
    def __init__(self, items):
        self.items = items
        self.slug = None
        self.brand_id = None

    def filter(self, condition):
        column_name = getattr(condition.left, "name", None)
        value = getattr(condition.right, "value", None)
        if column_name == "slug":
            self.slug = value
        elif column_name == "id":
            self.brand_id = value
        return self

    def first(self):
        if self.brand_id is not None:
            for item in self.items:
                if item.id == self.brand_id:
                    return item
            return None
        if self.slug is None:
            return self.items[0] if self.items else None
        for item in self.items:
            if item.slug == self.slug:
                return item
        return None

    def order_by(self, *args, **kwargs):
        return self

    def all(self):
        return list(self.items)


class FakeBrandSession:
    def __init__(self) -> None:
        self.items = []
        self.next_id = 1

    def add(self, item) -> None:
        self.items.append(item)

    def commit(self) -> None:
        pass

    def refresh(self, item) -> None:
        if getattr(item, "id", None) is None:
            item.id = self.next_id
            self.next_id += 1

    def query(self, model):
        return FakeBrandQuery(self.items)


class BrandTests(unittest.TestCase):
    def test_brand_creation(self) -> None:
        db = FakeBrandSession()
        brand = create(
            payload=BrandCreate(name="WorkspaceHQ", slug="workspacehq", market="office"),
            db=db,
        )
        self.assertEqual(brand.id, 1)
        self.assertEqual(brand.slug, "workspacehq")

    def test_duplicate_brand_slug_rejected(self) -> None:
        db = FakeBrandSession()
        create(payload=BrandCreate(name="WorkspaceHQ", slug="workspacehq", market="office"), db=db)

        with self.assertRaises(Exception):
            create(payload=BrandCreate(name="Other", slug="workspacehq", market="office"), db=db)

    def test_brand_listing_and_lookup(self) -> None:
        db = FakeBrandSession()
        created = create(
            payload=BrandCreate(name="WorkspaceHQ", slug="workspacehq", market="office"),
            db=db,
        )
        self.assertEqual(list_all(db=db)[0].id, created.id)
        self.assertEqual(get_by_id(brand_id=created.id, db=db).id, created.id)


if __name__ == "__main__":
    unittest.main()
