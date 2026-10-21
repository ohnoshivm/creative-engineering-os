#!/usr/bin/env python3
"""Recommend one CEOS capability for a task; never dispatches or installs tools."""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRAMEWORKS = ("auto", "next", "react", "vite-react", "astro", "svelte", "vue", "vite", "vanilla", "unknown")
REACT_FRAMEWORKS = {"next", "react", "vite-react"}


def normalize(value):
    return " ".join(re.findall(r"[a-z0-9]+", str(value).casefold()))


def contains_phrase(text, phrase):
    text = " " + normalize(text) + " "
    phrase = " " + normalize(phrase) + " "
    return phrase.strip() and phrase in text


def load_routes():
    data = json.loads((ROOT / "integrations/routes.json").read_text())
    routes = data.get("routes", [])
    capabilities = data.get("capabilities", {})
    if data.get("schemaVersion") != 1 or len(routes) != 19 or not isinstance(capabilities, dict):
        raise ValueError("unsupported route catalog")
    ids = {route["id"] for route in routes}
    if len(ids) != 19 or any(len(route.get("capabilities", [])) != 2 for route in routes):
        raise ValueError("invalid route catalog")
    if any(cap not in capabilities for route in routes for cap in route["capabilities"]):
        raise ValueError("invalid capability reference")
    if any(not route.get("secondaryContribution", "").strip() for route in routes):
        raise ValueError("every secondary capability needs an explicit contribution")
    if any(all(capabilities[cap].get("requiresReact") for cap in route["capabilities"]) for route in routes):
        raise ValueError("every route needs a non-React option")
    return data


def match_route(request, routes):
    normalized = normalize(request)
    matches = []
    for order, route in enumerate(routes):
        phrases = [route["id"].replace("-", " "), route["label"], *route["triggers"]]
        scores = []
        for phrase in phrases:
            candidate = normalize(phrase)
            if not candidate or not contains_phrase(normalized, candidate):
                continue
            scores.append(10000 + len(candidate) if candidate == normalized else 100 * len(candidate.split()) + len(candidate))
        if scores:
            matches.append((max(scores), -order, route))
    return max(matches, default=(None, None, None))[2]


def detect_mode(request, rules, requested):
    if requested != "AUTO":
        return requested, "explicit override"
    if any(contains_phrase(request, signal) for signal in rules["flagshipSignals"]):
        return "FLAGSHIP", "flagship scope signal"
    if any(contains_phrase(request, signal) for signal in rules["fastExclusions"]):
        return "STANDARD", "expanded scope overrides small-change wording"
    if any(contains_phrase(request, signal) for signal in rules["fastSignals"]):
        return "FAST", "small local change signal"
    has_action = any(contains_phrase(request, signal) for signal in rules["fastActions"])
    has_scope = any(contains_phrase(request, signal) for signal in rules["fastScope"])
    has_exclusion = any(contains_phrase(request, signal) for signal in rules["fastExclusions"])
    if has_action and has_scope and not has_exclusion:
        return "FAST", "single local styling signal"
    return "STANDARD", "default scoped-work mode"


def detect_constraints(request, signals):
    return {key: any(contains_phrase(request, phrase) for phrase in phrases) for key, phrases in signals.items()}


