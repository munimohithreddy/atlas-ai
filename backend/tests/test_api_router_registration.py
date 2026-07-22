import unittest

from bootstrap import configure_test_environment

configure_test_environment()

from app.api.v1.router import api_router  # noqa: E402


class ApiRouterRegistrationTests(unittest.TestCase):
    def test_api_router_registers_health_and_opportunity_routes(self) -> None:
        paths = set()
        for route in api_router.routes:
            original_router = getattr(route, "original_router", None)
            if original_router is not None:
                paths.update(child_route.path for child_route in original_router.routes)
            elif hasattr(route, "path"):
                paths.add(route.path)

        self.assertIn("/health", paths)
        self.assertIn("/asset-production-queue", paths)
        self.assertIn("/affiliate-programs", paths)
        self.assertIn("/affiliate-programs/{program_id}", paths)
        self.assertIn("/campaigns", paths)
        self.assertIn("/campaigns/{campaign_id}", paths)
        self.assertIn("/campaigns/{campaign_id}/tasks", paths)
        self.assertIn("/campaigns/{campaign_id}/assets", paths)
        self.assertIn("/asset-production-queue", paths)
        self.assertIn("/campaigns/{campaign_id}/approve", paths)
        self.assertIn("/campaigns/{campaign_id}/repair-readiness", paths)
        self.assertIn("/campaigns/{campaign_id}/status", paths)
        self.assertIn("/brands", paths)
        self.assertIn("/brands/{brand_id}", paths)
        self.assertIn("/business-plans", paths)
        self.assertIn("/business-plans/{business_plan_id}", paths)
        self.assertIn("/opportunities", paths)
        self.assertIn("/opportunities/{opportunity_id}/business-plan", paths)
        self.assertIn("/opportunities/evaluate", paths)
        self.assertIn("/opportunities/evaluate-with-evidence", paths)
        self.assertIn("/opportunities/portfolio", paths)
        self.assertIn("/research/preview", paths)


if __name__ == "__main__":
    unittest.main()
