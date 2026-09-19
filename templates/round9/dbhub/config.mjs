export function buildConfig(dsn) {
  if (!dsn) throw new Error('DSN is required; use a database-level read-only account');
  if (/[\x00-\x1f\x7f]/.test(dsn)) throw new Error('DSN contains control characters');
  return `[[sources]]
id = "default"
dsn = ${JSON.stringify(dsn)}

[[tools]]
name = "execute_sql"
source = "default"
readonly = true
max_rows = 1000

[[tools]]
name = "search_objects"
source = "default"
`;
}