def detect_framework(project, override):
    dependencies = set()
    notes = []
    package = project / "package.json"
    if package.is_file():
        try:
            data = json.loads(package.read_text())
            for group in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
                dependencies.update(data.get(group, {}).keys())
        except (OSError, ValueError, AttributeError):
            notes.append("package.json could not be parsed; used project config filenames")

    has_react = "react" in dependencies or "react-dom" in dependencies
    if override != "auto":
        if override in REACT_FRAMEWORKS and not has_react:
            notes.append("Framework override did not establish a React runtime in package.json; React-only routes remain excluded.")
        return override, has_react, "explicit override checked against package metadata", notes

    if "next" in dependencies or any(project.glob("next.config.*")):
        return "next", has_react, "package metadata or config filename", notes
    if "astro" in dependencies or any(project.glob("astro.config.*")):
        return "astro", has_react, "package metadata or config filename", notes
    if "svelte" in dependencies or "@sveltejs/kit" in dependencies or any(project.glob("svelte.config.*")):
        return "svelte", has_react, "package metadata or config filename", notes
    if "vue" in dependencies or "nuxt" in dependencies:
        return "vue", has_react, "package metadata", notes
    if has_react and ("vite" in dependencies or "@vitejs/plugin-react" in dependencies):
        return "vite-react", True, "package metadata", notes
    if has_react:
        return "react", True, "package metadata", notes
    if "vite" in dependencies or any(project.glob("vite.config.*")):
        return "vite", False, "package metadata or config filename", notes
    if dependencies:
        return "unknown", False, "package metadata", notes
    if any((project / name).exists() for name in ("index.html", "src", "public")):
        return "vanilla", False, "project files", notes
    return "unknown", False, "no framework markers found", notes


def skill_roots(project):
    home = Path.home()
    candidates = [
        ROOT / "skills",
        project / "skills",
        project / ".agents/skills",
        project / ".claude/skills",
        project / ".codex/skills",
        project / ".gemini/antigravity/skills",
        project / ".config/opencode/skills",
        home / ".agents/skills",
        home / ".claude/skills",
        home / ".codex/skills",
        home / ".gemini/antigravity/skills",
        home / ".config/opencode/skills",
    ]
    roots = []
    seen = set()
    for path in candidates:
        try:
            key = path.resolve()
        except OSError:
            key = path.absolute()
        if key not in seen:
            roots.append(path)
            seen.add(key)
    return roots


def discover_capabilities(catalog, project):
    roots = skill_roots(project)
    available = set()
    for capability_id, capability in catalog.items():
        if any((root / skill).is_dir() for root in roots for skill in capability.get("skills", [])):
            available.add(capability_id)
            continue
        if any((base / relative).is_file() for base in (ROOT, project) for relative in capability.get("paths", [])):
            available.add(capability_id)
    return available


def candidate(capability_id, catalog, available, profile, constraints):
    spec = catalog[capability_id]
    problems = []
    if spec.get("requiresReact") and not profile["reactRuntime"]:
        problems.append("requires an existing React runtime")
    if spec.get("requiresWebgl") and constraints.get("noWebgl"):
        problems.append("conflicts with the no-WebGL constraint")
    return {
        "id": capability_id,
        "label": spec["label"],
        "available": capability_id in available,
        "compatible": not problems,
        "note": "; ".join(problems) if problems else None,
    }


def resolve(request, data, project, mode_override="AUTO", framework_override="auto", available_override=None, need_secondary=False):
    route = match_route(request, data["routes"])
    mode, mode_reason = detect_mode(request, data["modeRules"], mode_override)
    framework, react_runtime, framework_source, framework_notes = detect_framework(project, framework_override)
    constraints = detect_constraints(request, data["constraintSignals"])
    if constraints["noReact"]:
        react_runtime = False
    if available_override is None:
        available = discover_capabilities(data["capabilities"], project)
        availability_source = "filesystem skill and tool paths"
    else:
        available = set(available_override)
        availability_source = "explicit capability list"

    result = {
        "route": {"id": route["id"], "label": route["label"]} if route else None,
        "mode": mode,
        "modeReason": mode_reason,
        "framework": {"name": framework, "reactRuntime": react_runtime, "source": framework_source},
        "constraints": [name for name, active in constraints.items() if active],
        "availabilitySource": availability_source,
        "workflow": data["modes"][mode]["guidance"],
        "escalateWhen": data["modes"][mode]["escalateWhen"],
        "notes": framework_notes,
    }
    if route is None:
        result["message"] = "No specialist route matched. Use the task mode to scale the checks, or pass a known route name or phrase."
        return result

    options = [candidate(capability_id, data["capabilities"], available, result["framework"], constraints) for capability_id in route["capabilities"]]
    compatible = [option for option in options if option["compatible"]]
    available_compatible = [option for option in compatible if option["available"]]
    if not compatible:
        result["message"] = "No compatible capability matched the project's framework or constraints. Use an existing native alternative or revise the task constraint."
        return result
    selected = (available_compatible or compatible)[0]
    if selected["id"] != options[0]["id"]:
        if not options[0]["compatible"]:
            result["notes"].append(f"Selected {selected['label']} because {options[0]['label']} {options[0]['note']}.")
            if "requires an existing React runtime" in (options[0]["note"] or "") and route.get("nonReactFallback"):
                result["notes"].append("Non-React alternative: " + route["nonReactFallback"])
        elif not options[0]["available"] and selected["available"]:
            result["notes"].append(f"Selected {selected['label']} because it is the first detected compatible capability.")
    elif not selected["available"]:
        result["notes"].append(f"{selected['label']} was not detected in skill or tool paths; verify the host capability before relying on it.")
    result["primary"] = selected

    if need_secondary:
        remaining = [option for option in compatible if option["id"] != selected["id"]]
        secondary_options = [option for option in remaining if option["available"]]
        secondary_options.extend(option for option in remaining if not option["available"])
        if secondary_options:
            result["secondary"] = {**secondary_options[0], "contribution": route["secondaryContribution"]}
    return result


