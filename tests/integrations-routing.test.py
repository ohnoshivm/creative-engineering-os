#!/usr/bin/env python3
"""Operational checks for the local CEOS task router."""
import json
import pathlib
import shutil
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
ROUTES = json.loads((ROOT / "integrations/routes.json").read_text())
ROUTE_BY_ID = {route["id"]: route for route in ROUTES["routes"]}
ROUTER = ROOT / "scripts/ceos-route.py"
TEST_ROOT = pathlib.Path.home() / "creative-engineering-os-upstreams/.tests/router"


class Routing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        TEST_ROOT.mkdir(parents=True, exist_ok=True)

    def project(self, package=None):
        path = pathlib.Path(tempfile.mkdtemp(prefix="project-", dir=TEST_ROOT))
        if package is not None:
            (path / "package.json").write_text(json.dumps(package))
        return path

    def route(self, request, project, available, *options):
        command = ["python3", str(ROUTER), request, "--project", str(project), "--format", "json"]
        for capability in available:
            command.extend(["--available", capability])
        command.extend(options)
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        self.assertIn(result.returncode, (0, 2), result.stderr)
        return result.returncode, json.loads(result.stdout)

    def test_nineteen_routes_have_explicit_secondary_roles_and_safe_fallbacks(self):
        routes = ROUTES["routes"]
        expected = {
            "creative-concept": ["ceos-direction", "impeccable"],
            "art-direction": ["ceos-art-direction", "ui-ux-pro-max"],
            "research": ["ui-ux-pro-max", "ceos-reference-library"],
            "typography": ["impeccable", "ui-ux-pro-max"],
            "wireframes": ["ceos-interaction", "ui-ux-pro-max"],
            "motion-direction": ["ceos-motion", "gsap"],
            "gsap-implementation": ["gsap", "ceos-motion"],
            "react-animations": ["react-bits", "gsap"],
            "components-forms": ["shadcn", "ui-ux-pro-max"],
            "interactive-elements": ["react-bits", "ceos-creative-coding"],
            "three-r3f": ["pmndrs-examples", "ceos-realtime-3d"],
            "glsl-shaders": ["ceos-shader", "pmndrs-examples"],
            "architecture": ["ceos-frontend", "superpowers-tdd"],
            "complex-implementation": ["superpowers-tdd", "ceos-frontend"],
            "debugging-verification": ["superpowers-verification", "existing-qa"],
            "visual-critique": ["impeccable", "ceos-visual-audit"],
            "browser-qa": ["existing-browser-tools", "superpowers-verification"],
            "performance": ["ceos-performance", "existing-performance-tools"],
            "release": ["ceos-production-quality", "superpowers-verification"],
        }
        self.assertEqual(len(routes), 19)
        self.assertEqual(len({route["id"] for route in routes}), 19)
        self.assertEqual({route["id"]: route["capabilities"] for route in routes}, expected)
        for route in routes:
            self.assertEqual(len(route["capabilities"]), 2, route["id"])
            self.assertEqual(len(set(route["capabilities"])), 2, route["id"])
            self.assertTrue(all(cap in ROUTES["capabilities"] for cap in route["capabilities"]))
            self.assertTrue(route.get("secondaryContribution", "").strip(), route["id"])
            if ROUTES["capabilities"][route["capabilities"][0]].get("requiresReact"):
                self.assertTrue(route.get("nonReactFallback", "").strip(), route["id"])
            self.assertTrue(
                any(not ROUTES["capabilities"][cap].get("requiresReact") for cap in route["capabilities"]),
                f"{route['id']} has no non-React option",
            )
        for capability in ("react-bits", "shadcn", "pmndrs-examples"):
            self.assertTrue(ROUTES["capabilities"][capability]["requiresReact"])

    def test_eight_user_scenarios_select_one_primary_and_no_unrelated_capability(self):
        all_capabilities = list(ROUTES["capabilities"])
        react = {"dependencies": {"react": "^19.0.0", "react-dom": "^19.0.0", "vite": "^7.0.0"}}
        cases = [
            ("Improve homepage visual hierarchy", None, "visual-critique", "impeccable"),
            ("Create a responsive editorial layout", None, "typography", "impeccable"),
            ("Create an animated headline", react, "react-animations", "react-bits"),
            ("Build a GSAP scroll sequence", None, "gsap-implementation", "gsap"),
            ("Build an accessible dialog component", react, "components-forms", "shadcn"),
            ("Prototype an interactive 3D object with React Three Fiber", react, "three-r3f", "pmndrs-examples"),
            ("Debug a broken production component", None, "debugging-verification", "superpowers-verification"),
            ("Audit an inconsistent landing page", None, "visual-critique", "impeccable"),
        ]
        for request, package, expected_route, expected_primary in cases:
            with self.subTest(request=request):
                project = self.project(package)
                try:
                    code, result = self.route(request, project, all_capabilities)
                    self.assertEqual(code, 0)
                    self.assertEqual(result["route"]["id"], expected_route)
                    self.assertEqual(result["primary"]["id"], expected_primary)
                    if package is not None:
                        self.assertEqual(result["framework"]["name"], "vite-react")
                        self.assertTrue(result["framework"]["reactRuntime"])
                    recommendations = [result["primary"]["id"]]
                    self.assertEqual(recommendations, [expected_primary])
                    self.assertNotIn("secondary", result)
                    self.assertNotIn("detectedCapabilities", result)
                    unrelated = set(all_capabilities) - set(ROUTE_BY_ID[expected_route]["capabilities"])
                    self.assertTrue(set(recommendations).isdisjoint(unrelated))
                finally:
                    shutil.rmtree(project)

    def test_modes_escalate_without_concept_gates_for_trivial_css(self):
        project = self.project({"dependencies": {}})
        try:
            code, fast = self.route("Fix one CSS spacing value", project, ["ceos-art-direction"])
            self.assertEqual(code, 2)
            self.assertEqual(fast["mode"], "FAST")
            self.assertIn("skip concept options, owner approvals", fast["workflow"].lower())
            self.assertNotIn("three distinct concepts", fast["workflow"].lower())

            _, standard = self.route("Research references for a page", project, ["ui-ux-pro-max"])
            self.assertEqual(standard["mode"], "STANDARD")
            _, expanded = self.route("Minor CSS fix for the design system", project, ["ceos-art-direction"])
            self.assertEqual(expanded["mode"], "STANDARD")
            self.assertIn("expanded scope", expanded["modeReason"])
            _, flagship = self.route("Build a flagship immersive site from scratch", project, ["ceos-direction"])
            self.assertEqual(flagship["mode"], "FLAGSHIP")
            _, override = self.route("Fix one CSS spacing value", project, ["ceos-art-direction"], "--mode", "STANDARD")
            self.assertEqual(override["mode"], "STANDARD")
        finally:
            shutil.rmtree(project)

    def test_react_only_capabilities_fall_back_for_non_react_projects(self):
        project = self.project({"dependencies": {"vite": "^7.0.0"}})
        cases = [
            ("Create a React Bits reveal animation", "react-bits", "gsap", "CSS or WAAPI"),
            ("Build a shadcn accessible dialog", "shadcn", "ui-ux-pro-max", "semantic HTML"),
            ("Build a React Three Fiber scene", "pmndrs-examples", "ceos-realtime-3d", "vanilla Three.js"),
            ("Create an interactive component using React Bits", "react-bits", "ceos-creative-coding", "semantic HTML"),
        ]
        try:
            self.assertEqual(ROUTES["capabilities"]["react-bits"]["requiresReact"], True)
            for request, excluded, fallback, guidance in cases:
                with self.subTest(request=request):
                    code, result = self.route(request, project, list(ROUTES["capabilities"]))
                    self.assertEqual(code, 0)
                    self.assertEqual(result["framework"]["name"], "vite")
                    self.assertFalse(result["framework"]["reactRuntime"])
                    self.assertNotEqual(result["primary"]["id"], excluded)
                    self.assertEqual(result["primary"]["id"], fallback)
                    self.assertTrue(result["primary"]["compatible"])
                    self.assertTrue(any(guidance.lower() in note.lower() for note in result["notes"]))
                    _, with_secondary = self.route(
                        request, project, list(ROUTES["capabilities"]), "--need-secondary"
                    )
                    self.assertNotIn("secondary", with_secondary)

            _, override = self.route(
                "Create a React Bits reveal animation",
                project,
                list(ROUTES["capabilities"]),
                "--framework", "react",
            )
            self.assertFalse(override["framework"]["reactRuntime"])
            self.assertEqual(override["primary"]["id"], "gsap")
        finally:
            shutil.rmtree(project)

        react_project = self.project({"dependencies": {"react": "^19.0.0", "react-dom": "^19.0.0"}})
        try:
            _, constrained = self.route(
                "Build an accessible shadcn dialog without React",
                react_project,
                list(ROUTES["capabilities"]),
            )
            self.assertIn("noReact", constrained["constraints"])
            self.assertFalse(constrained["framework"]["reactRuntime"])
            self.assertEqual(constrained["primary"]["id"], "ui-ux-pro-max")
        finally:
            shutil.rmtree(react_project)

    def test_react_runtime_is_detected_in_hybrid_framework_projects(self):
        project = self.project({"dependencies": {"astro": "^5.0.0", "@astrojs/react": "^4.0.0", "react": "^19.0.0"}})
        try:
            _, result = self.route(
                "Create a React Bits reveal animation", project, list(ROUTES["capabilities"])
            )
            self.assertEqual(result["framework"]["name"], "astro")
            self.assertTrue(result["framework"]["reactRuntime"])
            self.assertEqual(result["primary"]["id"], "react-bits")
        finally:
            shutil.rmtree(project)

    def test_secondary_is_opt_in_and_explains_its_contribution(self):
        project = self.project({"dependencies": {"react": "^19.0.0"}})
        try:
            _, primary_only = self.route("Create an animated headline", project, list(ROUTES["capabilities"]))
            self.assertEqual(primary_only["primary"]["id"], "react-bits")
            self.assertNotIn("secondary", primary_only)
            _, with_secondary = self.route(
                "Create an animated headline", project, list(ROUTES["capabilities"]), "--need-secondary"
            )
            self.assertEqual(with_secondary["secondary"]["id"], "gsap")
            self.assertTrue(with_secondary["secondary"]["contribution"])

            _, detected_fallback = self.route("Build a GSAP scroll sequence", project, ["ceos-motion"])
            self.assertEqual(detected_fallback["primary"]["id"], "ceos-motion")
            _, unavailable = self.route("Build a GSAP scroll sequence", project, ["ceos-direction"])
            self.assertEqual(unavailable["primary"]["id"], "gsap")
            self.assertFalse(unavailable["primary"]["available"])
            self.assertTrue(unavailable["notes"])
        finally:
            shutil.rmtree(project)

    def test_route_selection_is_deterministic(self):
        project = self.project({})
        try:
            _, first = self.route("Create a wireframe for the signup user flow", project, list(ROUTES["capabilities"]))
            _, second = self.route("Create a wireframe for the signup user flow", project, list(ROUTES["capabilities"]))
            self.assertEqual(first, second)
        finally:
            shutil.rmtree(project)


if __name__ == "__main__":
    unittest.main()
