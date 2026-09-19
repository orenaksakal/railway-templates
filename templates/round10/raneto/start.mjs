import fs from 'node:fs';

for (const key of ['PUBLIC_URL', 'SESSION_SECRET', 'RANETO_USERNAME', 'RANETO_PASSWORD']) {
  if (!process.env[key]) throw new Error(`Required variable ${key} is missing`);
}
if (process.env.SESSION_SECRET.length < 32) throw new Error('SESSION_SECRET must be at least 32 characters');
for (const path of ['/data', '/data/pages', '/data/pages/images', '/data/sessions']) {
  fs.mkdirSync(path, {recursive: true});
  fs.chownSync(path, 1000, 1000);
}
try {
  fs.writeFileSync('/data/pages/index.md', 'Title: My Knowledge Base\n\nWelcome. Sign in and edit this page to start your private knowledge base.\n', {flag: 'wx'});
  fs.chownSync('/data/pages/index.md', 1000, 1000);
} catch (error) {
  if (error.code !== 'EEXIST') throw error;
}
// The upstream file-session store is relative to the process working directory.
process.chdir('/data');
process.setgroups([]);
process.setgid(1000);
process.setuid(1000);
await import('/opt/raneto/server.js');