def render_text(result, include_secondary):
    if result["route"]:
        print(f"Route: {result['route']['label']} ({result['route']['id']})")
    else:
        print(result["message"])
    framework = result["framework"]
    print(f"Mode: {result['mode']} ({result['modeReason']})")
    print(f"Framework: {framework['name']} (React runtime: {'yes' if framework['reactRuntime'] else 'no'})")
    print("Constraints: " + (", ".join(result["constraints"]) or "none detected"))
    if result.get("primary"):
        primary = result["primary"]
        status = "available" if primary["available"] else "not detected"
        suffix = f" — {primary['note']}" if primary.get("note") else ""
        print(f"Primary: {primary['label']} [{status}]{suffix}")
    if include_secondary and result.get("secondary"):
        secondary = result["secondary"]
        status = "available" if secondary["available"] else "not detected"
        suffix = f" — {secondary['note']}" if secondary.get("note") else ""
        print(f"Secondary: {secondary['label']} [{status}] — {secondary['contribution']}{suffix}")
    if result["notes"]:
        for note in result["notes"]:
            print("Note: " + note)
    print("Workflow: " + result["workflow"])
    if result["escalateWhen"]:
        print("Escalate when: " + "; ".join(result["escalateWhen"]))


def main(argv=None):
    try:
        data = load_routes()
    except (OSError, ValueError, json.JSONDecodeError):
        print("Router data is invalid; check integrations/routes.json.", file=sys.stderr)
        return 2

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("request", nargs="*", help="task phrase or request")
    parser.add_argument("--task-id", choices=[route["id"] for route in data["routes"]], help="select a known route directly")
    parser.add_argument("--project", type=Path, default=Path.cwd(), help="project directory to inspect (default: current directory)")
    parser.add_argument("--mode", type=str.upper, choices=("AUTO", "FAST", "STANDARD", "FLAGSHIP"), default="AUTO")
    parser.add_argument("--framework", type=str.lower, choices=FRAMEWORKS, default="auto")
    parser.add_argument("--available", action="append", help="use only these capability IDs instead of filesystem discovery; repeat as needed")
    parser.add_argument("--need-secondary", action="store_true", help="include one compatible secondary capability")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)
    if args.task_id and args.request:
        parser.error("pass either request text or --task-id")
    if not args.task_id and not args.request:
        parser.error("pass task text or --task-id")
    project = args.project.expanduser().resolve()
    if not project.is_dir():
        parser.error("--project must be an existing directory")
    request = args.task_id or " ".join(args.request)
    available_override = args.available
    if available_override:
        unknown = sorted(set(available_override) - set(data["capabilities"]))
        if unknown:
            parser.error("--available contains an unknown capability ID")
    result = resolve(request, data, project, args.mode, args.framework, available_override, args.need_secondary)
    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        render_text(result, args.need_secondary)
    return 0 if result.get("primary") else 2


if __name__ == "__main__":
    raise SystemExit(main())
