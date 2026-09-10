"""Ten unpublished templates. Generate without touching the published catalog."""
from pathlib import Path
import json,uuid
from variable_descriptions import DESCRIPTIONS
ROOT=Path(__file__).resolve().parents[1]
BRANCH='main'
LOCK_PATH=ROOT/'images.round3.lock.json'
LOCK=json.loads(LOCK_PATH.read_text()) if LOCK_PATH.exists() else {}
def secret(n=64):return '${{secret('+str(n)+', "abcdef0123456789")}}'
def ref(s,k):return '${{'+s+'.'+k+'}}'
def private(s,port,scheme='http'):return scheme+'://'+ref(s,'RAILWAY_PRIVATE_DOMAIN')+':'+str(port)
def public(s):return 'https://'+ref(s,'RAILWAY_PUBLIC_DOMAIN')
def desc(k,v,s):
    if k in DESCRIPTIONS:return DESCRIPTIONS[k]
    if isinstance(v,tuple):return v[1]
    if v is None:return 'Required operator-supplied '+k.lower().replace('_',' ')+'. Enter your own value before deployment.'
    if str(v).startswith('${{secret('):return 'Generated '+k.lower().replace('_',' ')+'. Keep private and preserve with backups.'
    if '${{' in str(v):return k.lower().replace('_',' ').capitalize()+' resolved automatically from the linked service. Keep this reference when using the included topology.'
    return k.lower().replace('_',' ').capitalize()+' for '+s+'. The supplied value follows the pinned upstream deployment; change only with its configuration guide.'
def svc(name,*,image=None,dockerfile=None,env=None,port=None,volume=None,health=None,command=None):
    variables={}
    env=dict(env or {})
    if port is not None and health is not None:env.setdefault('PORT',port)
    for k,v in (env or {}).items():
        description=desc(k,v,name)
        if isinstance(v,tuple):v=v[0]
        variables[k]={'isOptional':False,'description':description}
        if v is not None:variables[k]['defaultValue']=str(v)
    s={'name':name,'source':{'image':LOCK.get(image,image)} if image else {'repo':'orenaksakal/railway-templates','branch':BRANCH},'variables':variables,'deploy':{'restartPolicyType':'ON_FAILURE','restartPolicyMaxRetries':10},'networking':{'serviceDomains':{}}}
    if dockerfile:
        s['build']={'builder':'RAILPACK','dockerfilePath':dockerfile};s['variables']['RAILWAY_DOCKERFILE_PATH']={'defaultValue':dockerfile,'isOptional':False,'description':DESCRIPTIONS['RAILWAY_DOCKERFILE_PATH']}
    if port:s['networking']['serviceDomains']={f'<hasDomain>:{port}':{'port':port}}
    if health:s['deploy'].update(healthcheckPath=health,healthcheckTimeout=600)
    if command:s['deploy']['startCommand']=command
    if volume:s['volumeMounts']={str(uuid.uuid5(uuid.NAMESPACE_URL,name+volume)):{'mountPath':volume}};s['deploy']['requiredMountPath']=volume
    return s
def postgres(app,name='postgres',image='postgres:17',db=None,init_args=None):
    # Each app owns a dedicated database. Multi-database products are explicit exceptions.
    env={'POSTGRES_USER':app.replace('-','_'),'POSTGRES_DB':db or app.replace('-','_'),'POSTGRES_PASSWORD':secret(),'PGDATA':'/var/lib/postgresql/data/pgdata'}
    if init_args:env['POSTGRES_INITDB_ARGS']=(init_args,'Initialization options applied only to an empty database volume. Keep locale and encoding compatible with the application.')
    env['DATABASE_URL']='postgresql://'+env['POSTGRES_USER']+':'+ref(name,'POSTGRES_PASSWORD')+'@'+ref(name,'RAILWAY_PRIVATE_DOMAIN')+':5432/'+env['POSTGRES_DB']
    return svc(name,image=image,env=env,volume='/var/lib/postgresql/data')
