#!/bin/zsh
# Add owned skill links; never overwrite foreign links or real directories.
set -euo pipefail
OS=${0:A:h:h}
targets=("$HOME/.claude/skills" "$HOME/.agents/skills" "$HOME/.gemini/antigravity/skills")
(( $# == 0 )) || targets=("$@")
for t in "$targets[@]"; do
  mkdir -p "$t"
  for s in "$OS"/skills/ceos-*(/); do
    dst="$t/${s:t}"
    if [[ -L "$dst" ]]; then
      if [[ "$(readlink "$dst")" == "$s" ]]; then echo "unchanged $dst"
      else echo "SKIPPED (foreign link): $dst"; fi
    elif [[ -e "$dst" ]]; then echo "SKIPPED (existing path): $dst"
    else ln -s "$s" "$dst"; echo "linked $dst"; fi
  done
done
