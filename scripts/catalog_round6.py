"""Fifteen independently generated Railway drafts; never mutate released catalogs."""
import json
from pathlib import Path
import uuid
import catalog_round3 as base

ROOT = Path(__file__).resolve().parents[1]
BRANCH = 'codex/fifteen-template-drafts'
LOCK_PATH = ROOT / 'images.round6.lock.json'
LOCK = json.loads(LOCK_PATH.read_text()) if LOCK_PATH.exists() else {}
secret, ref, private, public = base.secret, base.ref, base.private, base.public

def svc(name, **kw):
    if kw.get('image'):
        kw['image'] = LOCK.get(kw['image'], kw['image'])
    s = base.svc(name, **kw)
    if s['source'].get('repo'):
        s['source']['branch'] = BRANCH
    return s

def optional(service, **values):
    for key, description in values.items():
        service['variables'][key] = {'isOptional': True, 'description': description}
    return service

def pg(app, image='postgres:17-alpine', name='postgres', dockerfile=None):
    spec = {'dockerfile': dockerfile} if dockerfile else {'image': image}
    env = {'POSTGRES_USER': app, 'POSTGRES_DB': app, 'POSTGRES_PASSWORD': secret(),
           'PGDATA': '/var/lib/postgresql/data/pgdata', 'PGPORT': 5432,
           'DATABASE_URL': 'postgresql://'+app+':'+ref(name,'POSTGRES_PASSWORD')+'@'+ref(name,'RAILWAY_PRIVATE_DOMAIN')+':5432/'+app}
    return svc(name, **spec, env=env, volume='/var/lib/postgresql/data')

def redis():
    return base.redis()

def edge(name, target, port, owner=True, password=None, extra=None):
    env = {'UPSTREAM_HOST': ref(target,'RAILWAY_PRIVATE_DOMAIN'), 'UPSTREAM_PORT': port,
           'OWNER_AUTH': str(owner).lower()}
    if owner: env['ACCESS_PASSWORD'] = password or secret()
    env.update(extra or {})
    return svc(name, dockerfile='shared/round6-gateway/Dockerfile', env=env, port=8080, health='/healthz')

def plunk():
    store=svc('storage',dockerfile='shared/round6-storage/Dockerfile',env={
        'MINIO_ROOT_USER':secret(20),'MINIO_ROOT_PASSWORD':secret(),'S3_BUCKETS':'uploads',
        'PUBLIC_BUCKET':('uploads','Public email-image bucket. Do not upload confidential files; only this bucket allows anonymous reads.')},volume='/data',port=9000)
    env={'SERVICE':'all','NODE_ENV':'production','NGINX_PORT':80,
         'DATABASE_URL':ref('postgres','DATABASE_URL'),'DIRECT_DATABASE_URL':ref('postgres','DATABASE_URL'),
         'REDIS_URL':ref('redis','REDIS_URL'),'JWT_SECRET':secret(),'USE_HTTPS':'true',
         'API_DOMAIN':ref('plunk','RAILWAY_PUBLIC_DOMAIN'),'DASHBOARD_DOMAIN':'dashboard.internal.invalid',
         'API_URI':public('plunk')+'/api','DASHBOARD_URI':public('plunk'),
         'LANDING_DOMAIN':ref('landing','RAILWAY_PUBLIC_DOMAIN'),'WIKI_DOMAIN':ref('docs','RAILWAY_PUBLIC_DOMAIN'),
         'AWS_SES_REGION':(None,'Required region of your configured AWS SES account.'),
         'AWS_SES_ACCESS_KEY_ID':(None,'Required operator-owned SES access key. Never use a template author credential.'),
         'AWS_SES_SECRET_ACCESS_KEY':None,'SES_CONFIGURATION_SET':(None,'Required SES configuration set with the SNS callback described below.'),
         'S3_ENDPOINT':private('storage',9000),'S3_ACCESS_KEY_ID':ref('storage','MINIO_ROOT_USER'),
         'S3_ACCESS_KEY_SECRET':ref('storage','MINIO_ROOT_PASSWORD'),'S3_BUCKET':'uploads',
         'S3_PUBLIC_URL':public('storage')+'/uploads','S3_FORCE_PATH_STYLE':'true','NTFY_URL':'',
         'DISABLE_SIGNUPS':('false','Owner gateway protects registration. After creating your account, set true to close new registrations.'),
         'AUTO_PROJECT_DISABLE':'false'}
    app=svc('core',dockerfile='templates/plunk/Dockerfile',env=env,volume='/app/data')
    owner=svc('plunk',dockerfile='templates/plunk/Gateway.Dockerfile',env={
        'UPSTREAM_HOST':ref('core','RAILWAY_PRIVATE_DOMAIN'),'UPSTREAM_PORT':3000,
        'OWNER_AUTH':'true','ACCESS_PASSWORD':secret()},port=8080,health='/healthz')
    return [pg('plunk',image='postgres:16-alpine'),redis(),store,app,owner,
            edge('landing','core',80,password=ref('plunk','ACCESS_PASSWORD')),
            edge('docs','core',80,password=ref('plunk','ACCESS_PASSWORD'))]

