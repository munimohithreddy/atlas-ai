import unittest

from bootstrap import configure_test_environment

configure_test_environment()

from app.api.v1.router import api_router  # noqa: E402


class ApiRouterRegistrationTests(unittest.TestCase):
    def test_api_router_registers_health_and_opportunity_routes(self) -> None:
        paths = {
            route.path
            for included_router in api_router.routes
            for route in included_router.original_router.routes
        }

        self.assertIn("/health", paths)
        self.assertIn("/opportunities", paths)


if __name__ == "__main__":
    unittest.main()
