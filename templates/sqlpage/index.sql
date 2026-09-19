select 'shell' as component, 'My SQL application' as title;
select 'text' as component;
select 'Edit /data/www/index.sql to build your application. The SQLite database is stored at /data/app.db.' as contents;
select 'table' as component;
select sqlite_version() as sqlite_version, datetime('now') as server_utc;
