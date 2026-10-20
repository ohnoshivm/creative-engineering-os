#!/usr/bin/env python3
"""Sanitized installed-ecosystem catalog; Python stdlib only, no skill redistribution.

Reads SKILL.md, nearby license notices, local Git metadata, allowlisted plugin
manifest fields, and the two named Claude plugin registries. Never reads auth,
provider, MCP server, environment, backup, or skill support/data files. Output is
inventory metadata, not an installation lockfile. Use --verify-public-repos to
publish only GitHub origins independently accessible without authentication.
"""
from __future__ import annotations
import argparse
import collections
import concurrent.futures
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import urllib.error
import urllib.parse
import urllib.request

SKILL_ROOTS = [".claude/skills", ".agents/skills", ".codex/skills", ".config/opencode/skills", ".gemini/antigravity/skills"]
CACHE_ROOTS = [".claude/plugins/cache", ".codex/plugins/cache"]
SKIP = {".git", ".trash", "trash", "backup", "backups", "data", "node_modules", "__pycache__", ".cache", ".venv", "venv"}
META_PATHS = [".claude-plugin/plugin.json", ".codex-plugin/plugin.json", ".cursor-plugin/plugin.json", "plugin.json"]
LICENSE_NAMES = ["LICENSE", "LICENSE.md", "LICENSE.txt", "LICENSE-MIT", "LICENCE", "LICENCE.md", "COPYING", "COPYING.md"]
HEX = re.compile(r"^[0-9a-f]{7,64}$", re.I)
APP_ID = re.compile(r"app-[0-9a-f]{16,}", re.I)


def scalar(value, limit=180):
    if not isinstance(value, (str, int, float)) or isinstance(value, bool): return None
    s = str(value).strip()
    if not s or len(s) > limit or any(ord(c) < 32 for c in s): return None
    return s


def public_github(value):
    """Accept a public-host candidate; strip credentials, queries and fragments."""
    if isinstance(value, dict): value = value.get("url")
    if not isinstance(value, str): return None
    value = re.sub(r"^git@github\.com:", "https://github.com/", value)
    value = re.sub(r"^ssh://git@github\.com/", "https://github.com/", value)
    value = value.removeprefix("git+")
    try:
        u = urllib.parse.urlsplit(value)
        if u.hostname != "github.com": return None
        parts = u.path.strip("/").split("/")
        if len(parts) < 2: return None
        owner, repo = parts[:2]
        repo = repo.removesuffix(".git")
        if not all(re.fullmatch(r"[A-Za-z0-9_.-]+", x) for x in (owner, repo)): return None
        return "https://github.com/" + owner + "/" + repo
    except ValueError: return None


def allowed_dir(name):
    s = name.lower()
    return s not in SKIP and "backup" not in s and not s.startswith((".trash", ".bak"))


