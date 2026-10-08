export type VisualStudy = {
  id: string;
  title: string;
  theme: string;
  file: string;
  alt: string;
  caption: string;
  href: string;
  link: string;
  generated: boolean;
  en?: {title:string;theme:string;alt:string;caption:string;href:string;link:string};
  es?: {title:string;theme:string;alt:string;caption:string;href:string;link:string};
};

const generatedCollection = "noir/visual-atlas/collections/";
const visualAtlas = "noir/visual-atlas/";

export const visualStudyCollection: VisualStudy[] = [
  {
    id: "arquivo-caderno",
    title: "Caderno aberto",
    theme: "Arquivo · papel · processo",
    file: generatedCollection + "arquivo-caderno.webp",
    alt: "Caderno de páginas vazias, lápis, carvão e lupa sobre uma mesa escura de ateliê.",
    caption: "Composição editorial criada com assistência de IA; não é documento histórico.",
    href: "sketchbooks/",
    link: "Folhear cadernos",
    generated: true,
    en: {title:"Open sketchbook",theme:"Archive · paper · process",alt:"An open blank sketchbook, pencils, charcoal and a magnifier on a dark atelier table.",caption:"Editorial composition made with AI assistance; not a historical document.",href:"en/drawing/",link:"Browse drawing practice"},
    es: {title:"Cuaderno abierto",theme:"Archivo · papel · proceso",alt:"Cuaderno abierto de páginas vacías, lápices, carbón y lupa sobre una mesa oscura de taller.",caption:"Composición editorial creada con asistencia de IA; no es un documento histórico.",href:"es/dibujo/",link:"Explorar la práctica"},
  },
  {
    id: "botanica-iris",
    title: "Íris em carvão",
    theme: "Botânica · ritmo · ornamento",
    file: generatedCollection + "botanica-iris.webp",
    alt: "Estudo contemporâneo de uma íris e folhas em grafite sobre papel envelhecido.",
    caption: "Estudo editorial criado com assistência de IA; não é obra de acervo.",
    href: "bancos/flor-ornamento/",
    link: "Estudar botânica",
    generated: true,
    en: {title:"Charcoal iris",theme:"Botany · rhythm · ornament",alt:"Contemporary graphite study of an iris and leaves on aged paper.",caption:"Editorial study made with AI assistance; not a collection artwork.",href:"en/museums/",link:"Explore museum sources"},
    es: {title:"Lirio al carbón",theme:"Botánica · ritmo · ornamento",alt:"Estudio contemporáneo de un lirio y sus hojas en grafito sobre papel envejecido.",caption:"Estudio editorial creado con asistencia de IA; no es una obra de colección.",href:"es/museos/",link:"Explorar fuentes de museos"},
  },
  {
    id: "paisagem-maritima",
    title: "Mar e atmosfera",
    theme: "Paisagem · linha · espaço",
    file: generatedCollection + "paisagem-maritima.webp",
    alt: "Paisagem marítima contemporânea construída com massas de carvão e luz sobre o oceano.",
    caption: "Estudo editorial criado com assistência de IA; não é gravura histórica.",
    href: "bancos/linha-japonesa/",
    link: "Estudar linha e paisagem",
    generated: true,
    en: {title:"Sea and atmosphere",theme:"Landscape · line · space",alt:"Contemporary seascape built from charcoal-like masses and reflected light.",caption:"Editorial study made with AI assistance; not a historical print.",href:"en/museums/",link:"Explore museum sources"},
    es: {title:"Mar y atmósfera",theme:"Paisaje · línea · espacio",alt:"Paisaje marítimo contemporáneo construido con masas de carbón y luz sobre el océano.",caption:"Estudio editorial creado con asistencia de IA; no es un grabado histórico.",href:"es/museos/",link:"Explorar fuentes de museos"},
  },
  {
    id: "estudo-tonal",
    title: "Pera, tecido e volume",
    theme: "Forma · luz · valor",
    file: generatedCollection + "estudo-tonal.webp",
    alt: "Natureza-morta contemporânea de pera, tecido, esfera e tigela em luz lateral.",
    caption: "Estudo editorial criado com assistência de IA; não é obra histórica.",
    href: "colecoes/estudo-tonal/",
    link: "Estudar forma e luz",
    generated: true,
    en: {title:"Pear, cloth and volume",theme:"Form · light · value",alt:"Contemporary still life of a pear, cloth, sphere and bowl under side light.",caption:"Editorial study made with AI assistance; not a historical artwork.",href:"en/drawing/",link:"Explore drawing practice"},
    es: {title:"Pera, tela y volumen",theme:"Forma · luz · valor",alt:"Naturaleza muerta contemporánea de una pera, tela, esfera y cuenco bajo luz lateral.",caption:"Estudio editorial creado con asistencia de IA; no es una obra histórica.",href:"es/dibujo/",link:"Explorar la práctica"},
  },
  {
    id: "arquivo-bahia",
    title: "Arquivo da Bahia",
    theme: "Brasil · cartografia · memória gráfica",
    file: generatedCollection + "arquivo-bahia.webp",
    alt: "Mesa de pesquisa com papéis de contornos costeiros abstratos, folha botânica e rolo de impressão, inspirada na Bahia.",
    caption: "Composição editorial criada com assistência de IA; não é mapa nem documento de acervo.",
    href: "bancos/brasil-memoria/",
    link: "Estudar memória gráfica",
    generated: true,
    en: {title:"Bahia archive",theme:"Brazil · cartography · graphic memory",alt:"Research table with abstract coastal contours, botanical leaf and printing roller, inspired by Bahia.",caption:"Editorial composition made with AI assistance; not a map or collection document.",href:"en/brazilian-visual-culture/",link:"Explore Brazilian visual culture"},
    es: {title:"Archivo de Bahía",theme:"Brasil · cartografía · memoria gráfica",alt:"Mesa de investigación con contornos costeros abstractos, hoja botánica y rodillo de impresión, inspirada en Bahía.",caption:"Composición editorial creada con asistencia de IA; no es un mapa ni un documento de acervo.",href:"es/cultura-visual-brasilena/",link:"Explorar cultura visual brasileña"},
  },
];

