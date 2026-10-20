import fs from 'node:fs';
import path from 'node:path';
// Resolve only regular, nonempty files beneath a mirror, including after following symlinks.
export function mirrorFile(directory, url) {
  try {
    const root = fs.realpathSync(directory);
    const candidate = path.resolve(root, url.hostname, '.' + decodeURIComponent(url.pathname));
    const contained = p => p.startsWith(root + path.sep);
    if (!contained(candidate)) return null;
    const real = fs.realpathSync(candidate);
    if (!contained(real)) return null;
    const stat = fs.statSync(real);
    return stat.isFile() && stat.size > 0 ? real : null;
  } catch { return null; }
}
