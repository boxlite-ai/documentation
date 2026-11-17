"""Keep approved subscription statuses scoped to their exact page and rows."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("lint_docs", Path(__file__).with_name("lint-docs.py"))
lint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lint)


class SubscriptionStatusTests(unittest.TestCase):
    def test_only_exact_status_rows_on_plans_page_are_allowed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "cloud").mkdir()
            for relative, text, allowed in [
                ("cloud/plans.mdx", "\n".join(lint.SUBSCRIPTION_STATUS_LINES), True),
                ("cloud/other.mdx", "\n".join(lint.SUBSCRIPTION_STATUS_LINES), False),
                ("cloud/plans.mdx", "| New feature | — | — | Coming soon |", False),
                ("cloud/plans.mdx", "Enterprise SSO is coming soon", False),
            ]:
                with self.subTest(relative=relative, text=text):
                    path = root / relative
                    path.write_text(text)
                    self.assertEqual(not lint.check(path), allowed)


if __name__ == "__main__":
    unittest.main()
