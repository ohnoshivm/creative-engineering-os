#!/bin/zsh
# Rollback: remove only symlinks that point into ~/creative-engineering-os/skills.
set -uo pipefail
OS=${0:A:h:h}
for t in "$HOME/.claude/skills" "$HOME/.agents/skills" "$HOME/.gemini/antigravity/skills"; do
  for l in $t/ceos-*(N@); do
    [[ $(readlink "$l") == $OS/skills/* ]] && rm "$l" && echo "removed $l"
  done
done