export const institutionalBankCovers: Record<string, VisualStudy> = {
  aic: visualStudyCollection[3],
  bndigital: visualStudyCollection[4],
  cma: visualStudyCollection[1],
  europeana: visualStudyCollection[0],
  getty: visualStudyCollection[3],
  loc: visualStudyCollection[0],
  met: visualStudyCollection[3],
  nga: visualStudyCollection[2],
  nypl: visualStudyCollection[0],
  "paris-musees": visualStudyCollection[2],
  rijks: visualStudyCollection[2],
  smithsonian: visualStudyCollection[1],
  walters: visualStudyCollection[1],
};

const lensArtwork = [
  {file: visualAtlas + "maos-seis-gestos.webp", alt: "Estudo editorial de mãos em diferentes ações."},
  {file: visualAtlas + "figure-gesture.webp", alt: "Estudo editorial de uma figura vestida, da linha de ação à forma."},
  {file: visualAtlas + "harum-cover-study-adam.webp", alt: "Estudo editorial de figura sentada e tecido em carvão."},
  {file: visualAtlas + "estudo-tonal-pera.webp", alt: "Estudo editorial de pera, tecido e massas de luz e sombra."},
  {file: visualAtlas + "drapery-still-life.webp", alt: "Estudo editorial de tecido, volumes geométricos e luz lateral."},
  {file: visualAtlas + "iris-study.webp", alt: "Estudo editorial de íris e folhas em linha e hachura."},
  {file: visualAtlas + "collections/botanica-iris.webp", alt: "Composição editorial de botânica, desenho e papel de arquivo."},
  {file: visualAtlas + "theme-japanese-line.webp", alt: "Paisagem editorial em linha, onda e espaço inspirado na gravura japonesa."},
  {file: visualAtlas + "moonlit-landscape.webp", alt: "Paisagem editorial de ponte, água, montanhas e luz noturna."},
  {file: visualAtlas + "brasil-acervo-editorial.webp", alt: "Mesa editorial de pesquisa com mapa, papel e vestígio botânico."},
  {file: visualAtlas + "theme-brazil-memory.webp", alt: "Composição editorial de mapas, folhas e memória visual da Bahia."},
  {file: visualAtlas + "collections/arquivo-bahia.webp", alt: "Composição editorial de arquivo, cartografia e memória gráfica da Bahia."},
  {file: visualAtlas + "open-sketchbook.webp", alt: "Caderno editorial aberto com estudos de linha e composição."},
  {file: visualAtlas + "collections/arquivo-caderno.webp", alt: "Caderno editorial aberto sobre uma mesa de pesquisa."},
  {file: visualAtlas + "harum-cover-metalpoint.webp", alt: "Estudo editorial de retrato, ponta metálica e ferramentas de desenho."},
  {file: visualAtlas + "bndigital-study-atlas.webp", alt: "Painel editorial sobre cidade, cartografia, livro, botânica e retrato brasileiros."},
  {file: visualAtlas + "collections/estudo-tonal.webp", alt: "Natureza-morta editorial de pera, tecido, esfera e tigela."},
  {file: visualAtlas + "collections/paisagem-maritima.webp", alt: "Estudo editorial de mar, horizonte e atmosfera."},
];