def redis(name='redis'):
    return svc(name,image='redis:7.4@sha256:71da9275c5f3fcb97d0fa0c8c5b36cc995327265420f17a04bfd544f458059f7',env={'REDIS_PASSWORD':secret(),'REDIS_URL':'redis://:'+ref(name,'REDIS_PASSWORD')+'@'+ref(name,'RAILWAY_PRIVATE_DOMAIN')+':6379'},volume='/data',command="sh -c 'exec redis-server --bind 0.0.0.0 :: --appendonly yes --maxmemory-policy noeviction --requirepass \"$REDIS_PASSWORD\"'")
def storage(bucket,name='storage',exposed=False):
    return svc(name,dockerfile='shared/draft-storage/Dockerfile',env={'MINIO_ROOT_USER':secret(20),'MINIO_ROOT_PASSWORD':secret(),'S3_BUCKET':(bucket,'Private bucket created on first startup; changing this does not move existing objects.')},volume='/data',port=9000 if exposed else None,health='/minio/health/live' if exposed else None)
def dbos():
    return [postgres('dbos'),svc('dbos',dockerfile='templates/dbos/Dockerfile',env={'PORT':3000,'DATABASE_URL':ref('postgres','DATABASE_URL'),'API_KEY':secret()},port=3000,health='/healthz')]
def spicedb():
    return [postgres('spicedb'),svc('spicedb',dockerfile='templates/spicedb/Dockerfile',env={'SPICEDB_DATASTORE_ENGINE':('postgres','Use the included PostgreSQL datastore.'),'SPICEDB_DATASTORE_CONN_URI':ref('postgres','DATABASE_URL')+'?sslmode=disable','SPICEDB_GRPC_PRESHARED_KEY':secret(),'SPICEDB_GRPC_ADDR':('[::]:50051','Private authenticated gRPC listener. No public TCP proxy is created.'),'SPICEDB_HTTP_ENABLED':('true','Enable the authenticated HTTP gateway for Railway HTTPS access.'),'SPICEDB_HTTP_ADDR':('[::]:8443','HTTP gateway listener; Railway terminates public TLS.')},port=8443)]
def frappe(app):
    db=svc('mariadb',image='mariadb:10.11',env={'MARIADB_ROOT_PASSWORD':secret(),'MARIADB_ROOT_HOST':('%','Allow the private application service to initialize its site database.')},volume='/var/lib/mysql',command='docker-entrypoint.sh mariadbd --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci --skip-character-set-client-handshake')
    name='frappe-'+app
    web=svc(name,dockerfile=f'templates/{name}/Dockerfile',env={'PORT':8080,'FRAPPE_APP':(app,'Frappe application installed at build time; do not change independently of the image.'),'TEMPLATE_RELEASE':'v1.83.0' if app=='crm' else 'v1.30.1','FRAPPE_SITE_NAME':('site.localhost','Persistent internal site identity; keep stable when changing the public domain.'),'PUBLIC_URL':public(name),'DB_HOST':ref('mariadb','RAILWAY_PRIVATE_DOMAIN'),'DB_PORT':3306,'DB_ROOT_PASSWORD':ref('mariadb','MARIADB_ROOT_PASSWORD'),'ADMIN_PASSWORD':secret(),'REDIS_URL':ref('redis','REDIS_URL'),'WEB_WORKERS':('2','Gunicorn worker count; tune against available memory.'),'ALLOW_MIGRATION':('false','For an existing site on a different release, back up database and files before setting true for one upgrade.')},port=8080,volume='/data',health='/api/method/ping')
    return [db,redis(),web]
