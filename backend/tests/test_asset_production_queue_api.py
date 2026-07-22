import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from bootstrap import configure_test_environment

configure_test_environment()

from app.main import app  # noqa: E402


class AssetProductionQueueApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_global_asset_production_queue_returns_200(self) -> None:
        with patch("app.api.v1.router.list_asset_queue", return_value=[]):
            response = self.client.get("/api/v1/asset-production-queue")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_global_asset_production_queue_forwards_filters(self) -> None:
        with patch("app.api.v1.router.list_asset_queue", return_value=[]) as mocked:
            response = self.client.get(
                "/api/v1/asset-production-queue",
                params={
                    "campaign_id": 7,
                    "status": "queued",
                    "channel": "website",
                    "asset_type": "homepage",
                    "assigned_to": "sam",
                    "priority": "high",
                },
            )

        self.assertEqual(response.status_code, 200)
        mocked.assert_called_once()
        _, kwargs = mocked.call_args
        self.assertEqual(kwargs["campaign_id"], 7)
        self.assertEqual(kwargs["status"], "queued")
        self.assertEqual(kwargs["channel"], "website")
        self.assertEqual(kwargs["asset_type"], "homepage")
        self.assertEqual(kwargs["assigned_to"], "sam")
        self.assertEqual(kwargs["priority"], "high")


if __name__ == "__main__":
    unittest.main()
