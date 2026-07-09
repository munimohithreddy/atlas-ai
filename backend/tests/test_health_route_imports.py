import unittest

from bootstrap import configure_test_environment

configure_test_environment()

from app.api.v1 import health  # noqa: E402


class HealthRouteImportTests(unittest.TestCase):
    def test_health_router_imports_and_registers_health_path(self) -> None:
        paths = {route.path for route in health.router.routes}

        self.assertIn("/health", paths)
        self.assertTrue(callable(health.health))


if __name__ == "__main__":
    unittest.main()