def immich():
    db=postgres('immich',image='ghcr.io/immich-app/postgres:14-vectorchord0.4.3-pgvectors0.2.0@sha256:bcf63357191b76a916ae5eb93464d65c07511da41e3bf7a8416db519b40b1c23',init_args='--data-checksums')
    ml=svc('machine-learning',image='ghcr.io/immich-app/immich-machine-learning:v3.1.0',env={'MACHINE_LEARNING_WORKERS':('1','One CPU inference worker initially. No GPU is configured.')},volume='/cache')
    app=svc('immich',dockerfile='templates/immich/Dockerfile',env={'PORT':2283,'DB_HOSTNAME':ref('postgres','RAILWAY_PRIVATE_DOMAIN'),'DB_PORT':5432,'DB_USERNAME':'immich','DB_PASSWORD':ref('postgres','POSTGRES_PASSWORD'),'DB_DATABASE_NAME':'immich','REDIS_HOSTNAME':ref('redis','RAILWAY_PRIVATE_DOMAIN'),'REDIS_PORT':6379,'REDIS_PASSWORD':ref('redis','REDIS_PASSWORD'),'IMMICH_CONFIG_FILE':('/tmp/immich-config.json','Generated at startup to configure the private machine-learning service.'),'MACHINE_LEARNING_URL':private('machine-learning',3003),'IMMICH_TELEMETRY_INCLUDE':('','Empty selection disables telemetry collection.')},port=2283,volume='/data',health='/api/server/ping')
    return [db,redis(),ml,app]
def matrix():
    db=postgres('synapse',name='synapse-db',init_args='--encoding=UTF8 --locale=C');masdb=postgres('mas',name='mas-db')
    gw=svc('matrix',dockerfile='templates/matrix/Gateway.Dockerfile',env={'PORT':8080,'SYNAPSE_HOST':ref('synapse','RAILWAY_PRIVATE_DOMAIN'),'MAS_HOST':ref('mas','RAILWAY_PRIVATE_DOMAIN'),'PUBLIC_HOST':ref('matrix','RAILWAY_PUBLIC_DOMAIN')},port=8080,health='/healthz')
    syn=svc('synapse',dockerfile='templates/matrix/Synapse.Dockerfile',env={'SYNAPSE_SERVER_NAME':(ref('matrix','RAILWAY_PUBLIC_DOMAIN'),'Immutable Matrix server name. Choose your final domain before first deployment; it cannot be renamed later.'),'SYNAPSE_REPORT_STATS':'no','PUBLIC_URL':public('matrix'),'DB_HOST':ref('synapse-db','RAILWAY_PRIVATE_DOMAIN'),'DB_USER':'synapse','DB_PASSWORD':ref('synapse-db','POSTGRES_PASSWORD'),'MAS_URL':private('mas',8080)+'/', 'MATRIX_SHARED_SECRET':secret()},volume='/data')
    mas=svc('mas',dockerfile='templates/matrix/Mas.Dockerfile',env={'DATABASE_URL':ref('mas-db','DATABASE_URL'),'PUBLIC_URL':public('mas'),'SERVER_NAME':ref('synapse','SYNAPSE_SERVER_NAME'),'SYNAPSE_URL':private('synapse',8008),'MATRIX_SHARED_SECRET':ref('synapse','MATRIX_SHARED_SECRET'),'REGISTRATION_ENABLED':('false','Self-service registration stays closed. Create users with the MAS CLI, or deliberately enable registration for onboarding.')},volume='/data',port=8080)
    element=svc('element',dockerfile='templates/matrix/Element.Dockerfile',env={'HOMESERVER_URL':public('matrix'),'SERVER_NAME':ref('synapse','SYNAPSE_SERVER_NAME')},port=80,health='/')
    return [db,masdb,syn,mas,gw,element]