class Catalog:
    def __init__(self, home, bundle, verify):
        self.home, self.bundle, self.verify = home.resolve(), bundle.resolve(), verify
        self.issues = []
        self.git_cache, self.license_cache = {}, {}
        self.candidates, self.public = set(), {}
        self.packages, self.root_counts = {}, {}
        self.marketplaces = {}

    def path(self, p):
        try: s = "~/" + str(Path(p).relative_to(self.home))
        except ValueError: s = "<external-source>/" + Path(p).name
        return APP_ID.sub("app-<plugin-id>", s)

    def read_json(self, p):
        try:
            value = json.loads(p.read_text(encoding="utf-8"))
            return value if isinstance(value, dict) else {}
        except (OSError, ValueError):
            self.issues.append({"path": self.path(p), "kind": "metadata_unreadable"})
            return {}

    def walk(self, root):
        """Follow skill aliases, preserving each discovery path; prevent cycles."""
        def visit(p, ancestors):
            try:
                real = p.resolve(strict=True)
                if real in ancestors: return
                if any(not allowed_dir(part) for part in real.parts):
                    self.issues.append({"path": self.path(p), "kind": "excluded_alias_target"})
                    return
                entries = sorted(p.iterdir(), key=lambda x: x.name)
            except (OSError, RuntimeError):
                self.issues.append({"path": self.path(p), "kind": "directory_unreadable_or_broken_link"})
                return
            for child in entries:
                if child.name == "SKILL.md" and child.is_file(): yield child
                elif allowed_dir(child.name):
                    if child.is_dir(): yield from visit(child, ancestors | {real})
                    elif child.is_symlink() and not child.exists():
                        self.issues.append({"path": self.path(child), "kind": "broken_symlink"})
        if root.exists(): yield from visit(root, set())

    def git(self, directory):
        p = directory.resolve()
        # Stop at the home boundary: never inspect a home-directory repository.
        gitroot = next((x for x in [p, *p.parents] if x != self.home and (x / ".git").exists()), None)
        if gitroot is None: return None
        if gitroot in self.git_cache: return self.git_cache[gitroot]
        def run(*args):
            try:
                r = subprocess.run(["git", "-C", str(gitroot), *args], capture_output=True, text=True, timeout=5)
                return r.stdout.strip() if r.returncode == 0 else None
            except (OSError, subprocess.TimeoutExpired): return None
        origin = public_github(run("remote", "get-url", "origin"))
        commit = run("rev-parse", "HEAD")
        branch = scalar(run("symbolic-ref", "--quiet", "--short", "HEAD"))
        tag = scalar(run("describe", "--tags", "--exact-match", "HEAD"))
        result = {"repository": origin, "commit": commit if commit and HEX.fullmatch(commit) else None,
                  "ref": tag or branch, "evidence": "local_git", "checkout": self.path(gitroot),
                  "commit_scope": "checkout_HEAD_not_clean_tree_attestation"}
        if origin: self.candidates.add(origin)
        self.git_cache[gitroot] = result
        return result

    def header(self, data):
        text = data.decode("utf-8", errors="replace")
        if not text.startswith("---"): return {}
        parts = text.split("---", 2)
        if len(parts) < 3: return {}
        result = {}
        for line in parts[1].splitlines():
            m = re.match(r"^(name|license):\s*(.*?)\s*$", line)
            if m and m[2] not in {"|", ">", "|-", ">-"}:
                value = m[2].strip().strip("\"'")
                if scalar(value): result[m[1]] = value
        return result

    def licenses(self, p, header):
        result = []
        if header.get("license"):
            result.append({"label": header["license"], "evidence": "skill_frontmatter", "path": self.path(p)})
        real = p.resolve()
        parents = [real.parent, *list(real.parent.parents)[:4]]
        for folder in parents:
            if folder == self.home or folder == Path("/"): break
            if folder in self.license_cache: found = self.license_cache[folder]
            else:
                found = []
                for name in LICENSE_NAMES:
                    f = folder / name
                    if not f.is_file(): continue
                    try: text = f.read_text(encoding="utf-8", errors="replace")[:30000]
                    except OSError: continue
                    low = text.lower()
                    if "apache license" in low and "version 2.0" in low: label = "Apache-2.0"
                    elif "permission is hereby granted, free of charge" in low: label = "MIT-style notice"
                    elif "gnu affero general public license" in low: label = "AGPL notice; inspect version"
                    elif "gnu general public license" in low: label = "GPL notice; inspect version"
                    elif "unlicense" in low or "free and unencumbered software" in low: label = "Unlicense notice"
                    elif "creative commons" in low: label = "Creative Commons notice; inspect exact terms"
                    elif "redistribution and use in source and binary forms" in low: label = "BSD-style notice; inspect clauses"
                    elif "proprietary" in low: label = "Proprietary notice"
                    else: label = "License notice present; terms not classified"
                    found.append({"label": label, "evidence": "nearby_license_notice_not_scope_certification", "path": self.path(f)})
                self.license_cache[folder] = found
            if found:
                result.extend(found)
                break
        return result

    def load_registry(self):
        known = self.home / ".claude/plugins/known_marketplaces.json"
        if known.is_file():
            for name, record in self.read_json(known).items():
                if not isinstance(record, dict): continue
                source = record.get("source", {})
                if not isinstance(source, dict): continue
                repo = public_github("https://github.com/" + source["repo"]) if source.get("source") == "github" and isinstance(source.get("repo"), str) else public_github(source.get("url"))
                self.marketplaces[name] = repo
                if repo: self.candidates.add(repo)
        installed = self.home / ".claude/plugins/installed_plugins.json"
        records = []
        if installed.is_file():
            plugins = self.read_json(installed).get("plugins", {})
            if isinstance(plugins, dict):
                for key, values in plugins.items():
                    if not isinstance(key, str) or not isinstance(values, list): continue
                    name, _, market = key.partition("@")
                    for r in values:
                        if not isinstance(r, dict): continue
                        # Deliberately ignore scope, account/project IDs and timestamps.
                        install_path = r.get("installPath")
                        records.append({"name": scalar(name), "marketplace": scalar(market), "version": scalar(r.get("version")),
                            "commit": r.get("gitCommitSha") if isinstance(r.get("gitCommitSha"), str) and HEX.fullmatch(r["gitCommitSha"]) else None,
                            "_path": Path(install_path) if isinstance(install_path, str) else None})
        return records

    def package(self, root, provider, market, folder, cache_version):
        key = str(root)
        if key in self.packages: return self.packages[key]
        metadata = []
        for relative in META_PATHS:
            p = root / relative
            if p.is_file():
                d = self.read_json(p)
                manifest_name = scalar(d.get("name"))
                interface = d.get("interface") if isinstance(d.get("interface"), dict) else {}
                display_name = scalar(interface.get("displayName"))
                if manifest_name and APP_ID.fullmatch(manifest_name): manifest_name = display_name or "unnamed-plugin"
                metadata.append({"name": manifest_name, "version": scalar(d.get("version")),
                    "repository": public_github(d.get("repository")), "license": scalar(d.get("license")), "path": self.path(p)})
        name = next((d["name"] for d in metadata if d["name"]), None) or ("unnamed-plugin" if APP_ID.fullmatch(folder) else folder)
        version = next((d["version"] for d in metadata if d["version"]), None) or cache_version
        for d in metadata:
            if d["repository"]: self.candidates.add(d["repository"])
        marketrepo = self.marketplaces.get(market) if provider == "claude" else None
        item = {"id": "plugin-" + hashlib.sha256(key.encode()).hexdigest()[:16], "name": name,
            "provider": provider, "marketplace": market, "version": version, "cache_revision": cache_version,
            "discovery_location": self.path(root), "registration": "cache_present_activation_unverified",
            "registered_records": 0, "skill_discovery_count": 0, "metadata": metadata,
            "marketplace_repository": marketrepo, "git": self.git(root)}
        self.packages[key] = item
        return item

    def collect_packages(self):
        registry = self.load_registry()
        for rel in CACHE_ROOTS:
            base = self.home / rel
            if not base.exists(): continue
            provider = "claude" if rel.startswith(".claude/") else "codex"
            for market in sorted(base.iterdir()):
                if not market.is_dir() or not allowed_dir(market.name): continue
                for folder in sorted(market.iterdir()):
                    if not folder.is_dir() or not allowed_dir(folder.name): continue
                    for version in sorted(folder.iterdir()):
                        if version.is_dir() and allowed_dir(version.name):
                            self.package(version, provider, market.name, folder.name, version.name)
        for r in registry:
            match = self.packages.get(str(r["_path"])) if r["_path"] else None
            if match is None and r["_path"]:
                match = next((v for k,v in self.packages.items() if Path(k).resolve() == r["_path"].resolve()), None)
            if match:
                match["registration"] = "registered_installed"
                match["registered_records"] += 1
                if r["commit"]: match.setdefault("registry_commits", []).append(r["commit"])
            else:
                key = "registry:" + str(len(self.packages))
                marketrepo = self.marketplaces.get(r["marketplace"])
                self.packages[key] = {"id":"plugin-"+hashlib.sha256(key.encode()).hexdigest()[:16], "name":r["name"],
                    "provider":"claude", "marketplace":r["marketplace"], "version":r["version"],
                    "registration":"registered_cache_not_in_scanned_roots", "registered_records":1,
                    "discovery_location":"~/.claude/plugins/installed_plugins.json", "skill_discovery_count":0,
                    "metadata":[], "marketplace_repository":marketrepo, "git":None,
                    "registry_commits":[r["commit"]] if r["commit"] else []}
        return len(registry)

    def verify_sources(self):
        def check(repo):
            if not self.verify: return repo, False
            for attempt in range(2):
                try:
                    req = urllib.request.Request(repo, headers={"User-Agent":"Creative-Engineering-OS-catalog/1.0"})
                    with urllib.request.urlopen(req, timeout=15) as response:
                        target = public_github(response.url)
                        return repo, response.status == 200 and bool(target)
                except urllib.error.HTTPError as error:
                    if error.code not in {408, 429, 500, 502, 503, 504}: return repo, False
                except OSError:
                    pass
            return repo, False
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
            for repo, ok in pool.map(check, sorted(self.candidates)): self.public[repo] = ok

    def safe_source(self, source):
        if not source: return None
        if source.get("repository") and self.public.get(source["repository"]):
            return {**source, "public_repository_verified":True}
        # Do not publish private or unverified remote URL/branch names.
        return {"repository":None, "commit":source.get("commit"), "ref":None,
            "evidence":source.get("evidence"), "checkout":source.get("checkout"),
            "public_repository_verified":False, "limitation":"No independently verified public origin; candidate URL and ref withheld"}

    def collect(self):
        registry_count = self.collect_packages()
        discoveries = []
        for rel in SKILL_ROOTS + CACHE_ROOTS:
            root = self.home / rel
            count = 0
            for p in self.walk(root):
                try: data = p.read_bytes()
                except OSError:
                    self.issues.append({"path":self.path(p),"kind":"skill_unreadable"}); continue
                header = self.header(data)
                real = p.resolve()
                git = self.git(real.parent)
                package = None
                if rel in CACHE_ROOTS:
                    parts = p.relative_to(root).parts
                    if len(parts) >= 4: package = self.packages.get(str(root.joinpath(*parts[:3])))
                if package: package["skill_discovery_count"] += 1
                discoveries.append({"path":p,"canonical":real,"hash":hashlib.sha256(data).hexdigest(),"header":header,
                    "name":header.get("name") or p.parent.name,"folder":p.parent.name,"git":git,
                    "license":self.licenses(p,header),"plugin":package["id"] if package else None})
                count += 1
            self.root_counts["~/"+rel] = {"exists":root.exists(),"skill_discoveries":count}
        self.verify_sources()
        # Union by both canonical source and exact file bytes, preserving aliases.
        parent = list(range(len(discoveries)))
        def find(i):
            while parent[i] != i: parent[i] = parent[parent[i]]; i=parent[i]
            return i
        canonical, hashes = {}, {}
        for i,d in enumerate(discoveries):
            for mapping,key in [(canonical,str(d["canonical"])),(hashes,d["hash"])]:
                if key in mapping: parent[find(i)] = find(mapping[key])
                else: mapping[key] = i
        groups = collections.defaultdict(list)
        for i,d in enumerate(discoveries): groups[find(i)].append(d)
        skills = []
        for group in groups.values():
            names = sorted({x["name"] for x in group})
            sources = []
            for x in group:
                source = self.safe_source(x["git"])
                if source and source not in sources: sources.append(source)
            plugins = sorted({x["plugin"] for x in group if x["plugin"]})
            core = any(x["canonical"].is_relative_to(self.bundle/"skills") for x in group)
            pkg_sources = [p for p in self.packages.values() if p["id"] in plugins]
            for pkg in pkg_sources:
                for metadata in pkg["metadata"]:
                    if self.public.get(metadata["repository"]):
                        sources.append({"repository":metadata["repository"], "ref":None, "commit":None,
                            "evidence":"plugin_manifest", "source_scope":"plugin_declared_repository",
                            "plugin_package_id":pkg["id"], "public_repository_verified":True})
                if self.public.get(pkg["marketplace_repository"]):
                    sources.append({"repository":pkg["marketplace_repository"], "ref":None, "commit":None,
                        "evidence":"known_marketplace_registry", "source_scope":"distribution_origin_not_skill_authorship",
                        "plugin_package_id":pkg["id"], "public_repository_verified":True})
            sources = list({json.dumps(item,sort_keys=True):item for item in sources}.values())
            evidence = any(s.get("public_repository_verified") for s in sources) or any(
                any(self.public.get(m["repository"]) for m in p["metadata"] if m["repository"]) or self.public.get(p["marketplace_repository"]) for p in pkg_sources)
            licenses = []
            for x in group:
                for lic in x["license"]:
                    if lic not in licenses: licenses.append(lic)
            for pkg in pkg_sources:
                for m in pkg["metadata"]:
                    lic = {"label":m["license"],"evidence":"plugin_manifest_scope_requires_review","path":m["path"]}
                    if m["license"] and lic not in licenses: licenses.append(lic)
            skills.append({"id":"skill-"+min(x["hash"] for x in group)[:16],"name":names[0],"names":names,
                "folders":sorted({x["folder"] for x in group}),"sha256":sorted({x["hash"] for x in group}),
                "status":"bundled_core" if core else "upstream_install" if evidence else "provenance_unknown",
                "discovery_locations":sorted({self.path(x["path"]) for x in group}),
                "canonical_sources":sorted({self.path(x["canonical"]) for x in group}),
                "sources":sources,"plugin_package_ids":plugins,"license_evidence":licenses,
                "redistribution":"original_core_only" if core else "not_bundled_use_upstream_and_review_license"})
        skills.sort(key=lambda x:(x["name"].lower(),x["id"]))
        packages = []
        for p in self.packages.values():
            p["git"] = self.safe_source(p["git"])
            p["marketplace_repository"] = p["marketplace_repository"] if self.public.get(p["marketplace_repository"]) else None
            for m in p["metadata"]:
                m["repository_public_verified"] = bool(self.public.get(m["repository"]))
                if not m["repository_public_verified"]: m["repository"] = None
            p["registry_commits"] = sorted(set(p.get("registry_commits",[])))
            p["provenance_status"] = "upstream_install" if p["marketplace_repository"] or any(m["repository_public_verified"] for m in p["metadata"]) or (p["git"] and p["git"].get("public_repository_verified")) else "provenance_unknown"
            packages.append(p)
        packages.sort(key=lambda x:(x["provider"],x["name"],x.get("version") or "",x["id"]))
        date = datetime.date.today().isoformat()
        common = {"schema_version":1,"generated_on":date,"inventory_only":True,
            "privacy":{"paths":"Home-relative; opaque app identifiers replaced with app-<plugin-id>",
                "excluded":"Authors, accounts, install timestamps, auth/provider/MCP configuration, environment and credential data",
                "upstream_urls":"Only independently unauthenticated-public verified GitHub repository roots; no query strings or credentials"},
            "completeness":{"scope":"Seven named roots; reachable SKILL.md files including symlink aliases and historical plugin-cache versions; excludes trash/backup/data and dependency internals",
                "roots":self.root_counts,"issues":self.issues,"public_repository_checks":len(self.public),
                "public_repository_verified":sum(self.public.values()),"public_repository_unverified_or_unavailable":sum(not x for x in self.public.values())}}
        skilldoc = {**common,"summary":{"skill_discoveries":len(discoveries),"unique_skills":len(skills),
            "deduplicated_discoveries":len(discoveries)-len(skills),
            "distinct_declared_names":len({name for skill in skills for name in skill["names"]}),
            "distinct_canonical_files":len({str(d["canonical"]) for d in discoveries}),
            "status_counts":dict(collections.Counter(x["status"] for x in skills)),
            "without_license_evidence":sum(not x["license_evidence"] for x in skills),"with_license_evidence":sum(bool(x["license_evidence"]) for x in skills)},"skills":skills}
        plugdoc = {**common,"summary":{"plugin_packages":len(packages),"registered_install_records":registry_count,
            "distinct_plugin_names":len({p["name"] for p in packages}),
            "registered_plugin_names":len({p["name"] for p in packages if p["registered_records"]}),
            "cache_package_entries":sum("cache_revision" in p for p in packages),
            "registered_package_entries":sum(p["registration"]=="registered_installed" for p in packages),
            "cache_activation_unverified_entries":sum(p["registration"]=="cache_present_activation_unverified" for p in packages),
            "provenance_counts":dict(collections.Counter(p["provenance_status"] for p in packages))},"plugins":packages}
        return skilldoc,plugdoc


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home",type=Path,default=Path.home(),help="Inventory root; defaults to current user's home")
    parser.add_argument("--bundle-root",type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output-dir",type=Path,default=Path(__file__).resolve().parents[1]/"manifests")
    parser.add_argument("--verify-public-repos",action="store_true",help="Unauthenticated HTTPS checks; no credentials or APIs")
    args=parser.parse_args()
    skills,plugins=Catalog(args.home,args.bundle_root,args.verify_public_repos).collect()
    args.output_dir.mkdir(parents=True,exist_ok=True)
    for name,doc in [("ecosystem-skills.json",skills),("ecosystem-plugins.json",plugins)]:
        content=json.dumps(doc,indent=2,ensure_ascii=False)+"\n"
        if str(args.home.resolve()) in content or re.search(r"/Users/[^/]+/",content):
            raise SystemExit("Refusing to write inventory containing an absolute home path")
        (args.output_dir/name).write_text(content,encoding="utf-8")
    print(json.dumps({"skills":skills["summary"],"plugins":plugins["summary"],"issues":len(skills["completeness"]["issues"])}))

if __name__=="__main__":main()
