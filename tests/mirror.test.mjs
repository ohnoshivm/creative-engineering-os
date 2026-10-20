import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { mirrorFile } from '../tooling/lib/safe-mirror.mjs';
test('mirror permits intended files and rejects traversal, missing files and symlink escapes', () => {
  const temporary = fs.mkdtempSync(path.join(os.tmpdir(), 'ceos-mirror-'));
  try {
    const root = path.join(temporary, 'mirror'); fs.mkdirSync(path.join(root, 'example.com'), { recursive:true });
    const file = path.join(root, 'example.com', 'asset'); fs.writeFileSync(file, 'ok');
    const secret = path.join(temporary, 'private'); fs.writeFileSync(secret, 'private');
    assert.equal(mirrorFile(root, new URL('https://example.com/asset')), fs.realpathSync(file));
    assert.equal(mirrorFile(root, new URL('https://example.com/missing')), null);
    assert.equal(mirrorFile(root, new URL('https://example.com/..%2f..%2fprivate')), null);
    fs.symlinkSync(secret, path.join(root, 'example.com', 'link'));
    assert.equal(mirrorFile(root, new URL('https://example.com/link')), null);
    assert.equal(mirrorFile(root, new URL('https://example.com/%zz')), null);
  } finally { fs.rmSync(temporary, { recursive:true, force:true }); }
});