def novu():
    db=svc('mongodb',image='mongo:8.0.17',env={'MONGO_INITDB_ROOT_USERNAME':'novu','MONGO_INITDB_ROOT_PASSWORD':secret()},volume='/data/db')
    common={'NODE_ENV':'production','MONGO_URL':'mongodb://novu:'+ref('mongodb','MONGO_INITDB_ROOT_PASSWORD')+'@'+ref('mongodb','RAILWAY_PRIVATE_DOMAIN')+':27017/novu?authSource=admin','MONGO_MIN_POOL_SIZE':1,'MONGO_MAX_POOL_SIZE':10,'REDIS_HOST':ref('redis','RAILWAY_PRIVATE_DOMAIN'),'REDIS_PORT':6379,'REDIS_PASSWORD':ref('redis','REDIS_PASSWORD'),'REDIS_DB_INDEX':2,'REDIS_CACHE_SERVICE_HOST':ref('redis','RAILWAY_PRIVATE_DOMAIN'),'REDIS_CACHE_SERVICE_PORT':6379,'NEW_RELIC_ENABLED':'false','S3_LOCAL_STACK':private('storage',9000),'S3_BUCKET_NAME':'novu','S3_REGION':'us-east-1','AWS_ACCESS_KEY_ID':ref('storage','MINIO_ROOT_USER'),'AWS_SECRET_ACCESS_KEY':ref('storage','MINIO_ROOT_PASSWORD'),'API_ROOT_URL':public('api'),'SUBSCRIBER_WIDGET_JWT_EXPIRATION_TIME':'15d'}
    api=svc('api',image='ghcr.io/novuhq/novu/api:3.19.0',env={**common,'PORT':3000,'FRONT_BASE_URL':public('novu'),'JWT_SECRET':secret(),'STORE_ENCRYPTION_KEY':(secret(32),'Exactly 32 generated characters for encrypting provider credentials; retain with MongoDB backups.'),'NOVU_SECRET_KEY':secret(),'MONGO_AUTO_CREATE_INDEXES':'true','IS_API_IDEMPOTENCY_ENABLED':'false','IS_API_RATE_LIMITING_ENABLED':'false','IS_NEW_MESSAGES_API_RESPONSE_ENABLED':'true','IS_V2_ENABLED':'true','IS_SELF_HOSTED':'true'},port=3000,health='/v1/health-check')
    worker=svc('worker',image='ghcr.io/novuhq/novu/worker:3.19.0',env={**common,'PORT':3004,'STORE_ENCRYPTION_KEY':ref('api','STORE_ENCRYPTION_KEY'),'BROADCAST_QUEUE_CHUNK_SIZE':100,'MULTICAST_QUEUE_CHUNK_SIZE':100,'IS_EMAIL_INLINE_CSS_DISABLED':'false','IS_USE_MERGED_DIGEST_ID_ENABLED':'false'})
    ws=svc('ws',image='ghcr.io/novuhq/novu/ws:3.19.0',env={**common,'PORT':3002,'JWT_SECRET':ref('api','JWT_SECRET')},port=3002,health='/v1/health-check')
    dash=svc('novu',image='ghcr.io/novuhq/novu/dashboard:3.19.0',env={'VITE_API_HOSTNAME':public('api'),'VITE_WEBSOCKET_HOSTNAME':public('ws')},port=4000,health='/')
    return [db,redis(),storage('novu'),api,worker,ws,dash]
