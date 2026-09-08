const fs=require('node:fs');
const url=new URL(process.env.MACHINE_LEARNING_URL);
if(url.protocol!=='http:')throw new Error('Expected private HTTP machine-learning endpoint');
fs.writeFileSync('/tmp/immich-config.json',JSON.stringify({machineLearning:{enabled:true,urls:[url.href]}}));
