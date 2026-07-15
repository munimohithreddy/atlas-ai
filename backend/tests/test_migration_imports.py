import subprocess
import sys
import unittest
from pathlib import Path

from bootstrap import configure_test_environment

configure_test_environment()


class MigrationImportTests(unittest.TestCase):
    def test_migrations_import_from_repository_root(self) -> None:
        root = Path(__file__).resolve().parents[2]
        result = subprocess.run(
            [
                str(root / ".venv" / "Scripts" / "alembic.exe"),
                "-c",
                str(root / "backend" / "alembic.ini"),
                "heads",
            ],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)

    def test_migrations_import_from_backend_directory(self) -> None:
        backend_dir = Path(__file__).resolve().parents[1]
        result = subprocess.run(
            [
                str(backend_dir.parent / ".venv" / "Scripts" / "alembic.exe"),
                "heads",
            ],
            cwd=backend_dir,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)


if __name__ == "__main__":
    unittest.main()