def appflowy():
    db=svc('postgres',dockerfile='templates/appflowy/Postgres.Dockerfile',env={'POSTGRES_USER':'postgres','POSTGRES_DB':'postgres','POSTGRES_PASSWORD':secret(),'APP_USER':'appflowy','APP_DB':'appflowy','APP_PASSWORD':secret(),'PGDATA':'/var/lib/postgresql/data/pgdata','ENABLE_VECTOR':'true','ALLOW_APP_DATABASE_CREATION':'false','DATABASE_URL':'postgresql://appflowy:'+ref('postgres','APP_PASSWORD')+'@'+ref('postgres','RAILWAY_PRIVATE_DOMAIN')+':5432/appflowy'},volume='/var/lib/postgresql/data')
    s3={'APPFLOWY_S3_USE_MINIO':'true','APPFLOWY_S3_CREATE_BUCKET':'true','APPFLOWY_S3_MINIO_URL':private('storage',9000),'APPFLOWY_S3_ACCESS_KEY':ref('storage','MINIO_ROOT_USER'),'APPFLOWY_S3_SECRET_KEY':ref('storage','MINIO_ROOT_PASSWORD'),'APPFLOWY_S3_BUCKET':'appflowy','APPFLOWY_S3_REGION':'us-east-1'}
    auth=svc('gotrue',image='appflowyinc/gotrue:latest',env={'PORT':9999,'GOTRUE_ADMIN_EMAIL':(None,'Required service-administrator email. This is not the end-user AppFlowy account; sign up separately in the app.'),'GOTRUE_ADMIN_PASSWORD':secret(),'GOTRUE_SITE_URL':'appflowy-flutter://','GOTRUE_URI_ALLOW_LIST':public('appflowy')+'/**,appflowy-flutter://**','GOTRUE_JWT_SECRET':secret(),'GOTRUE_JWT_EXP':7200,'GOTRUE_JWT_ADMIN_GROUP_NAME':'supabase_admin','GOTRUE_DB_DRIVER':'postgres','DATABASE_URL':ref('postgres','DATABASE_URL')+'?search_path=auth','API_EXTERNAL_URL':public('appflowy')+'/gotrue','GOTRUE_DISABLE_SIGNUP':'false','GOTRUE_MAILER_AUTOCONFIRM':('true','No SMTP is configured. Email confirmation is bypassed until you configure delivery.'),'GOTRUE_MAILER_URLPATHS_CONFIRMATION':'/gotrue/verify','GOTRUE_MAILER_URLPATHS_RECOVERY':'/gotrue/verify'})
    api=svc('cloud',image='appflowyinc/appflowy_cloud:0.18.3',env={**s3,'RUST_LOG':'info','APPFLOWY_ENVIRONMENT':'production','APPFLOWY_DATABASE_URL':ref('postgres','DATABASE_URL'),'APPFLOWY_REDIS_URI':ref('redis','REDIS_URL'),'APPFLOWY_GOTRUE_JWT_SECRET':ref('gotrue','GOTRUE_JWT_SECRET'),'APPFLOWY_GOTRUE_JWT_EXP':7200,'APPFLOWY_GOTRUE_BASE_URL':private('gotrue',9999),'APPFLOWY_S3_PRESIGNED_URL_ENDPOINT':public('storage'),'APPFLOWY_ACCESS_CONTROL':'true','APPFLOWY_DATABASE_MAX_CONNECTIONS':20,'APPFLOWY_WEB_URL':public('appflowy'),'APPFLOWY_BASE_URL':public('appflowy'),'APPFLOWY_INDEXER_ENABLED':('false','Optional AI indexer is not included in this draft.')})
    worker=svc('worker',image='appflowyinc/appflowy_worker:0.18.3',env={**s3,'RUST_LOG':'info','APPFLOWY_ENVIRONMENT':'production','APPFLOWY_WORKER_ENVIRONMENT':'production','APPFLOWY_WORKER_REDIS_URL':ref('redis','REDIS_URL'),'APPFLOWY_WORKER_DATABASE_URL':ref('postgres','DATABASE_URL'),'APPFLOWY_WORKER_DATABASE_NAME':'appflowy','APPFLOWY_WORKER_IMPORT_TICK_INTERVAL':30})
    admin=svc('admin',image='appflowyinc/admin_frontend:latest',env={'ADMIN_FRONTEND_REDIS_URL':ref('redis','REDIS_URL'),'ADMIN_FRONTEND_GOTRUE_URL':private('gotrue',9999),'ADMIN_FRONTEND_APPFLOWY_CLOUD_URL':private('cloud',8000),'ADMIN_FRONTEND_PATH_PREFIX':'/console'})
    web=svc('web',image='appflowyinc/appflowy_web:0.17.1',env={'APPFLOWY_BASE_URL':public('appflowy'),'APPFLOWY_GOTRUE_BASE_URL':public('appflowy')+'/gotrue','APPFLOWY_WS_BASE_URL':'wss://'+ref('appflowy','RAILWAY_PUBLIC_DOMAIN')+'/ws/v2','PORT':80})
    gw=svc('appflowy',dockerfile='templates/appflowy/Gateway.Dockerfile',env={'PORT':8080,'API_HOST':ref('cloud','RAILWAY_PRIVATE_DOMAIN'),'AUTH_HOST':ref('gotrue','RAILWAY_PRIVATE_DOMAIN'),'WEB_HOST':ref('web','RAILWAY_PRIVATE_DOMAIN'),'ADMIN_HOST':ref('admin','RAILWAY_PRIVATE_DOMAIN')},port=8080,health='/healthz')
    return [db,redis(),storage('appflowy',exposed=True),auth,api,worker,admin,web,gw]
