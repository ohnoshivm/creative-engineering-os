# Claude Code plugin

This repository is both a portable studio bundle and a Claude Code plugin marketplace. The plugin uses documented Claude conventions; it is not a cross-client plugin binary.

In Claude Code2.1.275+:

```text
/plugin install creative-engineering-os --marketplace ohnoshivm/creative-engineering-os
```

Or in a terminal:

```sh
claude plugin marketplace add ohnoshivm/creative-engineering-os
claude plugin install creative-engineering-os@creative-engineering-os
```

Start `/creative-engineering-os:ceos-studio-workflow`. The plugin ships13 skills, creative-auditor and isolated/headless Chrome DevTools MCP1.11.0 with usage-statistics/CrUX requests disabled. It adds no startup hooks, model defaults, account providers or paid-service registration. Read-only auditor tools are restricted; the integration owner supplies captures and saves reports. Tool permissions are not an OS sandbox.

For templates and shared scripts, keep a normal checkout at ~/creative-engineering-os and install its local dependencies. A plugin cache is maintained by the client, so new projects belong outside it. The plugin's files can be located through its resolved plugin root; in commands/hooks Claude supports `${CLAUDE_PLUGIN_ROOT}`. Core skill examples use the standard home checkout; when using another location, resolve paths against the checked-out bundle root instead of copying machine-specific paths.

Use `claude --plugin-dir /path/to/checkout` for a local development session. Validate with `claude plugin validate /path/to/checkout --strict`. Restart/reload plugins after updates. Do not install manual Claude core links or another chrome-devtools definition if using the plugin copy; keep other clients' independent adapters as needed.

Third-party plugins from the ecosystem catalogue are installed separately from their publishers. They are not dependencies force-enabled by this plugin. Marketplace version1.0.0 pins the studio release metadata; npm/CLI dependencies have their own pins. Review updates, re-run tests and compare screenshots before upgrading a production project.

Official reference: https://code.claude.com/docs/en/plugins-reference and https://code.claude.com/docs/en/plugin-marketplaces .
