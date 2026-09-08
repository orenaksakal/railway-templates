import { spawn } from 'node:child_process';

// Publish completed migrations through PostgreSQL before waiting for Hub. Hub
// must not depend on this service's DNS or HTTP readiness during deployment.
let child;
const run = (args) => new Promise((resolve, reject) => {
  child = spawn('node', args, { stdio: 'inherit' });
  child.once('error', reject);
  child.once('exit', code => code === 0 ? resolve() : reject(new Error(`Initialization exited ${code}`)));
});
for (const signal of ['SIGTERM', 'SIGINT']) process.on(signal, () => {
  child?.kill(signal);
  setTimeout(() => process.exit(0), 1000).unref();
});
try {
  await run(['/home/nextjs/wait-for-dependencies.mjs']);
  await run(['/home/nextjs/validate-env.mjs']);
  await run(['packages/database/dist/scripts/apply-migrations.js']);
  await run(['/home/nextjs/record-migrations.mjs']);
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
  child.once('exit', code => process.exit(code ?? 1));
} catch (error) {
  console.error(error.message);
  process.exit(1);
}
