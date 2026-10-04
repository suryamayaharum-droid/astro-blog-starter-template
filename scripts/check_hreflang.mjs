import fs from 'node:fs';
import path from 'node:path';

const root=path.resolve('dist');
const SITE_ORIGIN='https://suryamayaharum-droid.github.io';
const SITE_BASE='/astro-blog-starter-template/';

const htmlFiles=[];
const walk=(dir)=>{
  for(const entry of fs.readdirSync(dir,{withFileTypes:true})){
    const full=path.join(dir,entry.name);
    if(entry.isDirectory())walk(full);
    else if(entry.isFile()&&entry.name.endsWith('.html'))htmlFiles.push(full);
  }
};
walk(root);

const norm=(value)=>{
  try{
    const u=new URL(value,SITE_ORIGIN);
    u.hash='';
    if(u.pathname.length>1)u.pathname=u.pathname.replace(/\/+$/,'');
    return u.href;
  }catch{return value;}
};
const pages=new Map();
for(const file of htmlFiles){
  const html=fs.readFileSync(file,'utf8');
  const lang=html.match(/<html[^>]*\blang="([^"]+)"/i)?.[1]||'';
  const canonical=html.match(/<link[^>]*\brel="canonical"[^>]*\bhref="([^"]+)"/i)?.[1]||'';
  if(!canonical)continue;
  const alternates=new Map();
  const re=/<link[^>]*\brel="alternate"[^>]*\bhreflang="([^"]+)"[^>]*\bhref="([^"]+)"[^>]*>/gi;
  for(const m of html.matchAll(re))alternates.set(m[1],norm(m[2]));
  pages.set(norm(canonical),{file,lang,canonical:norm(canonical),alternates});
}

const errors=[];
let checked=0;
for(const page of pages.values()){
  for(const [hreflang,href] of page.alternates){
    if(hreflang==='x-default'||hreflang===page.lang)continue;
    const u=new URL(href);
    if(u.origin!==SITE_ORIGIN||!u.pathname.startsWith(SITE_BASE))continue;
    checked++;
    const target=pages.get(norm(href));
    if(!target){
      errors.push(`missing target: ${page.canonical} [${hreflang}] -> ${href}`);
      continue;
    }
    const back=target.alternates.get(page.lang);
    if(!back){
      errors.push(`missing reciprocal: ${href} has no hreflang="${page.lang}" back to ${page.canonical}`);
      continue;
    }
    if(norm(back)!==page.canonical){
      errors.push(`wrong reciprocal: ${href} [${page.lang}] -> ${back}, expected ${page.canonical}`);
    }
  }
}

console.log(`hreflang health: ${pages.size} canonical HTML pages | ${checked} localized relations checked | ${errors.length} errors`);
if(errors.length){
  for(const error of errors.slice(0,50))console.error('HREFLANG:',error);
  if(errors.length>50)console.error(`... ${errors.length-50} more`);
  process.exit(1);
}