function candidatesForLens(label: string, bankId: string) {
  const name = label.toLocaleLowerCase("pt-BR");
  if (bankId === "bndigital") {
    if (/bahia/.test(name)) return [lensArtwork[11], lensArtwork[10], lensArtwork[17], lensArtwork[15]];
    if (/cartograf|mapa|map/.test(name)) return [lensArtwork[9], lensArtwork[10], lensArtwork[15], lensArtwork[11]];
    if (/bot[aâ]nic|flora|flower/.test(name)) return [lensArtwork[6], lensArtwork[5], lensArtwork[10]];
    if (/impr|peri[oó]d|livro|document|arquivo|archiv/.test(name)) return [lensArtwork[13], lensArtwork[12], lensArtwork[14], lensArtwork[15]];
    if (/retrato|portrait/.test(name)) return [lensArtwork[2], lensArtwork[14], lensArtwork[1], lensArtwork[15]];
    if (/brasil|oitocent|hist[oó]ric/.test(name)) return [lensArtwork[15], lensArtwork[9], lensArtwork[11], lensArtwork[12]];
  }
  if (/bot[aâ]nic|flora|flower|folha|plant/.test(name)) return [lensArtwork[6], lensArtwork[5], lensArtwork[10]];
  if (/m[aã]o|gesto|hand|gesture|press[aã]o|contato/.test(name)) return [lensArtwork[0], lensArtwork[1], lensArtwork[2]];
  if (/figura|anatom|portrait|retrato|pose|fashion|moda|traje|sculpt|escultur|rembrandt|mestre|master/.test(name)) return [lensArtwork[1], lensArtwork[2], lensArtwork[14], lensArtwork[0]];
  if (/carv[aã]o|tonal|luz|light|valor|value|color|cor|drape|tecido|textil|mat[eé]ria|still.life|natureza|volume|interior|ateli[eê]|studio/.test(name)) return [lensArtwork[3], lensArtwork[4], lensArtwork[16], lensArtwork[14]];
  if (/mar|paisag|onda|jap[aã]o|[aã]sia|wave|landscape/.test(name)) return [lensArtwork[7], lensArtwork[8], lensArtwork[17], lensArtwork[10]];
  if (/map|cartograf|territ|bahia|brazil|brasil|architecture|arquitet|paris|cidade|city/.test(name)) return [lensArtwork[10], lensArtwork[9], lensArtwork[15], lensArtwork[11], lensArtwork[8]];
  if (/gravura|print|etch|metalpoint|linha|line|ink|reprodu|poster|cartaz|dessin|desenho|drawing/.test(name)) return [lensArtwork[14], lensArtwork[7], lensArtwork[13], lensArtwork[12], lensArtwork[15]];
  if (/foto|photograph|mem[oó]ria|arquivo|archiv|manuscript|manuscrito|book|livro|press|imprensa|design|caderno|document|free.to.use|dom[ií]nio.p[uú]blico/.test(name)) return [lensArtwork[13], lensArtwork[12], lensArtwork[9], lensArtwork[15], lensArtwork[2]];
  return [];
}

