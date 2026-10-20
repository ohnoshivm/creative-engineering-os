# Publication and installation boundaries

Public archives use an allowlist. They exclude account/auth files, environment values, API headers/URLs from personal MCP configs, provider routing, private backups, app databases, package caches, node_modules, raw personal installation reports and original private Git history. Ecosystem records expose names/provenance/versions only; they are not an account backup.

The portable installer plans by default, preserves existing files/entries, backs up only the configs it changes privately and adds one reviewed credential-free diagnostic server. It never signs into a vendor, installs a paid plan or changes models. Refusing to overwrite an existing path is intentional; resolve conflicting installations with their owner.

Skills/MCPs/plugins and npm install scripts can execute actions as the user. Inspect source, licenses and lockfile changes. Chrome uses an isolated temporary profile; this does not sandbox the filesystem or make untrusted pages safe. Diagnostic captures/HARs may hold private content; keep them out of public repos. No public install command includes account secrets.

Production browser checks use a real installed browser. Visual baselines are evidence for a specific environment, not a universal render guarantee. Physical-device GPU, Safari/Firefox, field CWV/INP, hosted response headers and deployment rollback require project-specific verification.

Report issues through GitHub without including credentials or private captures. If a credential was exposed, revoke it with its vendor; publishing a sanitized package does not rotate old credentials.
