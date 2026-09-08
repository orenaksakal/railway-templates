import { readFile } from 'node:fs/promises';
import pg from 'pg';

// This file is shared with Hub and must match the pinned application image.
// Only successful upstream migration completion is allowed to publish it.
let client;
try {
  if (!process.env.DATABASE_URL) throw new Error('Missing database URL');
  const release = (await readFile(new URL('./migration-version', import.meta.url), 'utf8')).trim();
  if (!release) throw new Error('Missing migration release');
  client = new pg.Client({
    connectionString: process.env.DATABASE_URL,
    connectionTimeoutMillis: 5000,
    statement_timeout: 5000,
    application_name: 'railway-formbricks-bootstrap',
  });
  await client.connect();
  await client.query(`
    CREATE TABLE IF NOT EXISTS public.railway_template_migrations (
      component text PRIMARY KEY,
      release text NOT NULL,
      completed_at timestamptz NOT NULL DEFAULT now()
    )
  `);
  await client.query(`
    INSERT INTO public.railway_template_migrations (component, release)
    VALUES ('formbricks', $1)
    ON CONFLICT (component) DO UPDATE
      SET release = EXCLUDED.release, completed_at = now()
  `, [release]);
  console.log('Formbricks migration completion recorded');
} catch {
  // Driver errors may contain connection details; keep credentials out of logs.
  console.error('Could not record Formbricks migration completion');
  process.exitCode = 1;
} finally {
  await client?.end();
}
