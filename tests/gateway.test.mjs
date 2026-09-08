import { test } from 'node:test';
import assert from 'node:assert/strict';
import http from 'node:http';
import { once } from 'node:events';
import { createGateway } from '../templates/firecrawl/gateway.mjs';

test('gateway rejects missing/incorrect credentials and keeps non-API routes private', async t => {
  const seen = [];
  const upstream = http.createServer((req, res) => {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', () => {
      seen.push({ url: req.url, auth: req.headers.authorization, body });
      res.setHeader('content-type', 'application/json');
      res.end(JSON.stringify({ success: true, path: req.url, body }));
    });
  }).listen(0, '127.0.0.1');
  await once(upstream, 'listening');
  const key = 'f'.repeat(64);
  const gateway = createGateway({ apiKey: key, upstream: `http://127.0.0.1:${upstream.address().port}` }).listen(0, '127.0.0.1');
  await once(gateway, 'listening');
  t.after(() => { gateway.closeAllConnections(); gateway.close(); upstream.closeAllConnections(); upstream.close(); });
  const base = `http://127.0.0.1:${gateway.address().port}`;
  assert.equal((await fetch(base + '/v2/scrape')).status, 401);
  assert.equal((await fetch(base + '/v2/scrape', { headers: { authorization: 'Bearer wrong' } })).status, 401);
  assert.equal(seen.length, 0);
  const auth = { authorization: `Bearer ${key}`, 'content-type': 'application/json' };
  assert.equal((await fetch(base + '/admin', { headers: auth })).status, 404);
  for (const path of ['/v2/%2e%2e%2fadmin', '/v2/%252e%252e/admin', '/v2/%5cadmin']) {
    assert.equal((await fetch(base + path, { headers: auth })).status, 404);
  }
  const result = await fetch(base + '/v2/scrape?test=1', { method: 'POST', headers: auth, body: '{"url":"https://example.com"}' });
  assert.equal(result.status, 200);
  assert.equal((await result.json()).body, '{"url":"https://example.com"}');
  assert.equal(seen[0].auth, undefined, 'gateway secret must not reach the unauthenticated upstream');
  assert.equal((await fetch(base + '/healthz')).status, 200);
  assert.equal((await fetch(base + '/healthz?bypass=true')).status, 401);
});

test('gateway refuses weak keys and non-private transport configurations', () => {
  assert.throws(() => createGateway({ apiKey: 'short', upstream: 'http://localhost:3002' }));
  assert.throws(() => createGateway({ apiKey: 'f'.repeat(64), upstream: 'https://localhost:3002' }));
});
