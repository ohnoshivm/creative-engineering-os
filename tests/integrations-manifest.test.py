#!/usr/bin/env python3
"""The checked-in integration manifest is reproducible from evidence and pins."""
import json
import pathlib
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
GENERATOR = ROOT / 'scripts/integrations/generate_manifest.py'


class Manifest(unittest.TestCase):
    def test_manifest_has_one_entry_per_named_integration(self):
        data = json.loads((ROOT / 'integrations/manifest.json').read_text())
        self.assertEqual(len(data['integrations']), 8)

    def test_regenerated_manifest_matches_committed_bytes(self):
        result = subprocess.run(
            [sys.executable, str(GENERATOR), '--check'],
            capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())


if __name__ == '__main__':
    unittest.main()
