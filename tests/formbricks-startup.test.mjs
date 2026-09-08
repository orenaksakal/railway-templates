import assert from 'node:assert/strict';
import { mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import test from 'node:test';

const exec = promisify(execFile);
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const startup = process.env.FORMBRICKS_START_SCRIPT || path.join(root, 'templates/formbricks/start.mjs');

async function runStartup(failStep) {
  const directory = await mkdtemp(path.join(tmpdir(), 'formbricks-startup-'));
  const events = path.join(directory, 'events.jsonl');
  const preload = path.join(directory, 'preload.mjs');
  try {
    await writeFile(preload, `
      import childProcess from 'node:child_process';
      import { syncBuiltinESMExports } from 'node:module';
      import { EventEmitter } from 'node:events';
      import { appendFileSync } from 'node:fs';
      const record = event => appendFileSync(process.env.TEST_EVENTS, JSON.stringify(event) + '\\n');
      childProcess.spawn = (command, args) => {
        record(args[0]);
        const child = new EventEmitter();
        child.kill = () => {};
        setImmediate(() => child.emit('exit', args[0] === process.env.TEST_FAIL_STEP ? 1 : 0));
        return child;
      };
      syncBuiltinESMExports();
      globalThis.fetch = async url => { record(url); return { ok: true }; };
    `);
    let code = 0;
    try {
      await exec(process.execPath, ['--import', preload, startup], {
        env: { ...process.env, HUB_API_URL: 'http://hub.invalid:8080', TEST_EVENTS: events, TEST_FAIL_STEP: failStep || '' },
        timeout: 5000,
      });
    } catch (error) {
      code = error.code;
    }
    return { code, events: (await readFile(events, 'utf8')).trim().split('\n').map(JSON.parse) };
  } finally {
    await rm(directory, { recursive: true, force: true });
  }
}

test('application publishes migration completion before waiting for Hub and launching web', async () => {
  const result = await runStartup();
  assert.equal(result.code, 0);
  assert.deepEqual(result.events, [
    '/home/nextjs/wait-for-dependencies.mjs',
    '/home/nextjs/validate-env.mjs',
    'packages/database/dist/scripts/apply-migrations.js',
    '/home/nextjs/record-migrations.mjs',
    'http://hub.invalid:8080/health',
    'packages/database/dist/scripts/create-saml-database.js',
    'apps/web/server.js',
  ]);
});

test('failed upstream migrations never publish readiness or launch web', async () => {
  const result = await runStartup('packages/database/dist/scripts/apply-migrations.js');
  assert.equal(result.code, 1);
  assert.equal(result.events.at(-1), 'packages/database/dist/scripts/apply-migrations.js');
  assert.ok(!result.events.includes('/home/nextjs/record-migrations.mjs'));
});

test('failed migration publication never starts Hub polling or launches web', async () => {
  const result = await runStartup('/home/nextjs/record-migrations.mjs');
  assert.equal(result.code, 1);
  assert.equal(result.events.at(-1), '/home/nextjs/record-migrations.mjs');
});

test('shared migration release matches the exact pinned application image', async () => {
  const dockerfile = await readFile(path.join(root, 'templates/formbricks/Dockerfile'), 'utf8');
  const release = (await readFile(path.join(root, 'templates/formbricks/migration-version'), 'utf8')).trim();
  assert.equal(dockerfile.split('\n')[0], `FROM ghcr.io/formbricks/formbricks:${release}`);
});