def appwrite():
    # Core-only draft: no Docker socket, execution worker, or external executor is provisioned.
    db=postgres('appwrite',image='appwrite/postgres:0.1.0');db['volumeMounts']={str(uuid.uuid5(uuid.NAMESPACE_URL,'appwrite-pg')):{'mountPath':'/var/lib/postgresql'}};db['deploy']['requiredMountPath']='/var/lib/postgresql';db['variables']['PGDATA']['defaultValue']='/var/lib/postgresql/18/docker'
    env={'PORT':80,'APPWRITE_WORKER_POOL_SIZE':('78','Connection pool budget for the combined worker, matching the pinned upstream queue concurrency. Does not change HTTP pool size.'),'_APP_CPU_NUM':1,'_APP_ENV':('production','Production self-host runtime mode.'),'_APP_EDITION':'self-hosted','_APP_DOMAIN':ref('appwrite','RAILWAY_PUBLIC_DOMAIN'),'_APP_CONSOLE_DOMAIN':ref('appwrite','RAILWAY_PUBLIC_DOMAIN'),'_APP_CONSOLE_HOSTNAMES':ref('appwrite','RAILWAY_PUBLIC_DOMAIN'),'_APP_OPTIONS_FORCE_HTTPS':'enabled','_APP_OPTIONS_ABUSE':'enabled','_APP_OPENSSL_KEY_V1':secret(),'_APP_NOTIFICATIONS_TRACKING_SECRET':secret(),'_APP_DB_ADAPTER':'postgresql','_APP_DB_HOST':ref('postgres','RAILWAY_PRIVATE_DOMAIN'),'_APP_DB_PORT':5432,'_APP_DB_SCHEMA':'appwrite','_APP_DB_USER':'appwrite','_APP_DB_PASS':ref('postgres','POSTGRES_PASSWORD'),'_APP_DB_ROOT_PASS':ref('postgres','POSTGRES_PASSWORD'),'_APP_DB_ADAPTER_DOCUMENTSDB':'mongodb','_APP_DB_HOST_DOCUMENTSDB':ref('mongodb','RAILWAY_PRIVATE_DOMAIN'),'_APP_DB_PORT_DOCUMENTSDB':27017,'_APP_DB_ADAPTER_VECTORSDB':'postgresql','_APP_DB_HOST_VECTORSDB':ref('postgres','RAILWAY_PRIVATE_DOMAIN'),'_APP_DB_PORT_VECTORSDB':5432,'_APP_REDIS_HOST':ref('redis','RAILWAY_PRIVATE_DOMAIN'),'_APP_REDIS_PORT':6379,'_APP_REDIS_PASS':ref('redis','REDIS_PASSWORD'),'_APP_STORAGE_LIMIT':('30000000','Maximum upload size in bytes; individual bucket limits must fit within this ceiling.'),'_APP_STORAGE_DEVICE':'Local','_APP_STORAGE_ANTIVIRUS':'disabled','_APP_USAGE_STATS':'disabled','_APP_FUNCTIONS_RUNTIMES':('','Functions and Sites execution are excluded: Railway does not supply the Docker socket required by the executor.'),'_APP_EXECUTOR_SECRET':secret(),'_APP_GEO_ENDPOINT':private('geo',80)+'/v1','_APP_GEO_SECRET':secret(),'_APP_WORKERS_NUM':1,'_APP_WORKER_PER_CORE':1,'ALLOW_MIGRATION':('false','Back up all data before allowing an upgrade migration on an existing volume.')}
    app=svc('core',dockerfile='templates/appwrite/Dockerfile',env=env,volume='/storage')
    console=svc('console',image='appwrite/new:1.1.16',env={'VITE_CONSOLE_PROFILE':'self-hosted','APPWRITE_ENDPOINT_SAME_ORIGIN':'true'})
    geo=svc('geo',image='appwrite/geo:0.3.1',env={'GEO_SECRET':ref('core','_APP_GEO_SECRET')})
    realtime=svc('realtime',dockerfile='templates/appwrite/Realtime.Dockerfile',env={**{key:ref('core',key) for key in env},'_APP_POOL_ADAPTER':'swoole'},command='realtime')
    gw=svc('appwrite',dockerfile='templates/appwrite/Gateway.Dockerfile',env={'PORT':8080,'API_HOST':ref('core','RAILWAY_PRIVATE_DOMAIN'),'CONSOLE_HOST':ref('console','RAILWAY_PRIVATE_DOMAIN'),'REALTIME_HOST':ref('realtime','RAILWAY_PRIVATE_DOMAIN')},port=8080,health='/healthz')
    mongo=svc('mongodb',dockerfile='templates/appwrite/Mongo.Dockerfile',env={'MONGO_INITDB_ROOT_USERNAME':'appwrite','MONGO_INITDB_ROOT_PASSWORD':ref('postgres','POSTGRES_PASSWORD'),'MONGO_PRIVATE_HOST':ref('mongodb','RAILWAY_PRIVATE_DOMAIN')},volume='/data')
    return [db,mongo,redis(),app,realtime,console,geo,gw]
