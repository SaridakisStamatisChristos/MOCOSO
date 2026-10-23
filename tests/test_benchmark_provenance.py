"""Adversarial provenance tests; all mutations are confined to temporary Git repos."""
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from benchmarks.compare_v02 import provenance


@unittest.skipUnless(shutil.which('git'), 'Git is required for provenance testing')
class BenchmarkProvenance(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'checkout'
        self.root.mkdir()
        self.git('init', '-q')
        self.path = self.root / 'modconvex.py'
        self.path.write_text('sentinel = 1\n', encoding='utf-8')
        self.git('add', 'modconvex.py')
        self.git('-c', 'user.name=MOCOSO Test',
                 '-c', 'user.email=test@example.invalid',
                 'commit', '-qm', 'baseline')
        self.commit = self.git('rev-parse', 'HEAD')

    def git(self, *args):
        return subprocess.check_output(
            ['git', '-C', str(self.root), *args], text=True,
            stderr=subprocess.DEVNULL
        ).strip()

    def test_clean_pinned_checkout_passes(self):
        result = provenance(self.path, expected_commit=self.commit)
        self.assertEqual(result['git_commit'], self.commit)
        self.assertEqual(result['git_blob_sha'],
                         self.git('rev-parse', f'{self.commit}:modconvex.py'))
        self.assertEqual(result['git_blob_sha'], result['committed_git_blob_sha'])

    def test_tampered_file_with_unchanged_head_is_rejected(self):
        self.path.write_text('sentinel = 2\n', encoding='utf-8')
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.commit)
        with self.assertRaisesRegex(AssertionError, 'baseline file differs'):
            provenance(self.path, expected_commit=self.commit)

    def test_wrong_commit_is_rejected(self):
        with self.assertRaisesRegex(AssertionError, 'baseline drift'):
            provenance(self.path, expected_commit='0' * 40)

    def test_untracked_file_is_rejected(self):
        other = self.root / 'other.py'
        other.write_text('sentinel = 1\n', encoding='utf-8')
        with self.assertRaisesRegex(AssertionError, 'cannot verify baseline file'):
            provenance(other, expected_commit=self.commit)

    def test_missing_git_checkout_is_rejected(self):
        other = Path(self.temp.name) / 'standalone.py'
        other.write_text('sentinel = 1\n', encoding='utf-8')
        with self.assertRaisesRegex(AssertionError, 'baseline drift'):
            provenance(other, expected_commit=self.commit)

    def test_optional_provenance_still_works_for_standalone_file(self):
        other = Path(self.temp.name) / 'standalone.py'
        other.write_text('sentinel = 1\n', encoding='utf-8')
        self.assertIsNone(provenance(other)['git_commit'])
        self.assertEqual(len(provenance(other)['sha256']), 64)


if __name__ == '__main__':
    unittest.main()
