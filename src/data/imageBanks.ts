export type ImageBankLens = {
  label: string;
  query: string;
  note: string;
};

export type ImageBank = {
  id: string;
  name: string;
  place: string;
  kind: "museum"|"network"|"archive";
  access: string;
  rights: string;
  collectionUrl: string;
  rightsUrl: string;
  docsUrl?: string;
  liveFederated: boolean;
  strengths: string[];
  periods: string[];
  lenses: ImageBankLens[];
  caution: string;
};

const commonLenses: ImageBankLens[] = [
  {label:"Mãos & gesto",query:"hands gesture drawing",note:"mãos, dedos, peso, contato e estudos preparatórios"},
  {label:"Figura & anatomia",query:"figure anatomy study",note:"estrutura, pose, torso, estudos acadêmicos"},
  {label:"Carvão & desenho",query:"charcoal drawing",note:"massa tonal, marca, papel e processo"},
  {label:"Retrato",query:"portrait drawing",note:"fisionomia, luz, enquadramento e presença"},
  {label:"Botânica",query:"flowers botanical drawing",note:"ritmo, ornamento, ramo e construção vegetal"},
  {label:"Gravura & linha",query:"print engraving etching",note:"contorno, hachura, recorte e reprodução"}
];

export const imageBanks: ImageBank[] = [
  {
    id:"met",
    name:"The Metropolitan Museum of Art",
    place:"New York · EUA",
    kind:"museum",
    access:"Open Access + API sem chave",
    rights:"Filtre pelas fichas marcadas Public Domain / Open Access.",
    collectionUrl:"https://www.metmuseum.org/art/collection",
    rightsUrl:"https://www.metmuseum.org/hubs/open-access",
    docsUrl:"https://metmuseum.github.io/",
    liveFederated:true,
    strengths:["desenho europeu","antiguidade","arte asiática","escultura","gravura","arte decorativa"],
    periods:["Antiguidade","Medieval","Renascimento","Barroco","século XIX","Ukiyo-e"],
    lenses:commonLenses,
    caution:"O texto curatorial e a imagem de uma obra não têm necessariamente a mesma licença. Leia a ficha."
  },
  {
    id:"aic",
    name:"Art Institute of Chicago",
    place:"Chicago · EUA",
    kind:"museum",
    access:"Open Access + REST + IIIF",
    rights:"Use obras com is_public_domain=true.",
    collectionUrl:"https://www.artic.edu/collection",
    rightsUrl:"https://www.artic.edu/open-access/open-access-images",
    docsUrl:"https://api.artic.edu/docs/",
    liveFederated:true,
    strengths:["Impressionismo","Pós-Impressionismo","gravura","desenho","modernismo","fotografia"],
    periods:["século XIX","Impressionismo","Pós-Impressionismo","Modernismos"],
    lenses:[
      ...commonLenses,
      {label:"Cor & luz",query:"impressionism light color",note:"pincelada, atmosfera, série e instante"}
    ],
    caution:"O IIIF facilita o estudo técnico, mas a condição de domínio público deve continuar visível no registro."
  },
  {
    id:"cma",
    name:"Cleveland Museum of Art",
    place:"Cleveland · EUA",
    kind:"museum",
    access:"Open Access API + CC0",
    rights:"Prefira registros com share_license_status=CC0.",
    collectionUrl:"https://www.clevelandart.org/art/collection",
    rightsUrl:"https://www.clevelandart.org/open-access",
    docsUrl:"https://openaccess-api.clevelandart.org/",
    liveFederated:true,
    strengths:["arte asiática","medieval","gravura","desenho","escultura","arte decorativa"],
    periods:["Antiguidade","Medieval","Ásia","Renascimento","Barroco","século XIX"],
    lenses:commonLenses,
    caution:"CC0 nos dados não autoriza automaticamente qualquer ativo externo associado; siga o status da própria imagem."
  },
  {
    id:"rijks",
    name:"Rijksmuseum",
    place:"Amsterdam · Países Baixos",
    kind:"museum",
    access:"Collection Online + Linked Data + IIIF",
    rights:"Registros podem indicar Public Domain, CC0, CC BY ou restrição.",
    collectionUrl:"https://www.rijksmuseum.nl/en/collection",
    rightsUrl:"https://data.rijksmuseum.nl/",
    docsUrl:"https://data.rijksmuseum.nl/",
    liveFederated:false,
    strengths:["mestres holandeses","gravura","desenho","artes decorativas","Japão","fotografia histórica"],
    periods:["Renascimento do Norte","Barroco holandês","século XIX","Ukiyo-e"],
    lenses:[
      {label:"Rembrandt",query:"Rembrandt drawing",note:"luz, gravura, retrato e estudo"},
      {label:"Ateliê & interior",query:"interior studio light",note:"luz de janela, objetos, silêncio e atmosfera"},
      {label:"Gravura",query:"etching print",note:"linha, hachura e impressão"},
      {label:"Japão",query:"Japanese print",note:"recorte, vazio, padrão e paisagem"},
      {label:"Natureza-morta",query:"still life",note:"matéria, objeto e composição"},
      {label:"Desenho",query:"drawing study",note:"processo, gesto e preparação"}
    ],
    caution:"Não trate o Rijks como um banco inteiramente livre; verifique o rótulo de direitos de cada objeto."
  },
  {
    id:"getty",
    name:"J. Paul Getty Museum",
    place:"Los Angeles · EUA",
    kind:"museum",
    access:"Open Content + Linked.Art + SPARQL + IIIF",
    rights:"Dados abertos e muitas imagens de obras em domínio público; confirme cada ativo.",
    collectionUrl:"https://www.getty.edu/art/collection/",
    rightsUrl:"https://www.getty.edu/projects/open-content-program/",
    docsUrl:"https://data.getty.edu/museum/collection/docs/",
    liveFederated:false,
    strengths:["desenho europeu","pintura","escultura","manuscritos","fotografia","proveniência"],
    periods:["Medieval","Renascimento","Barroco","Rococó","século XIX"],
    lenses:[
      {label:"Desenho de mestre",query:"master drawing",note:"estudos, preparação e decisão"},
      {label:"Drapeado",query:"drapery study",note:"peso, dobra e direção"},
      {label:"Escultura",query:"sculpture study",note:"massa, perfil e volume"},
      {label:"Manuscritos",query:"illuminated manuscript",note:"imagem, ouro, página e ornamento"},
      {label:"Retrato",query:"portrait",note:"pose, superfície e presença"},
      {label:"Fotografia",query:"photography",note:"enquadramento e memória visual"}
    ],
    caution:"Os dados Linked Open Data e os direitos das imagens são camadas diferentes."
  },
  {
    id:"smithsonian",
    name:"Smithsonian Open Access",
    place:"Washington, D.C. · EUA",
    kind:"network",
    access:"Open Access + API com chave gratuita",
    rights:"Procure a marca CC0 no item e na mídia.",
    collectionUrl:"https://www.si.edu/openaccess",
    rightsUrl:"https://www.si.edu/openaccess/faq",
    docsUrl:"https://www.si.edu/openaccess/devtools",
    liveFederated:false,
    strengths:["arte","design","fotografia","objetos","história","ciência visual"],
    periods:["multiperíodo","arte americana","design","fotografia","arquivo"],
    lenses:[
      {label:"Desenho",query:"drawing",note:"acervos cruzados entre museus e arquivos"},
      {label:"Design",query:"design sketch",note:"processo, objeto e construção"},
      {label:"Fotografia",query:"portrait photography",note:"pose, enquadramento e documentação"},
      {label:"Botânica",query:"botanical illustration",note:"ciência, desenho e padrão"},
      {label:"Textil & padrão",query:"textile pattern",note:"ornamento, repetição e superfície"},
      {label:"Arquivo de artista",query:"artist sketchbook",note:"cadernos, cartas e processo"}
    ],
    caution:"A API exige chave; o HARUM NOIR não coloca credenciais no cliente ou no Git."
  },
  {
    id:"nga",
    name:"National Gallery of Art",
    place:"Washington, D.C. · EUA",
    kind:"museum",
    access:"Open Access + dataset CC0",
    rights:"Dados factuais CC0; use imagens sinalizadas como Open Access.",
    collectionUrl:"https://www.nga.gov/artworks",
    rightsUrl:"https://www.nga.gov/artworks/free-images-and-open-access",
    docsUrl:"https://github.com/NationalGalleryOfArt/opendata",
    liveFederated:false,
    strengths:["pintura europeia","desenho","gravura","arte americana","escultura"],
    periods:["Renascimento","Barroco","Rococó","século XIX","Modernismos"],
    lenses:commonLenses,
    caution:"O dataset é excelente para índice e pesquisa, mas a reutilização visual continua vinculada ao status da imagem."
  },
  {
    id:"paris-musees",
    name:"Paris Musées Collections",
    place:"Paris · França",
    kind:"network",
    access:"Coleções online + Open Content",
    rights:"Grande conjunto de reproduções de obras em domínio público com marca Open Content/CC0.",
    collectionUrl:"https://www.parismuseescollections.paris.fr/en",
    rightsUrl:"https://www.parismuseescollections.paris.fr/en",
    liveFederated:false,
    strengths:["arte francesa","desenho","moda","cartaz","fotografia","história de Paris"],
    periods:["Rococó","Neoclassicismo","Romantismo","século XIX","Modernismos"],
    lenses:[
      {label:"Desenho francês",query:"dessin",note:"linha, atelier e estudo"},
      {label:"Moda",query:"mode",note:"silhueta, tecido e época"},
      {label:"Cartazes",query:"affiche",note:"tipografia, cor e composição"},
      {label:"Paris",query:"Paris",note:"cidade, arquitetura e cotidiano"},
      {label:"Retrato",query:"portrait",note:"pose, identidade e moda"},
      {label:"Fotografia",query:"photographie",note:"arquivo, gesto e enquadramento"}
    ],
    caution:"Mesmo em um portal Open Content, confirme a marca do objeto antes de reutilizar uma reprodução."
  },
  {
    id:"walters",
    name:"The Walters Art Museum",
    place:"Baltimore · EUA",
    kind:"museum",
    access:"Coleção online + imagens CC0 de obras em domínio público",
    rights:"O museu libera sob CC0 imagens de obras que considera em domínio público, com exceções.",
    collectionUrl:"https://art.thewalters.org/",
    rightsUrl:"https://thewalters.org/about/policies/rights-reproductions/",
    docsUrl:"https://api.thewalters.org/index.html",
    liveFederated:false,
    strengths:["Antiguidade","Medieval","manuscritos","arte islâmica","Ásia","joias e objetos"],
    periods:["Antiguidade","Medieval","mundo islâmico","Ásia","Renascimento"],
    lenses:[
      {label:"Manuscritos",query:"manuscript",note:"página, miniatura, ornamento e narrativa"},
      {label:"Escultura antiga",query:"ancient sculpture",note:"perfil, volume e objeto"},
      {label:"Arte islâmica",query:"Islamic art",note:"padrão, caligrafia e superfície"},
      {label:"Joias",query:"jewelry",note:"escala, detalhe e repetição"},
      {label:"Ásia",query:"Asian art",note:"linha, objeto e iconografia"},
      {label:"Desenho",query:"drawing",note:"estudo e documentação"}
    ],
    caution:"A antiga API v1 foi encerrada; o portal de coleção e os dados estáticos continuam como portas de estudo."
  },
  {
    id:"nypl",
    name:"NYPL Digital Collections",
    place:"New York · EUA",
    kind:"archive",
    access:"Coleções digitais · portal de pesquisa",
    rights:"Há materiais em domínio público/CC0, mas os direitos variam por item.",
    collectionUrl:"https://digitalcollections.nypl.org/",
    rightsUrl:"https://digitalcollections.nypl.org/about",
    docsUrl:"https://api.repo.nypl.org/",
    liveFederated:false,
    strengths:["gravuras","fotografia","mapas","cartazes","livros ilustrados","arquivo urbano"],
    periods:["século XIX","século XX","design gráfico","fotografia","arquivo"],
    lenses:[
      {label:"Cartaz",query:"poster",note:"composição, tipografia e cor"},
      {label:"Fotografia urbana",query:"street photography",note:"gesto, enquadramento e cidade"},
      {label:"Mapas",query:"map",note:"linha, hierarquia e informação"},
      {label:"Moda",query:"fashion",note:"silhueta, época e registro"},
      {label:"Gravura",query:"print",note:"linha, reprodução e circulação"},
      {label:"Livro ilustrado",query:"illustrated book",note:"sequência, página e narrativa"}
    ],
    caution:"A Repository API foi descontinuada em 2026; trate a NYPL como portal/arquivo, não como integração viva."
  },
  {
    id:"bndigital",
    name:"Biblioteca Nacional Digital",
    place:"Rio de Janeiro · Brasil",
    kind:"archive",
    access:"Acervo digital público · milhões de documentos",
    rights:"A BNDigital informa que disponibiliza documentos em domínio público ou com autorização de publicação do titular.",
    collectionUrl:"https://bndigital.bn.gov.br/acervodigital/",
    rightsUrl:"https://bndigital.bn.gov.br/orientacoes-de-uso-de-arquivos-digitais/",
    docsUrl:"https://bndigital.bn.gov.br/",
    liveFederated:false,
    strengths:["iconografia brasileira","gravura","livros","periódicos","cartografia","memória gráfica"],
    periods:["Brasil colonial","Império","século XIX","Primeira República","modernização gráfica"],
    lenses:[
      {label:"Brasil oitocentista",query:"século XIX Brasil gravura",note:"cidade, costumes, arquitetura e circulação impressa"},
      {label:"Bahia",query:"Bahia Salvador gravura",note:"paisagem, arquitetura, porto e memória visual"},
      {label:"Cartografia",query:"mapa Brasil",note:"linha, território, hierarquia e informação"},
      {label:"Imprensa ilustrada",query:"periódico ilustrado",note:"imagem, tipografia e narrativa editorial"},
      {label:"Botânica brasileira",query:"flora Brasil ilustração",note:"desenho científico, forma e repertório vegetal"},
      {label:"Retrato histórico",query:"retrato Brasil século XIX",note:"pose, vestuário e representação social"}
    ],
    caution:"Livre acesso não significa que todo uso seja idêntico; confirme a situação indicada para o documento e siga as orientações de reprodução da Fundação Biblioteca Nacional."
  },
  {
    id:"loc",
    name:"Library of Congress",
    place:"Washington, D.C. · EUA",
    kind:"archive",
    access:"JSON/YAML API pública · sem chave + conjuntos Free to Use and Reuse",
    rights:"A API expõe muitos tipos de item; reutilize apenas materiais cuja própria ficha/coleção indique ausência de restrições conhecidas ou entrada nos conjuntos Free to Use and Reuse.",
    collectionUrl:"https://www.loc.gov/",
    rightsUrl:"https://www.loc.gov/free-to-use/",
    docsUrl:"https://www.loc.gov/apis/json-and-yaml/",
    liveFederated:false,
    strengths:["fotografia","cartaz","mapas","gravura","desenho","livros e arquivo"],
    periods:["século XIX","século XX","design gráfico","fotografia","cartografia"],
    lenses:[
      {label:"Cartazes",query:"posters",note:"composição, tipografia, propaganda e cor"},
      {label:"Fotografia",query:"photographs portrait",note:"pose, gesto, enquadramento e documento"},
      {label:"Mapas",query:"maps",note:"linha, hierarquia, território e legenda"},
      {label:"Desenhos & gravuras",query:"prints drawings",note:"hachura, reprodução e circulação"},
      {label:"Arquitetura",query:"architecture drawings",note:"estrutura, escala e documentação"},
      {label:"Free to Use",query:"free to use and reuse",note:"conjuntos curados pela própria Library of Congress para reutilização"}
    ],
    caution:"A API é aberta, mas os direitos variam por item. Use a ficha de Rights & Access ou os conjuntos Free to Use and Reuse antes de reutilizar mídia."
  },
  {
    id:"europeana",
    name:"Europeana",
    place:"Europa · agregador multinacional",
    kind:"network",
    access:"Agregador de patrimônio cultural + APIs / Linked Data",
    rights:"Cada objeto carrega um rights statement padronizado. Prefira CC0, Public Domain Mark ou outra licença compatível com o uso pretendido.",
    collectionUrl:"https://www.europeana.eu/en",
    rightsUrl:"https://pro.europeana.eu/page/available-rights-statements",
    docsUrl:"https://pro.europeana.eu/page/documentation",
    liveFederated:false,
    strengths:["museus europeus","bibliotecas","arquivos","fotografia","design","patrimônio"],
    periods:["multiperíodo","Europa","design","fotografia","arquivo"],
    lenses:[
      {label:"Domínio público",query:"public domain",note:"filtrar por direitos antes de olhar volume"},
      {label:"Desenho",query:"drawing",note:"comparar instituições e tradições diferentes"},
      {label:"Cartaz & design",query:"poster design",note:"imagem, tipografia e circulação"},
      {label:"Fotografia histórica",query:"historical photography",note:"documento, enquadramento e memória"},
      {label:"Ornamento",query:"ornament pattern",note:"padrão, superfície e repertório"},
      {label:"Moda & traje",query:"fashion costume",note:"silhueta, tecido, época e representação"}
    ],
    caution:"Europeana agrega milhares de instituições: o rights statement é parte essencial do registro. A API de busca usa chave; não expor credenciais no cliente."
  }
];