def ragflow():
    db=svc('mysql',image='mysql:8.0.40',env={'MYSQL_ROOT_PASSWORD':secret(),'MYSQL_DATABASE':'rag_flow','MYSQL_USER':'ragflow','MYSQL_PASSWORD':secret()},volume='/var/lib/mysql',command='docker-entrypoint.sh mysqld --max-connections=150 --max-allowed-packet=1073741824 --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci --default-authentication-plugin=mysql_native_password --binlog-expire-logs-seconds=604800')
    es=svc('elasticsearch',dockerfile='templates/ragflow/Elasticsearch.Dockerfile',env={'discovery.type':('single-node','Single-node search index. This is not a high-availability cluster.'),'xpack.security.enabled':'true','xpack.security.http.ssl.enabled':'false','ELASTIC_PASSWORD':secret(),'ES_JAVA_OPTS':('-Xms1g -Xmx1g','Initial Java heap. Increase only with sufficient Railway memory.'),'node.store.allow_mmap':('false','Avoid dependence on host vm.max_map_count, which cannot be changed from a Railway container.')},volume='/usr/share/elasticsearch/data')
    app=svc('ragflow',dockerfile='templates/ragflow/Dockerfile',env={'DOC_ENGINE':'elasticsearch','DB_TYPE':'mysql','DEVICE':'cpu','MYSQL_HOST':ref('mysql','RAILWAY_PRIVATE_DOMAIN'),'MYSQL_DBNAME':'rag_flow','MYSQL_USER':'ragflow','MYSQL_PASSWORD':ref('mysql','MYSQL_PASSWORD'),'MYSQL_PORT':3306,'MYSQL_MAX_PACKET':1073741824,'ES_HOST':ref('elasticsearch','RAILWAY_PRIVATE_DOMAIN'),'ELASTIC_PASSWORD':ref('elasticsearch','ELASTIC_PASSWORD'),'MINIO_HOST':ref('storage','RAILWAY_PRIVATE_DOMAIN'),'MINIO_USER':ref('storage','MINIO_ROOT_USER'),'MINIO_PASSWORD':ref('storage','MINIO_ROOT_PASSWORD'),'REDIS_HOST':ref('redis','RAILWAY_PRIVATE_DOMAIN'),'REDIS_PASSWORD':ref('redis','REDIS_PASSWORD'),'REGISTER_ENABLED':('1','Enable account onboarding initially. Disable registration after creating the intended accounts.'),'ENABLE_REGISTER':'1','API_PROXY_SCHEME':'python','ALLOW_ANY_HOST':'0','TZ':'UTC'},port=80,health='/')
    return [db,es,redis(),storage('ragflow'),app]
CATALOG={'dbos':dbos,'spicedb':spicedb,'frappe-crm':lambda:frappe('crm'),'frappe-helpdesk':lambda:frappe('helpdesk'),'immich':immich,'matrix':matrix,'novu':novu,'appflowy':appflowy,'appwrite':appwrite,'ragflow':ragflow}
def generate():
    for name,factory in CATALOG.items():
        services=factory();config={'services':{str(uuid.uuid5(uuid.NAMESPACE_URL,name+'/'+s['name'])):s for s in services}}
        (ROOT/'templates'/name/'template.json').write_text(json.dumps(config,indent=2)+'\n');print(name,len(services))
if __name__=='__main__':generate()
