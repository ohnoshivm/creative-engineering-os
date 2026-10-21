#!/usr/bin/env python3
"""Small deterministic and heuristic checks for the pmndrs metadata index."""
import importlib.util
import json
import pathlib
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "pmndrs_examples_index", ROOT / "scripts/integrations/pmndrs_examples_index.py"
)
indexer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(indexer)


class PmndrsExamplesIndex(unittest.TestCase):
    def test_determinism_metadata_derivations_and_portability(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = pathlib.Path(temporary)
            (source / "LICENSE").write_text("MIT License\n", encoding="utf-8")
            examples = source / "examples"
            r3f = examples / "basic-example"
            r3f.mkdir(parents=True)
            (r3f / "pmndrs.json").write_text(json.dumps({
                "title": "Basic Example",
                "description": "A pointer demo",
                "tags": ["interaction", "events"],
                "libraries": ["@react-three/fiber", "@react-three/drei"],
                "authors": ["Author"],
                "source": "https://example.com/source",
                "assets": [{"name": "Model", "creator": "Artist", "license": "CC-BY-4.0"}],
            }), encoding="utf-8")
            (r3f / "package.json").write_text(json.dumps({
                "name": "basic-example",
                "version": "1.0.0",
                "scripts": {"dev": "vite --host"},
                "dependencies": {"three": "1.0.0", "@react-three/fiber": "2.0.0"},
                "devDependencies": {"vite": "3.0.0"},
            }), encoding="utf-8")

            vanilla = examples / "vanilla-shader"
            vanilla.mkdir()
            (vanilla / "pmndrs.json").write_text(json.dumps({
                "title": "Vanilla Shader",
                "description": "A shader example",
                "tags": ["shader"],
                "libraries": [],
                "authors": ["Author"],
                "source": "https://example.com/shader",
                "assets": [],
            }), encoding="utf-8")
            (vanilla / "package.json").write_text(json.dumps({
                "name": "vanilla-shader",
                "version": "1.0.0",
                "scripts": {"dev": "vite"},
                "dependencies": {"three": "1.0.0"},
                "devDependencies": {},
            }), encoding="utf-8")

            first = indexer.build_index(source)
            second = indexer.build_index(source)
            self.assertEqual(json.dumps(first, sort_keys=True), json.dumps(second, sort_keys=True))
            self.assertEqual([entry["slug"] for entry in first["examples"]], ["basic-example", "vanilla-shader"])

            r3f_entry, vanilla_entry = first["examples"]
            self.assertEqual(r3f_entry["input"], ["pointer"])
            self.assertEqual(r3f_entry["complexity"], "low")
            self.assertEqual(r3f_entry["renderer"], "r3f")
            self.assertEqual(r3f_entry["vanilla_portability"], "rewrite-required")
            self.assertEqual(r3f_entry["assets"][0]["license"], "CC-BY-4.0")
            self.assertEqual(list(r3f_entry["package"]["dependencies"]["runtime"]), ["@react-three/fiber", "three"])
            self.assertEqual(vanilla_entry["input"], ["not-tagged"])
            self.assertEqual(vanilla_entry["complexity"], "high")
            self.assertEqual(vanilla_entry["renderer"], "vanilla-three")
            self.assertEqual(vanilla_entry["vanilla_portability"], "native")
            self.assertEqual(indexer.derive_complexity(["animation", "events", "controls", "scroll"], []), "medium")
            self.assertEqual(indexer.derive_input(["controls"]), ["controls-unspecified"])
            self.assertEqual(indexer.derive_renderer({}, []), ("other-or-unknown", "unclassified"))


if __name__ == "__main__":
    unittest.main()
