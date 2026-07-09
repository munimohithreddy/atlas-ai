import unittest

from bootstrap import configure_test_environment

configure_test_environment()

from app.api.v1.affiliate_programs import create, list_all  # noqa: E402
from app.schemas.affiliate_program import AffiliateProgramCreate  # noqa: E402


class FakeAffiliateQuery:
    def __init__(self, items) -> None:
        self.items = items

    def order_by(self, *args, **kwargs):
        return self

    def all(self):
        return list(self.items)


class FakeAffiliateSession:
    def __init__(self) -> None:
        self.items = []
        self.next_id = 1
        self.commits = 0

    def add(self, item) -> None:
        self.items.append(item)

    def commit(self) -> None:
        self.commits += 1

    def refresh(self, item) -> None:
        if getattr(item, "id", None) is None:
            item.id = self.next_id
            self.next_id += 1

    def query(self, model):
        return FakeAffiliateQuery(self.items)


def build_affiliate_payload() -> AffiliateProgramCreate:
    return AffiliateProgramCreate(
        name="Coffee Gear Partner",
        network="Impact",
        category="coffee",
        website_url="https://example.com/coffee",
        commission_type="percent",
        commission_rate=12.5,
        cookie_duration_days=30,
        approval_required=True,
        notes="espresso machines and coffee gear",
    )


class AffiliateProgramTests(unittest.TestCase):
    def test_affiliate_program_creation(self) -> None:
        db = FakeAffiliateSession()

        program = create(payload=build_affiliate_payload(), db=db)

        self.assertEqual(program.id, 1)
        self.assertEqual(program.name, "Coffee Gear Partner")
        self.assertEqual(program.category, "coffee")
        self.assertEqual(db.commits, 1)

    def test_affiliate_program_listing(self) -> None:
        db = FakeAffiliateSession()
        create(payload=build_affiliate_payload(), db=db)

        programs = list_all(db=db)

        self.assertEqual(len(programs), 1)
        self.assertEqual(programs[0].network, "Impact")


if __name__ == "__main__":
    unittest.main()
