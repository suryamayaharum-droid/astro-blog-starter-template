import fs from 'node:fs';
import path from 'node:path';

const root=path.resolve('dist');
const SITE_ORIGIN=new URL(process.env.PUBLIC_SITE_URL||'https://suryamayaharum-droid.github.io').origin;
const SITE_BASE=process.env.PUBLIC_SITE_URL?'/':'/astro-blog-starter-template/';
const htmlFiles=[];
const walk=(dir)=>{
  for(const entry of fs.readdirSync(dir,{withFileTypes:true})){
    const full=path.join(dir,entry.name);
    if(entry.isDirectory())walk(full);
    else if(entry.isFile()&&entry.name.endsWith('.html'))htmlFiles.push(full);
  }
};
walk(root);

const errors=[];
const warnings=[];
const capture=(html,re)=>html.match(re)?.[1]?.trim()||'';
const meta=(html,key)=>{
  const esc=key.replace(/[.*+?^$(){}|[\\]\\\\]/g,'\\\\$&');
  return capture(html,new RegExp('<meta[^>]+(?:name|property)="'+esc+'"[^>]+content="([^"]*)"[^>]*>','i'));
};

for(const file of htmlFiles){
  const html=fs.readFileSync(file,'utf8');
  const rel=path.relative(root,file).replaceAll(path.sep,'/');
  const title=capture(html,/<title>([^<]*)<\\/title>/i);
  const desc=meta(html,'description');
  const robots=meta(html,'robots');
  const lang=capture(html,/<html[^>]*\\blang="([^"]+)"/i);
  const canonical=capture(html,/<link[^>]*\\brel="canonical"[^>]*\\bhref="([^"]+)"/i);
  const ogTitle=meta(html,'og:title');
  const ogDescription=meta(html,'og:description');
  const ogImage=meta(html,'og:image');
  const isRedirect=/<meta[^>]*http-equiv="refresh"[^>]*>/i.test(html);

  if(isRedirect){
    if(!title)errors.push(rel+': redirect missing title');
    if(!canonical)errors.push(rel+': redirect missing canonical');
    else{
      try{
        const u=new URL(canonical,SITE_ORIGIN);
        if(u.origin!==SITE_ORIGIN||!u.pathname.startsWith(SITE_BASE))errors.push(rel+': redirect canonical leaves site '+u.href);
        else{
          const sub=u.pathname.slice(SITE_BASE.length).replace(/^\\/+|\\/+$/g,'');
          const target=sub?path.join(root,...sub.split('/'),'index.html'):path.join(root,'index.html');
          const fileTarget=sub?path.join(root,...sub.split('/')):path.join(root,'index.html');
          if(!fs.existsSync(target)&&!fs.existsSync(fileTarget))errors.push(rel+': redirect target missing '+u.pathname);
        }
      }catch{errors.push(rel+': invalid redirect canonical '+canonical);}
    }
    if(!robots||!/noindex/i.test(robots)||!/follow/i.test(robots))errors.push(rel+': redirect must declare noindex,follow');
    continue;
  }

  if(!title)errors.push(rel+': missing title');
  if(!desc)errors.push(rel+': missing meta description');
  if(!lang)errors.push(rel+': missing html lang');
  if(!canonical)errors.push(rel+': missing canonical');
  else{
    try{
      const u=new URL(canonical);
      if(!/^https?:$/.test(u.protocol)||u.origin!==SITE_ORIGIN||!u.pathname.startsWith(SITE_BASE))throw new Error();
    }catch{errors.push(rel+': invalid or noncanonical URL '+canonical);}
  }
  if(!robots)errors.push(rel+': missing robots meta');
  else if(/noindex/i.test(robots))errors.push(rel+': production page is noindex');
  if(!ogTitle)errors.push(rel+': missing og:title');
  if(!ogDescription)errors.push(rel+': missing og:description');
  if(!ogImage)errors.push(rel+': missing og:image');

  if(title.length>75)warnings.push(rel+': long title ('+title.length+')');
  if(desc.length>180)warnings.push(rel+': long description ('+desc.length+')');

  const selfAlt=[...html.matchAll(/<link[^>]*\\brel="alternate"[^>]*\\bhreflang="([^"]+)"[^>]*\\bhref="([^"]+)"/gi)].find(m=>m[1]===lang);
  if(!selfAlt)errors.push(rel+': missing self hreflang for '+lang);

  for(const m of html.matchAll(/<script[^>]*type="application\\/ld\\+json"[^>]*>([\\s\\S]*?)<\\/script>/gi)){
    const raw=m[1].trim();
    if(!raw){errors.push(rel+': empty JSON-LD block');continue;}
    try{
      const data=JSON.parse(raw);
      if(!data||typeof data!=='object')errors.push(rel+': JSON-LD is not an object');
    }catch(error){
      errors.push(rel+': invalid JSON-LD: '+String(error.message||error));
    }
  }
}

console.log('SEO surface: '+htmlFiles.length+' HTML pages | '+errors.length+' errors | '+warnings.length+' warnings');
for(const warning of warnings.slice(0,30))console.warn('SEO WARNING:',warning);
if(warnings.length>30)console.warn('... '+(warnings.length-30)+' more warnings');
if(errors.length){
  for(const error of errors.slice(0,80))console.error('SEO ERROR:',error);
  if(errors.length>80)console.error('... '+(errors.length-80)+' more errors');
  process.exit(1);
}
