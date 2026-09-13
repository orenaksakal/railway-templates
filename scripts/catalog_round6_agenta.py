"""Adapt the pinned upstream Railway layout, not its live preview project."""
import json
from catalog_round6 import ROOT, svc, pg, redis, ref, secret, private, public, optional

def services():
    upstream=json.loads((ROOT/'templates/agenta/upstream-template.json').read_text())
    result=[]
    for name,s in upstream['services'].items():
        if name in ('Postgres','redis','gateway','seaweedfs','alembic'):continue
        env={}
        for k,v in s['variables'].items():
            if isinstance(v,dict):
                key=v['secret']
                if key=='AGENTA_STORE_JWT_PRIVATE_KEY':continue
                env[k]=secret(20 if key=='AGENTA_STORE_ACCESS_KEY' else 64) if name=='api' else ref('api',key)
            else:
                v=v.replace('${{gateway.', '${{agenta.').replace('${{Postgres.','${{postgres.')
                for service,port in [('api',8000),('services',8080),('supertokens',3567)]:
                    v=v.replace('http://'+service+'.railway.internal:'+str(port),private(service,port))
                v=v.replace('redis://redis.railway.internal:6379/0',ref('redis','REDIS_URL')+'/0')
                env[k]=v
        if name=='api':
            # All shared secrets must exist on the designated owner, even if a
            # release's API variable list omits one consumed by another service.
            for key in upstream['secrets']:
                if key in ('POSTGRES_PASSWORD','AGENTA_STORE_JWT_PRIVATE_KEY'):continue
                env.setdefault(key,secret(20 if key=='AGENTA_STORE_ACCESS_KEY' else 64))
            env['POSTGRES_PASSWORD']=ref('postgres','POSTGRES_PASSWORD')
            env['START_ROLE']='api'
            env['PGHOST']=ref('postgres','RAILWAY_PRIVATE_DOMAIN')
            env['PGPORT']=5432
            env['ALEMBIC_CFG_PATH_CORE']='/app/oss/databases/postgres/migrations/core/alembic.ini'
            env['ALEMBIC_CFG_PATH_TRACING']='/app/oss/databases/postgres/migrations/tracing/alembic.ini'
        if name in ('worker-streams','worker-queues','cron','services'):
            env['START_ROLE']=name
            env['API_HEALTH_URL']=private('api',8000)+'/health'
        if name=='runner':
            env['AGENTA_RUNNER_ENABLED_SANDBOX_PROVIDERS']='daytona'
            env['AGENTA_RUNNER_DEFAULT_SANDBOX_PROVIDER']='daytona'
            env['AGENTA_RUNNER_DAYTONA_API_KEY']=(None,'Required operator-owned Daytona key. Agent execution uses a separate sandbox service; no host Docker socket or FUSE device is provisioned.')
        image=s['image'].replace('{app_tag}','v0.118.0')
        kw={'image':image,'command':s.get('startCommand') or None}
        if name in ('api','worker-streams','worker-queues','cron'):
            kw={'dockerfile':'templates/agenta/Api.Dockerfile'}
        if name=='services':kw={'dockerfile':'templates/agenta/Services.Dockerfile'}
        app=svc(name,**kw,env=env,volume='/data' if name=='api' else None)
        if name=='runner':optional(app,AGENTA_RUNNER_DAYTONA_SNAPSHOT='Optional Daytona snapshot name for the chosen runtime.',AGENTA_RUNNER_DAYTONA_TARGET='Optional Daytona target region.')
        result.append(app)
    db=pg('agenta',dockerfile='templates/agenta/Postgres.Dockerfile')
    store=svc('seaweedfs',dockerfile='templates/agenta/Storage.Dockerfile',env={
        'AGENTA_STORE_ACCESS_KEY':ref('api','AGENTA_STORE_ACCESS_KEY'),
        'AGENTA_STORE_SECRET_KEY':ref('api','AGENTA_STORE_SECRET_KEY'),
        'AGENTA_STORE_SIGNING_KEY':ref('api','AGENTA_STORE_SIGNING_KEY'),
        'AGENTA_STORE_BUCKET':'agenta-store','AGENTA_STORE_JWT_ISSUER':private('api',8000)+'/api'},volume='/data')
    gateway=svc('agenta',dockerfile='templates/agenta/Gateway.Dockerfile',env={
        'UPSTREAM_HOST':ref('web','RAILWAY_PRIVATE_DOMAIN'),'UPSTREAM_PORT':8080,
        'API_HOST':ref('api','RAILWAY_PRIVATE_DOMAIN'),'SERVICES_HOST':ref('services','RAILWAY_PRIVATE_DOMAIN'),
        'MOBILE_HOST':ref('web-mobile','RAILWAY_PRIVATE_DOMAIN'),'ACCESS_PASSWORD':secret(),'OWNER_AUTH':'true'},port=8080,health='/healthz')
    return [db,redis(),store,*result,gateway]
