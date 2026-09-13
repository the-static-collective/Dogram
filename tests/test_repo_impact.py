import tempfile
import unittest
from pathlib import Path

from dogram.repo_impact import build_repo_impact, extract_python_dependency_graph, render_impact_markdown


class RepoImpactTests(unittest.TestCase):
    def test_extracts_local_python_import_edges_and_compares_two_trees(self):
        with tempfile.TemporaryDirectory() as left_dir, tempfile.TemporaryDirectory() as right_dir:
            left = Path(left_dir)
            right = Path(right_dir)
            for root in (left, right):
                (root / "pkg").mkdir()
                (root / "pkg" / "__init__.py").write_text("")
                (root / "pkg" / "a.py").write_text("from . import b\n")
                (root / "pkg" / "b.py").write_text("VALUE = 1\n")

            (right / "pkg" / "receipt.py").write_text("from . import b\n")
            (right / "pkg" / "a.py").write_text("from . import receipt\n")

            graph = extract_python_dependency_graph(right)
            self.assertIn("pkg/a.py", graph["nodes"])
            self.assertIn(["pkg/a.py", "pkg/receipt.py"], graph["edges"])
            self.assertIn(["pkg/receipt.py", "pkg/b.py"], graph["edges"])

            impact = build_repo_impact(left, right)
            self.assertEqual(impact["node_delta"]["added"], ["pkg/receipt.py"])
            self.assertIn(["pkg/a.py", "pkg/receipt.py"], impact["edge_delta"]["added"])
            self.assertIn(["pkg/a.py", "pkg/b.py"], impact["reachability_delta"]["gained"])

            summary = render_impact_markdown(impact)
            self.assertIn("Dogram Impact Receipt", summary)
            self.assertIn("pkg/receipt.py", summary)


if __name__ == "__main__":
    unittest.main()