export function artworkForLens(label: string, bankId: string, index: number, usedFiles: Set<string> = new Set()) {
  const start = [...bankId].reduce((sum, char) => sum + char.charCodeAt(0), 0) % lensArtwork.length;
  const rotatedDeck = [...lensArtwork.slice(start), ...lensArtwork.slice(0, start)];
  const preferred = candidatesForLens(label, bankId);
  const ordered = [...preferred, ...rotatedDeck];
  const artwork = ordered.find((item) => !usedFiles.has(item.file)) || ordered[index % ordered.length] || lensArtwork[index % lensArtwork.length];
  usedFiles.add(artwork.file);
  return artwork;
}

const companionStudy=(id:string,title:string,theme:string,file:string,alt:string,href:string,link:string):VisualStudy=>({
  id,title,theme,file:visualAtlas+file,alt,
  caption:"Composição temática HARUM NOIR; não é folha do caderno histórico.",
  href,link,generated:false,
});

export const sketchbookCompanionsByShelf: Record<string, VisualStudy[]> = {
  "Figura & composição": [
    {id:"figura-linha",title:"Linha de ação",theme:"Figura · gesto",file:visualAtlas+"figure-gesture.webp",alt:"Estudo editorial de uma figura vestida em etapas de construção.",caption:"Composição temática HARUM NOIR; não é folha do caderno histórico.",href:"colecoes/gesto-figura/",link:"Estudo de figura",generated:false},
    {id:"maos-acao",title:"Mãos em ação",theme:"Gesto · contato",file:visualAtlas+"maos-seis-gestos.webp",alt:"Seis estudos editoriais de mãos em ações distintas.",caption:"Composição temática HARUM NOIR; não é folha do caderno histórico.",href:"maos/",link:"Estudo de mãos",generated:false},
    companionStudy("mãos-carvão","Mãos e carvão","Pressão · marca","harum-noir-hands-study.webp","Estudo editorial de mãos e ferramentas de desenho em carvão.","maos/","Ler gesto"),
    companionStudy("olhar-estrutura","Olhar construído","Estrutura · volume","harum-noir-caderno-olhar.webp","Estudo editorial de olho construído sobre uma esfera.","colecoes/estudo-tonal/","Estudar volume"),
  ],
  "Escultura & viagem": [
    {id:"arquivo-caderno-companion",title:"Mesa de pesquisa",theme:"Caderno · memória",file:visualStudyCollection[0].file,alt:visualStudyCollection[0].alt,caption:"Composição criada com assistência de IA; não é folha do caderno histórico.",href:"biblioteca/",link:"Abrir Biblioteca",generated:true},
    {id:"paisagem-viagem",title:"Paisagem e distância",theme:"Viagem · atmosfera",file:visualStudyCollection[2].file,alt:visualStudyCollection[2].alt,caption:"Estudo criado com assistência de IA; não é desenho histórico.",href:"bancos/linha-japonesa/",link:"Estudar paisagem",generated:true},
    companionStudy("galeria-viagem","Galeria e percurso","Escultura · contexto","museum-gallery.webp","Cena editorial de galeria para pesquisa de acervo.","museus/","Abrir Museus"),
    companionStudy("mesa-viagem","Mesa de ateliê","Observação · materiais","atelier-desk.webp","Mesa editorial de ateliê com ferramentas e papel.","atelier/","Abrir Ateliê"),
  ],
  "Memória & anotação": [
    {id:"arquivo-aberto",title:"Página em aberto",theme:"Arquivo · processo",file:visualStudyCollection[0].file,alt:visualStudyCollection[0].alt,caption:"Composição criada com assistência de IA; não é folha do caderno histórico.",href:"biblioteca/",link:"Abrir Biblioteca",generated:true},
    {id:"memoria-bahia",title:"Memória gráfica",theme:"Brasil · arquivo",file:visualStudyCollection[4].file,alt:visualStudyCollection[4].alt,caption:"Composição criada com assistência de IA; não é documento de acervo.",href:"bancos/brasil-memoria/",link:"Estudar arquivo",generated:true},
    companionStudy("caderno-aberto","Caderno de processo","Memória · sequência","open-sketchbook.webp","Caderno aberto em uma composição editorial de ateliê.","cadernos/","Abrir Cadernos"),
    companionStudy("materiais-memória","Ferramentas e papel","Vestígio · matéria","tools-paper.webp","Ferramentas de desenho e papel em composição editorial.","cadernos/vestigio/","Abrir Vestígio"),
  ],
  "Paisagem & atmosfera": [
    {id:"mar-atmosfera",title:"Mar e ritmo",theme:"Paisagem · carvão",file:visualStudyCollection[2].file,alt:visualStudyCollection[2].alt,caption:"Estudo criado com assistência de IA; não é folha do caderno histórico.",href:"bancos/linha-japonesa/",link:"Estudar paisagem",generated:true},
    {id:"paisagem-noite",title:"Paisagem noturna",theme:"Luz · silêncio",file:visualAtlas+"moonlit-landscape.webp",alt:"Paisagem noturna em estudo editorial de carvão.",caption:"Composição temática HARUM NOIR; não é folha do caderno histórico.",href:"outliers/",link:"Abrir Outliers",generated:false},
    companionStudy("linha-mar","Linha e vazio","Paisagem · contorno","theme-japanese-line.webp","Paisagem didática original com ritmo de ondas e grandes áreas vazias.","bancos/linha-japonesa/","Estudar linha"),
    companionStudy("bahia-paisagem","Costa e memória","Paisagem · território","brasil-acervo-editorial.webp","Composição editorial de arquivo visual brasileiro, sem representar documento histórico.","bancos/brasil-memoria/","Abrir memória gráfica"),
  ],
  "Matéria & linguagem": [
    {id:"estudo-valor",title:"Forma sob uma luz",theme:"Valor · volume",file:visualStudyCollection[3].file,alt:visualStudyCollection[3].alt,caption:"Estudo criado com assistência de IA; não é folha do caderno histórico.",href:"colecoes/estudo-tonal/",link:"Estudar valor",generated:true},
    {id:"iris-materia",title:"Ritmo botânico",theme:"Grafite · superfície",file:visualStudyCollection[1].file,alt:visualStudyCollection[1].alt,caption:"Estudo criado com assistência de IA; não é desenho histórico.",href:"bancos/flor-ornamento/",link:"Estudar botânica",generated:true},
    companionStudy("tecido-matéria","Tecido e dobra","Matéria · volume","drapery-still-life.webp","Estudo de tecido, luz e sombra em carvão.","colecoes/estudo-tonal/","Estudar forma"),
    companionStudy("papel-matéria","Papel e ferramentas","Marca · apagamento","tools-paper.webp","Ferramentas e papel em um estudo editorial de desenho.","cadernos/vestigio/","Estudar matéria"),
  ],
  "Observação & gesto": [
    {id:"gesto-maos",title:"A mão e a pressão",theme:"Ação · contato",file:visualAtlas+"maos-seis-gestos.webp",alt:"Seis estudos editoriais de mãos em ações distintas.",caption:"Composição temática HARUM NOIR; não é folha do caderno histórico.",href:"maos/",link:"Estudar gesto",generated:false},
    {id:"gesto-tonal",title:"Peso e volume",theme:"Forma · luz",file:visualStudyCollection[3].file,alt:visualStudyCollection[3].alt,caption:"Estudo criado com assistência de IA; não é folha do caderno histórico.",href:"colecoes/estudo-tonal/",link:"Estudar valor",generated:true},
    companionStudy("gesto-figura","Figura em equilíbrio","Ação · apoio","figure-gesture.webp","Estudo editorial de uma figura vestida em quatro etapas.","colecoes/gesto-figura/","Estudar figura"),
    companionStudy("gesto-atelier","A mão no ateliê","Processo · carvão","harum-noir-caderno-estudo.webp","Estudo editorial de ateliê com mão, carvão e caderno.","maos/","Voltar ao gesto"),
  ],
};
