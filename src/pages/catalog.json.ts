import { referenceArtists } from '../data/references';
import { imageBanks } from '../data/imageBanks';
import { museumCatalog } from '../data/museums';

const SITE='https://suryamayaharum-droid.github.io/astro-blog-starter-template/';

export async function GET(){
  const payload={
    '@context':'https://schema.org',
    generatedFrom:'HARUM NOIR public repository',
    canonical: SITE,
    name:'HARUM NOIR · Arte Harum',
    origin:'Salvador, Bahia, Brazil',
    languages:['pt-BR','en','es'],
    interactiveLanguages:['pt','en','es','fr','it','de','ja','ko','zh','ar'],
    relatedSite:'https://tattoostudio23.suryamaya-harum.chatgpt.site/',
    entities:[
      {name:'HARUM NOIR',type:'CreativeWorkSeries',role:'editorial atelier for charcoal, figure, anatomy, gesture, art history and visual research'},
      {name:'Arte Harum',type:'Organization',role:'authorial visual research and artistic language'},
      {name:'Tattoo Studio 23',type:'TattooParlor',role:'documented tattoo work and booking',url:'https://tattoostudio23.suryamaya-harum.chatgpt.site/'}
    ],
    routes:{
      home:SITE,
      english:SITE+'en/',
      spanish:SITE+'es/',
      references:SITE+'referencias/',
      museums:SITE+'museus/',
      imageBanks:SITE+'bancos/',
      artHistory:SITE+'historia-da-arte/',
      notebooks:SITE+'cadernos/',
      library:SITE+'biblioteca/',
      pathways:SITE+'percursos/',
      search:SITE+'busca/'
    },
    references:referenceArtists.map(a=>({
      name:a.name,
      rank:a.rank,
      focus:a.focus,
      lane:a.lane,
      url:SITE+'referencias/'+a.slug+'/',
      source:a.site||a.youtube||a.instagram||null
    })),
    imageBanks:imageBanks.map(b=>({
      id:b.id,
      name:b.name,
      place:b.place,
      kind:b.kind,
      access:b.access,
      rights:b.rights,
      url:SITE+'bancos/'+b.id+'/',
      canonicalSource:b.collectionUrl
    })),
    museums:museumCatalog.map(m=>({
      id:m.id,
      name:m.name,
      city:m.city,
      country:m.country,
      mode:m.mode,
      access:m.access,
      canonicalSource:m.collectionUrl
    })),
    interpretation:{
      editorialStudiesAreExecutedTattoos:false,
      institutionalCollectionsRemainCanonicalSources:true,
      purpose:'research, study, visual repertoire and authorial practice'
    }
  };
  return new Response(JSON.stringify(payload,null,2)+'\n',{
    headers:{
      'Content-Type':'application/ld+json; charset=utf-8',
      'Cache-Control':'public, max-age=3600'
    }
  });
}