def bugsink():
    db=svc('mysql',image='mysql:8.4',env={'MYSQL_DATABASE':'bugsink','MYSQL_USER':'bugsink',
        'MYSQL_PASSWORD':secret(),'MYSQL_ROOT_PASSWORD':secret()},volume='/var/lib/mysql')
    app=svc('bugsink',image='bugsink/bugsink:2.5.1',env={
        'PORT':8000,'SECRET_KEY':secret(),'ADMIN_EMAIL':(None,'Required administrator email for first startup.'),
        'ADMIN_PASSWORD':secret(),'CREATE_SUPERUSER':ref('bugsink','ADMIN_EMAIL')+':'+ref('bugsink','ADMIN_PASSWORD'),
        'DATABASE_URL':'mysql://bugsink:'+ref('mysql','MYSQL_PASSWORD')+'@'+ref('mysql','RAILWAY_PRIVATE_DOMAIN')+':3306/bugsink',
        'BASE_URL':public('bugsink'),'BEHIND_HTTPS_PROXY':'true','USE_X_REAL_IP':'false','USER_REGISTRATION':'CB_ADMINS',
        'PHONEHOME':'false','MAX_EVENT_AGE_DAYS':30,'MAX_RETENTION_EVENT_COUNT':100000,
        'SNAPPEA_NUM_WORKERS':2},port=8000,health='/health/ready')
    optional(app,EMAIL_HOST='Optional SMTP server for invitations and alerts.',EMAIL_HOST_USER='SMTP username.',
             EMAIL_HOST_PASSWORD='SMTP password.',DEFAULT_FROM_EMAIL='Verified sender email.')
    return [db,app]

def notifuse():
    app=svc('core',image='notifuse/notifuse:v40.0',env={
        'SERVER_PORT':8080,'SERVER_HOST':'0.0.0.0','ENVIRONMENT':'production','DB_HOST':ref('postgres','RAILWAY_PRIVATE_DOMAIN'),
        'DB_PORT':5432,'DB_USER':'notifuse','DB_PASSWORD':ref('postgres','POSTGRES_PASSWORD'),
        'DB_PREFIX':'notifuse','DB_NAME':'notifuse_system','DB_SSLMODE':'disable','SECRET_KEY':secret(),
        'ROOT_EMAIL':(None,'Required operator email. Complete the protected initial setup with this address.'),
        'API_ENDPOINT':public('notifuse'),'SMTP_BRIDGE_ENABLED':'false'},volume='/app/data')
    optional(app,SMTP_HOST='SMTP server for login/setup email.',SMTP_PORT='SMTP port, usually 587.',SMTP_USERNAME='SMTP username.',SMTP_PASSWORD='SMTP password.',SMTP_FROM_EMAIL='Verified sender address.',NOTIFUSE_LICENSE_KEY='Optional paid upstream license; no license is included.')
    return [pg('notifuse'),app,edge('notifuse','core',8080,extra={'OWNER_SCOPE':'setup'})]

