#!/usr/bin/env python3
"""Build a deterministic searchable index from a pinned pmndrs/examples checkout."""
from __future__ import annotations

import argparse
import json
import pathlib
import subprocess

REPOSITORY = "https://github.com/pmndrs/examples"
REVISION = "9905cd7b3d030a0ba5c6d327e15fe30ab648abb6"
EXPECTED_EXAMPLES = 200
ROOT = pathlib.Path(__file__).resolve().parents[2]

POINTER_TAGS = {
    "annotations",
    "autofocus",
    "events",
    "highlight",
    "interaction",
    "intersection",
    "raycast",
    "selection",
}
HIGH_COMPLEXITY_TAGS = {
    "bvh",
    "custom-renderer",
    "gpgpu",
    "physics",
    "postprocessing",
    "shader",
    "ssgi",
    "ssr",
    "webgpu",
}


def read_json(path: pathlib.Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def string_mapping(value: object, label: str) -> dict[str, str]:
    if not isinstance(value, dict) or any(not isinstance(k, str) or not isinstance(v, str) for k, v in value.items()):
        raise ValueError(f"{label} must be an object of string values")
    return dict(sorted(value.items()))


def derive_input(tags: list[str]) -> list[str]:
    signals = set()
    if POINTER_TAGS.intersection(tags):
        signals.add("pointer")
    if "scroll" in tags:
        signals.add("scroll")
    if "audio" in tags:
        signals.add("audio")
    if "controls" in tags:
        signals.add("controls-unspecified")
    if "game" in tags:
        signals.add("game-controls-unspecified")
    return sorted(signals or {"not-tagged"})


def derive_complexity(tags: list[str], libraries: list[str]) -> str:
    if HIGH_COMPLEXITY_TAGS.intersection(tags) or len(libraries) >= 5:
        return "high"
    if len(tags) >= 4 or len(libraries) >= 4:
        return "medium"
    return "low"


def derive_renderer(runtime_dependencies: dict[str, str], libraries: list[str]) -> tuple[str, str]:
    if "@react-three/fiber" in runtime_dependencies or "@react-three/fiber" in libraries:
        return "r3f", "rewrite-required"
    if "three" in runtime_dependencies:
        return "vanilla-three", "native"
    return "other-or-unknown", "unclassified"


def build_index(source: pathlib.Path) -> dict:
    license_text = (source / "LICENSE").read_text(encoding="utf-8")
    if "MIT License" not in license_text:
        raise ValueError("Pinned repository LICENSE is not recognized as MIT")

    examples_dir = source / "examples"
    entries = []
    for directory in sorted(path for path in examples_dir.iterdir() if path.is_dir()):
        metadata_path = directory / "pmndrs.json"
        package_path = directory / "package.json"
        if not metadata_path.exists() and not package_path.exists():
            continue
        if not metadata_path.is_file() or not package_path.is_file():
            raise ValueError(f"{directory.name} must contain both pmndrs.json and package.json")

        metadata = read_json(metadata_path)
        package = read_json(package_path)
        scripts = package.get("scripts", {})
        if not isinstance(scripts, dict):
            raise ValueError(f"{package_path} scripts must be an object")
        dev_command = scripts.get("dev")
        if not isinstance(dev_command, str) or not dev_command.strip():
            continue

        tags = metadata.get("tags")
        libraries = metadata.get("libraries")
        authors = metadata.get("authors")
        assets = metadata.get("assets")
        for field in ("title", "description", "source"):
            if not isinstance(metadata.get(field), str):
                raise ValueError(f"{metadata_path} {field} must be a string")
        if not isinstance(tags, list) or not all(isinstance(v, str) for v in tags):
            raise ValueError(f"{metadata_path} tags must be an array of strings")
        if not isinstance(libraries, list) or not all(isinstance(v, str) for v in libraries):
            raise ValueError(f"{metadata_path} libraries must be an array of strings")
        if not isinstance(authors, list) or not all(isinstance(v, str) for v in authors):
            raise ValueError(f"{metadata_path} authors must be an array of strings")
        if not isinstance(assets, list) or not all(isinstance(v, dict) for v in assets):
            raise ValueError(f"{metadata_path} assets must be an array of objects")

        runtime_dependencies = string_mapping(package.get("dependencies", {}), f"{package_path} dependencies")
        development_dependencies = string_mapping(package.get("devDependencies", {}), f"{package_path} devDependencies")
        if not isinstance(package.get("name"), str) or not isinstance(package.get("version"), str):
            raise ValueError(f"{package_path} name and version must be strings")
        renderer, vanilla_portability = derive_renderer(runtime_dependencies, libraries)

        entry = {
            "slug": directory.name,
            "path": f"examples/{directory.name}",
            "title": metadata.get("title", ""),
            "description": metadata.get("description", ""),
            "tags": tags,
            "libraries": libraries,
            "authors": authors,
            "source": metadata.get("source", ""),
            "assets": assets,
            "license": "MIT",
            "package": {
                "name": package.get("name", ""),
                "version": package["version"],
                "dev_command": dev_command,
                "dependencies": {
                    "runtime": runtime_dependencies,
                    "development": development_dependencies,
                },
            },
            "input": derive_input(tags),
            "complexity": derive_complexity(tags, libraries),
            "renderer": renderer,
            "vanilla_portability": vanilla_portability,
        }
        for key in ("publishedAt", "notes"):
            if key in metadata:
                entry[key] = metadata[key]
        entries.append(entry)

    entries.sort(key=lambda example: example["slug"])
    return {
        "format_version": 1,
        "source": {
            "repository": REPOSITORY,
            "revision": REVISION,
            "license": "MIT",
        },
        "example_count": len(entries),
        "heuristics": {
            "input": "Mapped only from upstream tags: interaction/events/raycast/selection/annotations/autofocus => pointer; scroll => scroll; audio => audio; controls/game => unspecified controls; no match => not-tagged.",
            "complexity": "High for bvh/custom-renderer/gpgpu/physics/postprocessing/shader/ssgi/ssr/webgpu tags or 5+ related libraries; medium for 4+ tags or 4+ related libraries; low otherwise. This is a metadata triage estimate, not a runtime or code-size measure.",
            "renderer": "r3f when @react-three/fiber appears in runtime dependencies or related libraries; vanilla-three when only a three.js runtime is declared; otherwise other-or-unknown.",
            "vanilla_portability": "R3F entries require adaptation to vanilla Three.js; vanilla-three entries are already native; unknown renderer entries are unclassified.",
            "runnable": "Included when an example has pmndrs.json, package.json, and a non-empty package scripts.dev command; this does not mean each example was built or run.",
        },
        "examples": entries,
    }


def verify_checkout(source: pathlib.Path) -> None:
    origin = subprocess.run(
        ["git", "-C", str(source), "config", "--get", "remote.origin.url"],
        check=True,
        capture_output=True,
        text=True,
        timeout=15,
    ).stdout.strip()
    if origin not in {REPOSITORY, REPOSITORY + ".git", "git@github.com:pmndrs/examples.git"}:
        raise ValueError(f"Expected official upstream origin {REPOSITORY}, found {origin}")
    revision = subprocess.run(
        ["git", "-C", str(source), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
        timeout=15,
    ).stdout.strip()
    if revision != REVISION:
        raise ValueError(f"Expected pinned revision {REVISION}, found {revision}")
    status = subprocess.run(
        ["git", "-C", str(source), "status", "--porcelain", "--untracked-files=no"],
        check=True,
        capture_output=True,
        text=True,
        timeout=15,
    ).stdout.strip()
    if status:
        raise ValueError("Pinned source checkout has tracked changes")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=pathlib.Path, help="clean checkout of the pinned upstream")
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=ROOT / "integrations/indexes/pmndrs-examples.json",
        help="output JSON path (default: integrations/indexes/pmndrs-examples.json)",
    )
    args = parser.parse_args()
    source = args.source.expanduser().resolve(strict=True)
    verify_checkout(source)
    index = build_index(source)
    if index["example_count"] != EXPECTED_EXAMPLES:
        raise ValueError(f"Expected {EXPECTED_EXAMPLES} runnable examples at the pinned revision, found {index['example_count']}")
    output = args.output.expanduser()
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(index, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {index['example_count']} examples to {output}")


if __name__ == "__main__":
    main()
