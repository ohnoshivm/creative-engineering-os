#!/bin/zsh
# Read-only structural health checks. Optional builds/tests are separate and explicit.
set -euo pipefail
OS=${0:A:h:h}
python3 -I "$OS/tests/verify-structure.py"
for tool in node npm git bun playwright-cli lighthouse blender; do
  if command -v "$tool" >/dev/null 2>&1; then echo "FOUND $tool: $(command -v "$tool")"
  else echo "MISSING $tool"; fi
done
