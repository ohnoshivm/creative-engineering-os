#!/usr/bin/env python3
"""Behavior checks for routing, framework boundaries and evidence validation."""
import importlib.util
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('ceos_integrations', ROOT / 'scripts/integrations.py')
api = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api)


class Routing(unittest.TestCase):
    def test_cli_route_delegates_to_the_single_router(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = pathlib.Path(tmp)
            (project / 'package.json').write_text(json.dumps({'dependencies': {'react': '19'}}))
            result = subprocess.run(
                [sys.executable, str(ROOT / 'scripts/integrations.py'), 'route',
                 'Build a GSAP scroll sequence', '--project', str(project), '--secondary'],
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            routed = json.loads(result.stdout)
            self.assertEqual(routed['route']['id'], 'gsap-implementation')
            self.assertEqual(routed['primary']['id'], 'gsap')
            self.assertEqual(routed['secondary']['id'], 'ceos-motion')

    def test_existing_task_phrases_use_the_ceos_route_catalog(self):
        cases = [
            ("Improve a homepage's visual hierarchy", {}, 'visual-critique', 'impeccable'),
            ('Design a responsive editorial layout', {}, 'typography', 'impeccable'),
            ('Implement an animated headline', {'react': '19'}, 'react-animations', 'react-bits'),
            ('Build a GSAP scroll sequence', {}, 'gsap-implementation', 'gsap'),
            ('Add an accessible dialog', {'react': '19'}, 'components-forms', 'shadcn'),
            ('Prototype an interactive 3D object', {'react': '19'}, 'three-r3f', 'pmndrs-examples'),
            ('Debug a broken production component', {}, 'debugging-verification', 'superpowers-verification'),
            ('Audit a visually inconsistent landing page', {}, 'visual-critique', 'impeccable'),
        ]
        for task, dependencies, expected_route, expected_primary in cases:
            with self.subTest(task=task), tempfile.TemporaryDirectory() as tmp:
                project = pathlib.Path(tmp)
                (project / 'package.json').write_text(json.dumps({'dependencies': dependencies}))
                result = api.route(task, project)
                self.assertEqual(result['route']['id'], expected_route)
                self.assertEqual(result['primary']['id'], expected_primary)

    def test_framework_fallbacks_and_modes_come_from_the_ceos_router(self):
        cases = [
            ('Add an accessible dialog', 'components-forms', 'ui-ux-pro-max'),
            ('Prototype an interactive 3D object', 'three-r3f', 'ceos-realtime-3d'),
            ('Implement an animated headline', 'react-animations', 'gsap'),
        ]
        for task, expected_route, expected_primary in cases:
            with self.subTest(task=task), tempfile.TemporaryDirectory() as tmp:
                project = pathlib.Path(tmp)
                result = api.route(task, project)
                self.assertEqual(result['route']['id'], expected_route)
                self.assertEqual(result['primary']['id'], expected_primary)

        for task, expected_mode in (
            ('Fix CSS spacing', 'FAST'),
            ('Design a landing page', 'STANDARD'),
            ('Build an immersive WebGL experience', 'FLAGSHIP'),
        ):
            self.assertEqual(api.route(task)['mode'], expected_mode)
        result = api.route('Fix visual hierarchy', secondary=True)
        self.assertEqual(result['primary']['id'], 'impeccable')
        self.assertEqual(result['secondary']['id'], 'ceos-visual-audit')
        self.assertEqual(api.route('Choose a color palette')['primary']['id'], 'ceos-art-direction')
        self.assertEqual(api.route('Review performance budgets')['primary']['id'], 'ceos-performance')

    def test_project_detection_is_read_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = pathlib.Path(tmp)
            (p/'package.json').write_text(json.dumps({'dependencies': {'astro': '7', 'react': '19'}}))
            before = (p/'package.json').read_bytes()
            result = api.route('Build an accessible dialog', p)
            self.assertEqual(result['framework']['name'], 'astro')
            self.assertTrue(result['framework']['reactRuntime'])
            self.assertEqual((p/'package.json').read_bytes(), before)


class Evidence(unittest.TestCase):
    def test_failed_missing_and_escaping_evidence_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = pathlib.Path(tmp)
            (p/'proof.log').write_text('real check output')
            state = {'mode': 'FAST', 'ui_changed': False, 'logic_changed': False,
                     'security_sensitive': False, 'checks': [
                         {'name': 'build', 'status': 'passed', 'evidence': ['proof.log']}]}
            self.assertEqual(api.verify_project(p, state), [])
            state['checks'][0]['evidence'] = ['../outside.log']
            self.assertTrue(api.verify_project(p, state))
            state['checks'][0]['evidence'] = ['missing.log']
            self.assertTrue(api.verify_project(p, state))
            state['checks'][0]['evidence'] = ['proof.log']
            state['checks'][0]['status'] = 'failed'
            self.assertTrue(api.verify_project(p, state))
            state['checks'][0]['status'] = 'passed'
            state['ui_changed'] = True
            self.assertTrue(any('browser' in e for e in api.verify_project(p, state)))

    def test_manifest_is_pinned_and_complete(self):
        self.assertEqual(api.verify_manifest(), [])

    def test_manifest_has_complete_records_for_seven_upstreams_and_router(self):
        manifest = api.read_json(ROOT/'integrations/manifest.json')
        entries = manifest['integrations']
        self.assertEqual(len(entries), 8)
        self.assertEqual({item['id'] for item in entries}, api.INTEGRATION_IDS)
        required = {'repository', 'revision', 'localPath', 'license', 'integrationType',
                    'supportedAgents', 'technologies', 'triggers', 'dependencies',
                    'verificationStatus', 'updateMethod', 'rollbackMethod', 'evidencePath'}
        for item in entries:
            with self.subTest(integration=item['id']):
                self.assertTrue(required.issubset(item))
                self.assertRegex(item['revision'], r'^[0-9a-f]{40}$')
                self.assertTrue(set(item['supportedAgents']) <= {'claude', 'codex', 'opencode', 'antigravity'})

    def test_manifest_lock_and_evidence_are_consistent_without_external_checkouts(self):
        self.assertEqual(api.verify_integration_records(), [])

    def test_cli_verify_is_read_only_and_does_not_require_external_checkouts(self):
        result = subprocess.run(
            [sys.executable, str(ROOT/'scripts/integrations.py'), 'verify'],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertTrue(report['passed'])
        self.assertFalse(report['installed_checked'])

    def test_registered_skill_tree_hash_detects_content_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp)
            (path/'SKILL.md').write_text('name: example\n')
            (path/'notes.md').write_text('first')
            skill_hash, tree_hash = api.read_tree_hash(path)
            self.assertEqual(len(skill_hash), 64)
            self.assertEqual(len(tree_hash), 64)
            (path/'notes.md').write_text('changed')
            next_skill_hash, next_tree_hash = api.read_tree_hash(path)
            self.assertEqual(next_skill_hash, skill_hash)
            self.assertNotEqual(next_tree_hash, tree_hash)


if __name__ == '__main__':
    unittest.main()
