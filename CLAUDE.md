# Creative Engineering OS

This repo is the reusable local toolkit, not the Pixelard website. Read SYSTEM.md, standards/STANDARD.md and the scoped task artifact. Use the relevant ceos specialist skill. Existing user/project instructions and host tool permissions take precedence.

Keep dependencies pinned and scoped to tooling/templates/demo. Never open or print backups, auth files, provider config values or environment dumps. Client configs are outside the repo; change only owned additions after private backup and semantic preservation checks.

One integration owner and explicit paths per specialist. Use native/T3 child APIs supported by the host; never launch top-level conversations as substitutes. Tests exercise production previews, not only development. Inspect real images, report unverified checks honestly, preserve baseline history.

Local health: scripts/verify.sh; python3 tests/scripts.test.py; node --test tests/mirror.test.mjs. Template build/smoke/visual commands are in each README. Run GPU/performance jobs sequentially on a quiet machine.
