import type { Config, PartialDeep } from './lib/types.ts';
const config: PartialDeep<Config> = {
  auth: { baseUrl: Deno.env.get('PUBLIC_URL')!, allowSignups: false, enableEmailVerification: false },
  core: {enabledApps: ['dashboard', 'files', 'news', 'notes', 'photos', 'expenses']},
  files: {allowPublicSharing: false},
};
export default config;
