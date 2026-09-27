import fs from "node:fs/promises";

const source = await fs.readFile("src/data/references.ts","utf8");
const matches = [...source.matchAll(/https:\/\/[^"'\s)]+/g)].map(m=>m[0].replace(/[;,]$/,""));
const urls = [...new Set(matches)].sort();
const socialHosts = new Set(["www.youtube.com","youtube.com","www.instagram.com","instagram.com","youtu.be"]);
const results=[];

async function check(url){
  const controller=new AbortController();
  const timer=setTimeout(()=>controller.abort(),12000);
  try{
    let res=await fetch(url,{method:"HEAD",redirect:"follow",signal:controller.signal,headers:{"user-agent":"HarumNoir-LinkHealth/1.0"}});
    if([405,501].includes(res.status)){
      res=await fetch(url,{method:"GET",redirect:"follow",signal:controller.signal,headers:{"user-agent":"HarumNoir-LinkHealth/1.0"}});
    }
    const host=new URL(url).hostname;
    const hard=[404,410].includes(res.status) && !socialHosts.has(host);
    const state=hard?"broken":res.status>=400?"warning":"ok";
    return {url,status:res.status,state,finalUrl:res.url};
  }catch(error){
    return {url,status:null,state:"warning",error:String(error?.message||error)};
  }finally{clearTimeout(timer)}
}

for(const url of urls){
  const result=await check(url);
  results.push(result);
  console.log(`${result.state.toUpperCase().padEnd(7)} ${String(result.status??"-").padEnd(4)} ${url}`);
}
const summary={
  checkedAt:new Date().toISOString(),
  total:results.length,
  ok:results.filter(r=>r.state==="ok").length,
  warning:results.filter(r=>r.state==="warning").length,
  broken:results.filter(r=>r.state==="broken").length,
  results
};
await fs.writeFile("link-health.json",JSON.stringify(summary,null,2));
console.log("\nSummary",summary.total,"links |",summary.ok,"ok |",summary.warning,"warning |",summary.broken,"broken");
if(summary.broken>0) process.exitCode=1;