def lago():
    env={'DATABASE_URL':ref('postgres','DATABASE_URL'),'REDIS_URL':ref('redis','REDIS_URL'),
        'REDIS_PASSWORD':ref('redis','REDIS_PASSWORD'),'LAGO_REDIS_CACHE_URL':ref('redis','REDIS_URL'),
        'LAGO_REDIS_CACHE_PASSWORD':ref('redis','REDIS_PASSWORD'),'RAILS_ENV':'production','RAILS_LOG_TO_STDOUT':'true',
        'SECRET_KEY_BASE':secret(),'LAGO_ENCRYPTION_PRIMARY_KEY':secret(32),'LAGO_ENCRYPTION_DETERMINISTIC_KEY':secret(32),
        'LAGO_ENCRYPTION_KEY_DERIVATION_SALT':secret(32),'LAGO_FRONT_URL':public('lago'),'LAGO_API_URL':public('api'),
        'LAGO_PDF_URL':private('pdf',3000),'LAGO_USE_AWS_S3':'false','LAGO_DISABLE_SEGMENT':'true',
        'LAGO_SIDEKIQ_WEB':'false','LAGO_DISABLE_SIGNUP':'true','LAGO_CREATE_ORG':'true',
        'LAGO_ORG_NAME':'My organization','LAGO_ORG_USER_EMAIL':(None,'Required first organization administrator email.'),
        'LAGO_ORG_USER_PASSWORD':secret(),'LAGO_ORG_API_KEY':secret(),'PORT':3000}
    app=svc('api',dockerfile='templates/lago/Dockerfile',env=env,volume='/data',port=3000,health='/health')
    optional(app,LAGO_SMTP_ADDRESS='SMTP host for invoices and account emails.',LAGO_SMTP_USERNAME='SMTP username.',LAGO_SMTP_PASSWORD='SMTP password.',LAGO_FROM_EMAIL='Verified sender email.')
    front=svc('lago',image='getlago/front:v1.53.0',env={'API_URL':public('api'),'APP_ENV':'production','LAGO_OAUTH_PROXY_URL':'https://proxy.getlago.com'},port=80)
    pdf=svc('pdf',image='getlago/lago-gotenberg:8.15',command='gotenberg --libreoffice-disable-routes=true --chromium-disable-javascript=true --api-timeout=300s')
    return [pg('lago',image='getlago/postgres-partman:15.0-alpine'),redis(),app,front,pdf]

def docuseal():
    app=svc('docuseal',dockerfile='templates/docuseal/Dockerfile',env={
        'DATABASE_URL':ref('postgres','DATABASE_URL'),'RAILS_ENV':'production','SECRET_KEY_BASE':secret(),
        'ADMIN_EMAIL':(None,'Required first administrator email. Created before the public listener opens.'),
        'ADMIN_PASSWORD':secret(),'ACCOUNT_NAME':'My organization','PUBLIC_URL':public('docuseal'),
        'FORCE_SSL':ref('docuseal','RAILWAY_PUBLIC_DOMAIN'),'RAILS_MAX_THREADS':5,'SIDEKIQ_THREADS':2,
        'SIDEKIQ_BASIC_AUTH_PASSWORD':secret()},volume='/data/docuseal',port=3000)
    return [pg('docuseal'),app]

def frappe(app,slug,version):
    db=svc('mariadb',image='mariadb:10.11',env={'MARIADB_ROOT_PASSWORD':secret(),'MARIADB_ROOT_HOST':'%'},
           volume='/var/lib/mysql',command='docker-entrypoint.sh mariadbd --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci --skip-character-set-client-handshake')
    web=svc(slug,dockerfile='templates/'+slug+'/Dockerfile',env={
        'PORT':8080,'FRAPPE_APP':app,'TEMPLATE_RELEASE':version,'FRAPPE_SITE_NAME':'site.localhost',
        'PUBLIC_URL':public(slug),'DB_HOST':ref('mariadb','RAILWAY_PRIVATE_DOMAIN'),'DB_PORT':3306,
        'DB_ROOT_PASSWORD':ref('mariadb','MARIADB_ROOT_PASSWORD'),'ADMIN_PASSWORD':secret(),
        'REDIS_URL':ref('redis','REDIS_URL'),'WEB_WORKERS':2,
        'ALLOW_MIGRATION':('false','For an existing site, back up its database and files before allowing migration to a changed release.')},
        port=8080,volume='/data',health='/api/method/ping')
    return [db,redis(),web]

