import rss from "@astrojs/rss";
import { SITE_TITLE, SITE_DESCRIPTION } from "../consts";
export async function GET(context){
 return rss({
  title:`${SITE_TITLE} · Carta do Ateliê`,
  description:SITE_DESCRIPTION,
  site:context.site,
  items:[{title:"Carta do Ateliê 001 — O desenho ainda precisa de silêncio",description:"Uma carta sobre processo, atenção, bordas e o que escolhemos deixar em suspensão.",pubDate:new Date("2026-09-27T15:00:00-03:00"),link:"/astro-blog-starter-template/carta"}],
  customData:"<language>pt-br</language>",
 });
}
