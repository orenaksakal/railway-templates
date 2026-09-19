import upstream from './upstream-config.js';

export default {
  ...upstream,
  site_title: process.env.SITE_TITLE || 'My Knowledge Base',
  base_url: process.env.PUBLIC_URL,
  nowrap: true,
  content_dir: '/data/pages',
  secret: process.env.SESSION_SECRET,
  authentication: true,
  authentication_for_read: true,
  authentication_for_edit: true,
  allow_editing: true,
  credentials: [{username: process.env.RANETO_USERNAME, password: process.env.RANETO_PASSWORD}],
};
