import { spawn } from 'node:child_process';
import http from 'node:http';

// Hub's migrations depend on Formbricks tables. Railway has no Compose depends_on.
// This private listener reports readiness only after application migrations finish.
let migrated = false;
let child;
const coordinator = http.createServer((req, res) => {
  res.writeHead(req.url === '/migrations' && migrated ? 200 : 503);
  res.end(migrated ? 'ready' : 'migrating');
});
coordinator.listen(3001, '::');
const run = (args) => new Promise((resolve, reject) => {
  child = spawn('node', args, { stdio: 'inherit' });
  child.once('error', reject);
  child.once('exit', code => code === 0 ? resolve() : reject(new Error(`Initialization exited ${code}`)));
});
for (const signal of ['SIGTERM', 'SIGINT']) process.on(signal, () => {
  child?.kill(signal);
  coordinator.close();
  setTimeout(() => process.exit(0), 1000).unref();
});
try {
  await run(['/home/nextjs/wait-for-dependencies.mjs']);
  await run(['/home/nextjs/validate-env.mjs']);
  await run(['packages/database/dist/scripts/apply-migrations.js']);
  migrated = true;
  const deadline = Date.now() + 300_000;
  let ready = false;
  while (Date.now() < deadline) {
    try {
      const response = await fetch(`${process.env.HUB_API_URL}/health`, { signal: AbortSignal.timeout(5000) });
      if (response.ok) { ready = true; break; }
    } catch {}
    await new Promise(resolve => setTimeout(resolve, 2000));
  }
  if (!ready) throw new Error('Hub did not become healthy within five minutes');
  await run(['packages/database/dist/scripts/create-saml-database.js']);
  child = spawn('node', ['apps/web/server.js'], { stdio: 'inherit' });
  child.once('error', error => { console.error(error.message); process.exit(1); });
  child.once('exit', code => { coordinator.close(); process.exit(code ?? 1); });
} catch (error) {
  console.error(error.message);
  coordinator.close();
  process.exit(1);
}
