import http from 'node:http';
import { createHash, timingSafeEqual } from 'node:crypto';
import { DBOS } from '@dbos-inc/dbos-sdk';

const key = process.env.API_KEY;
if (!key || key.length < 32 || !process.env.DATABASE_URL) throw new Error('Database and strong API key are required');
const authorized = (value) => {
  const a=Buffer.from(value || ''); const b=Buffer.from(`Bearer ${key}`);
  return a.length===b.length && timingSafeEqual(a,b);
};
DBOS.setConfig({name:'railway-durable-webhooks',systemDatabaseUrl:process.env.DATABASE_URL,systemDatabasePoolSize:5,executorID:'railway-single-replica',runAdminServer:false});
const processEvent = DBOS.registerWorkflow(async (event,delaySeconds) => {
  await DBOS.sleepSeconds(delaySeconds);
  return DBOS.runStep(async () => ({digest:createHash('sha256').update(JSON.stringify(event)).digest('hex'),event}),{name:'digest-event',retriesAllowed:true,maxAttempts:3});
},{name:'process-event'});
await import('./wait-for-dependencies.mjs');
await DBOS.launch();
const send=(res,status,body)=>{res.writeHead(status,{'Content-Type':'application/json','Cache-Control':'no-store'});res.end(JSON.stringify(body));};
const server=http.createServer(async (req,res)=>{
  try {
    const url=new URL(req.url,'http://localhost');
    if(req.method==='GET' && url.pathname==='/healthz') return send(res,200,{status:'ready'});
    if(!authorized(req.headers.authorization)) return send(res,401,{error:'Unauthorized'});
    if(req.method==='POST' && url.pathname==='/events') {
      const id=req.headers['idempotency-key'];
      if(typeof id!=='string'||!/^[a-zA-Z0-9_-]{1,128}$/.test(id))return send(res,400,{error:'Idempotency-Key must contain 1-128 letters, digits, underscores or hyphens'});
      let size=0;const chunks=[];
      for await(const chunk of req){size+=chunk.length;if(size>65536){send(res,413,{error:'Maximum body is 64 KiB'});return;}chunks.push(chunk);}
      let payload;try{payload=JSON.parse(Buffer.concat(chunks).toString());}catch{return send(res,400,{error:'Invalid JSON'});}
      if(!payload||typeof payload!=='object'||Array.isArray(payload))return send(res,400,{error:'JSON object required'});
      const delay=payload.delaySeconds??5;
      if(!Number.isInteger(delay)||delay<0||delay>3600)return send(res,400,{error:'delaySeconds must be 0-3600'});
      if(!Object.hasOwn(payload,'event'))return send(res,400,{error:'event is required'});
      const fingerprint=createHash('sha256').update(JSON.stringify({event:payload.event,delay})).digest('hex');
      const workflowID=`${id}-${fingerprint}`;
      await DBOS.startWorkflow(processEvent,{workflowID})(payload.event,delay);
      return send(res,202,{workflowID,statusUrl:`/events/${workflowID}`});
    }
    if(req.method==='GET' && /^\/events\/[a-zA-Z0-9_-]+$/.test(url.pathname)) {
      const handle=DBOS.retrieveWorkflow(url.pathname.slice(8));const status=await handle.getStatus();
      if(!status)return send(res,404,{error:'Unknown event'});
      return send(res,200,{status:status.status,...(status.status==='SUCCESS'?{result:await handle.getResult()}: {})});
    }
    send(res,404,{error:'Not found'});
  } catch {send(res,500,{error:'Workflow request failed'});}
});
server.listen(Number(process.env.PORT||3000),process.env.HOST||'0.0.0.0');
for(const signal of ['SIGTERM','SIGINT'])process.on(signal,()=>server.close(async()=>{await DBOS.shutdown();process.exit(0);}));
