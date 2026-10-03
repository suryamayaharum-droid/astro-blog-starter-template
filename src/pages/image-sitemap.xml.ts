const SITE='https://suryamayaharum-droid.github.io/astro-blog-starter-template';
const rows=[
  ['/', 'noir/visual-atlas/atelier-desk.webp', 'HARUM NOIR editorial atelier', 'Editorial atelier and visual research environment in Salvador, Brazil.'],
  ['/biblioteca/', 'noir/visual-atlas/charcoal-marks.webp', 'Charcoal marks study', 'Charcoal texture, pressure and mark-making study.'],
  ['/atelier/', 'noir/visual-atlas/drapery-still-life.webp', 'Drapery still life study', 'Drapery, light and material observation for drawing practice.'],
  ['/biblioteca/', 'noir/visual-atlas/graphite-texture.webp', 'Graphite texture study', 'Graphite surface and tonal texture for visual research.'],
  ['/biblioteca/', 'noir/visual-atlas/iris-study.webp', 'Iris and eye study', 'Eye observation, anatomy and drawing study.'],
  ['/historia-da-arte/', 'noir/visual-atlas/moonlit-landscape.webp', 'Moonlit landscape study', 'Atmosphere, value and nocturnal landscape study.'],
  ['/bancos/', 'noir/visual-atlas/museum-gallery.webp', 'Museum gallery research', 'Museum and archive discovery for art-history research.'],
  ['/cadernos/', 'noir/visual-atlas/open-sketchbook.webp', 'Open sketchbook', 'Sketchbook practice and observational drawing notes.'],
  ['/cadernos/', 'noir/visual-atlas/tools-paper.webp', 'Drawing tools and paper', 'Drawing materials and studio practice.']
];
const esc=(value:string)=>value.replace(/[&<>"']/g,(ch)=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[ch]||ch));
export async function GET(){
  const body=rows.map(([page,image,title,caption])=>`<url><loc>${SITE}${page}</loc><image:image><image:loc>${SITE}/${image}</image:loc><image:title>${esc(title)}</image:title><image:caption>${esc(caption)}</image:caption></image:image></url>`).join('');
  return new Response(`<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">${body}</urlset>`,{headers:{'Content-Type':'application/xml; charset=utf-8'}});
}
