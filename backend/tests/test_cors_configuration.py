import unittest

from starlette.middleware.cors import CORSMiddleware

from bootstrap import configure_test_environment

configure_test_environment()

from app.main import app  # noqa: E402


class CorsConfigurationTests(unittest.TestCase):
    def test_local_frontend_origin_is_allowed(self) -> None:
        cors_middleware = next(
            (
                middleware
                for middleware in app.user_middleware
                if middleware.cls is CORSMiddleware
            ),
            None,
        )

        self.assertIsNotNone(cors_middleware)
        self.assertEqual(
            cors_middleware.kwargs["allow_origins"],
            ["http://localhost:3000"],
        )


if __name__ == "__main__":
    unittest.main()