def dbgpt():
    app=svc('core',dockerfile='templates/db-gpt/Dockerfile',env={
        'OPENAI_API_KEY':(None,'Required model-provider API key. Provider charges are separate from Railway.'),
        'OPENAI_API_BASE':'https://api.openai.com/v1','LLM_MODEL_NAME':'gpt-4o','EMBEDDING_MODEL_NAME':'text-embedding-3-small',
        'EMBEDDING_MODEL_API_URL':'https://api.openai.com/v1/embeddings','DBGPT_LANG':'en','ENCRYPTION_KEY':secret(32),
        'PUBLIC_URL':public('db-gpt'),'DBGPT_MAX_PARALLEL_SUBAGENTS':1,'HF_HOME':'/data/cache/huggingface'},volume='/data')
    return [app,edge('db-gpt','core',5670)]

def unla():
    app=svc('core',dockerfile='templates/unla/Dockerfile',env={
        'ENV':'production','SUPER_ADMIN_USERNAME':'admin','SUPER_ADMIN_PASSWORD':secret(),
        'APISERVER_JWT_SECRET_KEY':secret(),'APISERVER_DB_NAME':'/app/data/unla.db','GATEWAY_DB_NAME':'/app/data/unla.db',
        'VITE_API_BASE_URL':'/api','VITE_WS_BASE_URL':'/api/ws','VITE_MCP_GATEWAY_BASE_URL':'/gateway',
        'VITE_GATEWAY_SERVICE_BASE_URL':public('unla')+'/gateway','VITE_DIRECT_MCP_GATEWAY_MODIFIER':'/gateway',
        'OAUTH2_ISSUER':public('unla')+'/gateway','LOGGER_LEVEL':'info','LLM_CONFIG_ADMIN_ONLY':'true'},volume='/app/data')
    return [app,edge('unla','core',80)]

def mcpjungle():
    app=svc('core',image='ghcr.io/mcpjungle/mcpjungle:0.4.6',env={
        'DATABASE_URL':ref('postgres','DATABASE_URL'),'SERVER_MODE':'enterprise','OTEL_ENABLED':'false',
        'MCP_SERVER_INIT_REQ_TIMEOUT_SEC':20})
    return [pg('mcpjungle'),app,edge('mcpjungle','core',8080)]

def perses():
    return [svc('core',dockerfile='templates/perses/Dockerfile',env={'ENCRYPTION_KEY':secret(32)},volume='/data'),edge('perses','core',8080)]

def timetagger():
    return [svc('timetagger',dockerfile='templates/timetagger/Dockerfile',env={
        'ADMIN_USERNAME':'admin','ADMIN_PASSWORD':secret(40),'TIMETAGGER_BIND':'0.0.0.0:8080',
        'TIMETAGGER_DATADIR':'/opt/_timetagger','TIMETAGGER_LOG_LEVEL':'info'},volume='/opt/_timetagger',port=8080)]

def vespa():
    return [svc('core',dockerfile='templates/vespa/Dockerfile',env={'VESPA_CONFIGSERVERS':'localhost'},volume='/opt/vespa/var'),
            edge('vespa','core',8080)]

def agenta():
    from catalog_round6_agenta import services
    return services()

CATALOG={'plunk':plunk,'bugsink':bugsink,'notifuse':notifuse,'lago':lago,'docuseal':docuseal,
         'frappe-learning':lambda:frappe('lms','frappe-learning','v2.63.0'), 'db-gpt':dbgpt,
         'frappe-insights':lambda:frappe('insights','frappe-insights','v3.13.2'),
         'frappe-builder':lambda:frappe('builder','frappe-builder','v1.34.0'),
         'unla':unla,'mcpjungle':mcpjungle,'perses':perses,'timetagger':timetagger,'vespa':vespa,'agenta':agenta}

def generate():
    for name,factory in CATALOG.items():
        services=factory()
        config={'services':{str(uuid.uuid5(uuid.NAMESPACE_URL,'round6/'+name+'/'+s['name'])):s for s in services}}
        p=ROOT/'templates'/name;p.mkdir(parents=True,exist_ok=True)
        (p/'template.json').write_text(json.dumps(config,indent=2)+'\n')
        print(name,len(services))

if __name__=='__main__':generate()