export const imageBankById = Object.fromEntries(imageBanks.map(x=>[x.id,x])) as Record<string,ImageBank>;


export const artHistoryBankMap: Record<string,string[]> = {
  "origens":["met","walters","cma"],
  "egito-mesopotamia":["met","walters","cma"],
  "grecia-roma":["met","getty","cma"],
  "asia-antiga":["met","cma","walters"],
  "medieval":["getty","walters","met"],
  "renascimento":["met","getty","nga"],
  "maneirismo":["met","getty","nga"],
  "barroco":["rijks","met","nga"],
  "rococo":["paris-musees","getty","met"],
  "neo-romantismo":["paris-musees","nga","met","bndigital"],
  "realismo":["paris-musees","met","aic","bndigital"],
  "ukiyoe":["met","rijks","aic"],
  "impressionismo":["aic","paris-musees","nga"],
  "simbolismo":["aic","paris-musees","met"],
  "modernismos":["aic","nga","paris-musees","bndigital"],
  "pos-guerra":["aic","smithsonian","nga"]
};


export const studyFans = [
  {id:"arquivo-impressos",title:"Arquivo, cartaz & impressão",query:"posters prints maps",thought:"Como uma imagem circula muda o modo como ela é construída.",image:"theme-brazil-memory.webp",alt:"Mesa editorial original com mapa ficcional da Bahia, folha botânica e estudos de porto; não é documento histórico.",practice:"Compare dois formatos impressos. Observe como escala, margem e repetição mudam a leitura.",bankIds:["loc","nypl","bndigital","europeana"]},
  {id:"maos-gesto",title:"Mãos & gesto",query:"hands gesture drawing",thought:"A mão como peso, ação, contato e narrativa.",image:"maos-seis-gestos.webp",alt:"Seis estudos de mãos em ações distintas para observar peso, contato e direção.",practice:"Desenhe uma mão em repouso, toque e pressão; preserve a direção do gesto antes de detalhar os dedos.",bankIds:["met","getty","cma","nga"]},
  {id:"carvao-noite",title:"Carvão & noite",query:"charcoal drawing dark tonal study",thought:"Massa escura, borda perdida, pressão e silêncio.",image:"outlier-redon.webp",alt:"Jardim noturno interpretativo em carvão, criado para estudar massa escura e luz sugerida; não é obra de acervo.",practice:"Faça uma massa escura contínua e recupere luz com borracha em três pontos, variando borda nítida e perdida.",bankIds:["met","aic","paris-musees","nga"]},
  {id:"figura-peso",title:"Figura em peso",query:"figure drawing contrapposto weight",thought:"Eixo, apoio, pelve, caixa torácica e centro de massa.",image:"season-01.webp",alt:"Estudo original de figura adulta vestida com variações de gesto e apoio.",practice:"Marque o pé de apoio, o eixo do tronco e a inclinação da pelve antes de construir a silhueta.",bankIds:["met","getty","cma","aic"]},
  {id:"linha-japonesa",title:"Linha japonesa",query:"Japanese woodblock print ukiyo-e",thought:"Recorte, padrão, vazio e continuidade de contorno.",image:"theme-japanese-line.webp",alt:"Paisagem didática original com ritmo de ondas, contornos recortados e grandes áreas vazias; não reproduz uma gravura histórica.",practice:"Reduza uma paisagem a três planos e teste como repetição de linha e espaço vazio conduzem o olhar.",bankIds:["met","rijks","aic"]},
  {id:"flor-ornamento",title:"Flor, padrão & ornamento",query:"flowers ornament botanical drawing",thought:"Ritmo vegetal, repetição, arabesco e superfície.",image:"iris-study.webp",alt:"Estudo botânico de íris em grafite e carvão para observar ritmo e estrutura vegetal.",practice:"Desenhe um ramo em três escalas: silhueta, ritmo das folhas e detalhe seletivo da flor.",bankIds:["paris-musees","met","cma","walters"]},
  {id:"atelie-luz",title:"Ateliê, luz & silêncio",query:"artist studio interior light drawing",thought:"A luz como estrutura antes do contorno.",image:"atelier-desk.webp",alt:"Mesa de ateliê editorial com ferramentas e papel sob luz lateral.",practice:"Escolha uma única fonte de luz e organize o estudo em massa iluminada, sombra e borda de transição.",bankIds:["rijks","met","nga","getty"]},
  {id:"brasil-memoria",title:"Brasil · memória gráfica",query:"Brasil século XIX gravura desenho",thought:"Paisagem, imprensa, cartografia, costumes e construção visual brasileira.",image:"brasil-acervo-editorial.webp",alt:"Composição editorial assistida por IA inspirada em arquivos visuais brasileiros; não representa documento histórico.",practice:"Cruze mapa, gravura e registro botânico em fontes institucionais. Registre autoria, data e direitos antes de usar qualquer imagem.",bankIds:["bndigital","nypl","paris-musees"]}
];
