import fs from 'node:fs/promises';
import path from 'node:path';

const failures=[];
const readJson=async(file)=>{
  try{return JSON.parse(await fs.readFile(path.resolve(file),'utf8'))}
  catch(error){failures.push(file+': '+String(error.message||error));return null}
};

const [catalog,knowledge,lume]=await Promise.all([
  readJson('dist/catalog.json'),
  readJson('dist/site-knowledge.json'),
  fs.readFile(path.resolve('src/components/LumeGuide.astro'),'utf8').catch(error=>{
    failures.push('src/components/LumeGuide.astro: '+String(error.message||error));
    return '';
  })
]);

const expect=(condition,message)=>{if(!condition)failures.push(message)};

if(catalog){
  expect(catalog.routes?.search?.endsWith('/buscar/'),'catalog routes.search must point to /buscar/');
  expect(catalog.routes?.charcoalRitual?.endsWith('/ritual-do-carvao/'),'catalog must expose charcoalRitual');
  expect(catalog.routes?.students?.endsWith('/alunos/'),'catalog must expose students');
  expect(catalog.routes?.observationRituals?.endsWith('/rituais-de-olhar/'),'catalog must expose observationRituals');
}

if(knowledge){
  expect(knowledge.routes?.search==='/buscar/','site-knowledge routes.search must be /buscar/');
  expect(knowledge.routes?.charcoalRitual==='/ritual-do-carvao/','site-knowledge must expose charcoalRitual');
  expect(knowledge.routes?.students==='/alunos/','site-knowledge must expose students');
  expect(knowledge.productStatus?.charcoalRitual?.state==='prelaunch','charcoal ritual must remain prelaunch');
  expect(knowledge.productStatus?.charcoalRitual?.purchaseOpen===false,'charcoal ritual purchase must remain closed');
  expect(knowledge.productStatus?.charcoalRitual?.freeSample==='/ritual-do-carvao/#amostra','charcoal ritual free sample route is stale');
}

if(lume){
  expect(lume.includes("search:{href:base+'buscar/'"),'Lume search destination must use /buscar/');
  expect(!lume.includes("search:{href:base+'busca/'"),'Lume still points to legacy /busca/');
  expect(lume.includes("ritual:{href:base+'ritual-do-carvao/#amostra'"),'Lume must expose the Ritual free sample');
}

if(failures.length){
  for(const failure of failures)console.error('DISCOVERY CONTRACT:',failure);
  process.exit(1);
}

console.log('Discovery contract passed: machine maps, canonical search and Ritual pre-launch state are aligned.');
