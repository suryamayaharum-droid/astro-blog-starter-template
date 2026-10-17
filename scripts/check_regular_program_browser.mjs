import assert from 'node:assert/strict';
import fs from 'node:fs';
import { chromium } from 'playwright';
const base=process.env.PROGRAM_TEST_BASE||'http://127.0.0.1:4173/astro-blog-starter-template/';
const browser=await chromium.launch({headless:true});
try {
 const context=await browser.newContext({viewport:{width:390,height:844},reducedMotion:'reduce'});
 const page=await context.newPage();
 const errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto(base+'escola/programa-regular/',{waitUntil:'networkidle'});
 assert.equal(await page.locator('[data-lesson-id]').count(),33);
 await page.locator('[data-program-task]').first().check();
 await page.reload();
 assert.ok(await page.locator('[data-program-task]').first().isChecked(),'A marcação deve sobreviver ao recarregamento');
 await page.goto(base+'escola/programa-regular/contorno-observado/',{waitUntil:'networkidle'});
 assert.ok(await page.locator('[data-program-task]').isChecked(),'A aula deve recuperar o registro do programa');
 await page.locator('[data-program-task]').uncheck();
 await page.reload();
 assert.equal(await page.locator('[data-program-task]').isChecked(),false,'Desmarcar também precisa persistir');
 fs.mkdirSync('responsive-audit',{recursive:true});
 const routes=['escola/programa-regular/','escola/programa-regular/contorno-observado/','escola/programa-regular/veladura/','escola/programa-regular/estudo-e-traducao-autoral/'];
 for(const width of [320,390,761,1440]){
  await page.setViewportSize({width,height:900});
  for(const route of routes){
   const response=await page.goto(base+route,{waitUntil:'networkidle'});
   assert.equal(response.status(),200,route);
   // Force lazy-loaded gallery images to load before checking their decoded size.
   await page.locator('img').evaluateAll(images=>images.forEach(i=>i.loading='eager'));
   await page.waitForFunction(()=>[...document.images].every(i=>i.complete));
   const result=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth+1,broken:[...document.images].filter(i=>i.naturalWidth===0).map(i=>i.src)}));
   assert.equal(result.overflow,false,`${width}: ${route} tem overflow`);
   assert.deepEqual(result.broken,[],`${width}: ${route} tem imagens quebradas`);
   if(route==='escola/programa-regular/'&&(width===390||width===1440))await page.screenshot({path:`responsive-audit/program-${width}.png`,fullPage:true});
   console.log('PASS',width,route);
  }
 }
 await page.goto(base+'buscar/?q=veladura',{waitUntil:'networkidle'});
 assert.ok(await page.locator('#search-results a[href*="programa-regular/veladura/"]').count(),'A busca deve encontrar a aula');
 assert.deepEqual(errors,[],'Não deve haver erros de execução');
 const nojs=await browser.newContext({javaScriptEnabled:false});
 const plain=await nojs.newPage();
 await plain.goto(base+'escola/programa-regular/');
 assert.equal(await plain.locator('[data-lesson-id] a').count(),33,'Todas as aulas precisam estar acessíveis sem JavaScript');
 console.log('PASS: progresso persistente e reversível, busca, 16 combinações de rota/tela e acesso sem JavaScript.');
} finally { await browser.close(); }
