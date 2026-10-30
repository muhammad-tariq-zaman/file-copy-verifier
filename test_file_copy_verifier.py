import os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import snapshot, compare


class TestCopyVerifier(unittest.TestCase):
    def test_identical_trees(self):
        with tempfile.TemporaryDirectory() as tmp:
            for side in ("src", "dst"):
                d = os.path.join(tmp, side)
                os.makedirs(d)
                open(os.path.join(d, "a.txt"), "w").write("hello")
            self.assertEqual(compare(snapshot(os.path.join(tmp, "src")), snapshot(os.path.join(tmp, "dst"))), ([], [], []))

    def test_missing_and_differing(self):
        with tempfile.TemporaryDirectory() as tmp:
            src, dst = os.path.join(tmp, "src"), os.path.join(tmp, "dst")
            os.makedirs(src); os.makedirs(dst)
            open(os.path.join(src, "a.txt"), "w").write("one")
            open(os.path.join(src, "b.txt"), "w").write("two")
            open(os.path.join(dst, "a.txt"), "w").write("ONE")
            missing, extra, differing = compare(snapshot(src), snapshot(dst))
            self.assertEqual(missing, ["b.txt"])
            self.assertEqual(differing, ["a.txt"])
