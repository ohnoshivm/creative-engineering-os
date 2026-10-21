#!/bin/zsh
# Read-only structural health checks. Optional builds/tests are separate and explicit.
set -euo pipefail
installed=0
if [[ $# -gt 1 || ( $# -eq 1 && $1 != --installed ) ]]; then
  print -u2 'Usage: scripts/verify.sh [--installed]'
  exit 2
fi
if [[ $# -eq 1 ]]; then installed=1; fi
OS=${0:A:h:h}
python3 -I "$OS/tests/verify-structure.py"
if (( installed )); then
  python3 -I "$OS/scripts/integrations.py" verify --installed
else
  python3 -I "$OS/scripts/integrations.py" verify
fi
for tool in node npm git bun playwright-cli lighthouse blender; do
  if command -v "$tool" >/dev/null 2>&1; then echo "FOUND $tool: $(command -v "$tool")"
  else echo "MISSING $tool"; fi
done
