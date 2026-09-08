import net from 'node:net';
const endpoints = [];
if (process.env.DATABASE_URL) {
  const db = new URL(process.env.DATABASE_URL);
  endpoints.push([db.hostname, Number(db.port || 5432)]);
}
if (process.env.REDIS_SERVER_HOST) endpoints.push([process.env.REDIS_SERVER_HOST, Number(process.env.REDIS_SERVER_PORT || 6379)]);
for (const [host, port] of endpoints) {
  const deadline = Date.now() + 180_000;
  let connected = false;
  while (Date.now() < deadline) {
    connected = await new Promise(resolve => {
      const socket = net.createConnection({ host, port });
      const done = value => { socket.destroy(); resolve(value); };
      socket.setTimeout(3000, () => done(false));
      socket.once('error', () => done(false));
      socket.once('connect', () => done(true));
    });
    if (connected) break;
    await new Promise(resolve => setTimeout(resolve, 2000));
  }
  if (!connected) throw new Error(`Dependency on port ${port} did not become reachable`);
}
