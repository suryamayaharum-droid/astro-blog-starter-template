export type OpenLibrarySource = {
  creator: string;
  title: string;
  source: string;
  url: string;
  observe: string;
  rights: string;
};

export type OpenLibraryCollection = {
  id: string;
  kicker: string;
  title: string;
  thesis: string;
  rule: string;
  destination: string;
  sources: OpenLibrarySource[];
};

export const openLibraryCollections: OpenLibraryCollection[] = [
  {
    id: "caderno-como-universo",
    kicker: "CADERNOS NOIR",
    title: "Caderno como universo",
    thesis: "O sketchbook como sistema de pensamento: ensaio, memória, observação e seleção — não miniatura de portfólio.",
    rule: "Comparar sequências e decisões. Uma página importa também pelo que vem antes e depois dela.",
    destination: "Sketchbook · repertório · memória",
    sources: [
      {
        creator: "Leo Gestel",
        title: "Schetsboek — 21 studies, 1934–1936",
        source: "Rijksmuseum",
        url: "https://www.rijksmuseum.nl/en/collection/object/Schetsboek--8ac2d7c29817cfff23657152a2165d3a",
        observe: "Figura, cabeça, cavalos e movimento atravessam técnicas diferentes dentro do mesmo caderno.",
        rights: "Public domain"
      },
      {
        creator: "Leo Gestel",
        title: "Schetsboek — 89 folhas, 1928",
        source: "Rijksmuseum",
        url: "https://www.rijksmuseum.nl/en/collection/object/Schetsboek--e21d9c4f8935d59f830c9d48f68aa808",
        observe: "Animais, retratos, paisagem e postura acumulam repertório sem separar o mundo em categorias rígidas.",
        rights: "Public domain"
      },
      {
        creator: "Sientje Mesdag-van Houten",
        title: "Schetsboek — 39 drawings",
        source: "Rijksmuseum",
        url: "https://www.rijksmuseum.nl/en/collection/object/Schetsboek--a6b3fc72e5b5d89001964aa2b3be9b25",
        observe: "Mãos, figura, interiores, cavalos, carroças e barcos convivem como observação cotidiana.",
        rights: "Public domain"
      },
      {
        creator: "Kenyon Cox",
        title: "Sketchbook Page — seated female figure",
        source: "Cooper Hewitt / Smithsonian",
        url: "https://www.si.edu/object/sketchbook-page%3Achndm_1984-86-4-46",
        observe: "Peso e silêncio corporal resolvidos com economia de grafite.",
        rights: "CC0"
      },
      {
        creator: "William Trost Richards",
        title: "Aug 21 1885: Nature Study (from Sketchbook X)",
        source: "The Met",
        url: "https://www.metmuseum.org/art/collection/search/13709",
        observe: "Notas rápidas e estudos densos coexistem como modos diferentes de permanecer diante da natureza.",
        rights: "Public domain"
      },
      {
        creator: "Thomas Henry Graham",
        title: "Sketchbook recording a tour in Switzerland and France",
        source: "New York Public Library",
        url: "https://digitalcollections.nypl.org/items/3ea3bad0-5432-0130-66f5-58d385a7bbd0",
        observe: "Viagem, arquitetura, paisagem e esboço inacabado viram memória sequencial.",
        rights: "Referência pública; checar jurisdição antes de re-hospedar"
      }
    ]
  },
  {
    id: "anatomias-do-mundo",
    kicker: "ANATOMIA SEM RIGIDEZ",
    title: "Anatomias do mundo",
    thesis: "A anatomia muda quando muda a cultura visual. Comparar sistemas históricos ajuda a separar estrutura corporal de convenção gráfica.",
    rule: "Usar anatomia para compreender forma e função; não transformar o corpo em aparência clínica nem tratar um cânone como universal.",
    destination: "Anatomia · sistemas · história visual",
    sources: [
      {
        creator: "Andreas Vesalius",
        title: "De humani corporis fabrica libri septem",
        source: "National Library of Medicine",
        url: "https://www.nlm.nih.gov/exhibition/historicalanatomies/vesalius_home.html",
        observe: "Dissecção observada, estrutura muscular e esquelética e desenho como investigação.",
        rights: "Public domain"
      },
      {
        creator: "Govard Bidloo / Gérard de Lairesse",
        title: "Ontleding des menschelyken lichaams",
        source: "National Library of Medicine",
        url: "https://www.nlm.nih.gov/exhibition/historicalanatomies/bidloo_home.html",
        observe: "Corpo, objetos de atelier e espaço físico aparecem juntos.",
        rights: "Public domain"
      },
      {
        creator: "Bernhard Siegfried Albinus / Jan Wandelaar",
        title: "Tabulae sceleti et musculorum corporis humani",
        source: "National Library of Medicine",
        url: "https://www.nlm.nih.gov/exhibition/historicalanatomies/albinus_home.html",
        observe: "Medição, grade e proporção convivem com figura inserida em ambiente.",
        rights: "Public domain"
      },
      {
        creator: "Mansur ibn Ilyas",
        title: "Tashrih-i badan-i insan",
        source: "National Library of Medicine",
        url: "https://www.nlm.nih.gov/exhibition/historicalanatomies/mansur_home.html",
        observe: "Ossos, nervos, músculos, veias e artérias organizados como sistemas visuais integrais.",
        rights: "Public domain"
      },
      {
        creator: "Carlo Ruini",
        title: "Anatomia del cavallo",
        source: "National Library of Medicine",
        url: "https://www.nlm.nih.gov/exhibition/historicalanatomies/ruini_bio.html",
        observe: "A estrutura interna do cavalo sustenta gesto, peso e volume externo.",
        rights: "Public domain"
      }
    ]
  },
  {
    id: "atelier-historico-aberto",
    kicker: "ATELIER HISTÓRICO",
    title: "Atelier histórico aberto",
    thesis: "Métodos acadêmicos podem treinar precisão, construção e comparação sem determinar a estética final do artista.",
    rule: "Método é ferramenta. Assimilar estrutura; não copiar acabamento nem transformar academia em estilo.",
    destination: "Fundamentos · proporção · construção",
    sources: [
      {
        creator: "Charles Bargue / Jean-Léon Gérôme",
        title: "Cours de dessin — fac-símile público",
        source: "Wikimedia Commons",
        url: "https://commons.wikimedia.org/wiki/File:Charles_Bargue_Drawing_Course_(IA_CharlesBargueDrawingCourse).pdf",
        observe: "Simplificação, proporção, contorno e passagem de relações grandes para valores.",
        rights: "Public domain"
      },
      {
        creator: "George B. Bridgman",
        title: "Constructive Anatomy",
        source: "Wikimedia Commons / Internet Archive",
        url: "https://commons.wikimedia.org/wiki/File:Constructive_anatomy_(IA_cu31924014504371).pdf",
        observe: "Massas, encaixes e relações mecânicas tratam o corpo como arquitetura em movimento.",
        rights: "Public domain"
      },
      {
        creator: "John Henry Vanderpoel",
        title: "The Human Figure",
        source: "Open Library / Internet Archive",
        url: "https://openlibrary.org/books/OL24433783M/The_human_figure",
        observe: "Partes do corpo são estudadas sem perder a leitura da figura inteira.",
        rights: "Scan gratuito; para uso visual preferir ativos explicitamente public domain"
      }
    ]
  },
  {
    id: "maos-sem-formula",
    kicker: "ANATOMIA SEM RIGIDEZ",
    title: "Mãos sem fórmula",
    thesis: "Mão é gesto, função, peso, idade, contato e relação com o corpo — não uma peça anatômica genérica.",
    rule: "Desenhar a mão fazendo alguma coisa. Comparar relações e ações antes de decorar um esquema.",
    destination: "Mãos · gesto · função",
    sources: [
      {
        creator: "Francis Augustus Lathrop",
        title: "Study of Hands",
        source: "Cooper Hewitt / Smithsonian",
        url: "https://www.si.edu/object/study-hands%3Achndm_1914-38-101",
        observe: "Duas mãos em relação revelam gesto, espaço entre formas e suporte tonal.",
        rights: "CC0"
      },
      {
        creator: "Walter Shirlaw",
        title: "Study of Hands of a Violin Player",
        source: "Cooper Hewitt / Smithsonian",
        url: "https://www.si.edu/object/study-hands-violin-player%3Achndm_1912-16-4",
        observe: "A anatomia aparece através da ação de tocar, segurar e orientar o objeto.",
        rights: "CC0"
      },
      {
        creator: "Edwin Howland Blashfield",
        title: "Studies of Hands",
        source: "Cooper Hewitt / Smithsonian",
        url: "https://www.si.edu/object/studies-hands%3Achndm_1969-112-1-a",
        observe: "Oito posições em carvão constroem repertório por variação de ângulo.",
        rights: "CC0"
      },
      {
        creator: "Daniel Huntington",
        title: "Study of Hands for Elderly Woman in Communion of the Sick",
        source: "Cooper Hewitt / Smithsonian",
        url: "https://www.si.edu/object/study-hands-elderly-woman-communion-sick%3Achndm_1942-50-52",
        observe: "Peso, idade e contato aparecem antes do detalhe anatômico.",
        rights: "CC0"
      },
      {
        creator: "Antoine Watteau",
        title: "Three Studies of a Woman's Head and a Study of Hands",
        source: "National Gallery of Art",
        url: "https://www.nga.gov/artworks/47120-three-studies-womans-head-and-study-hands-recto",
        observe: "Expressão facial e gesto manual são investigados como uma presença única.",
        rights: "Public domain"
      },
      {
        creator: "Enoch Wood Perry, Jr.",
        title: "Studies of Hands",
        source: "National Gallery of Art",
        url: "https://www.nga.gov/artworks/182227-studies-hands-recto",
        observe: "A própria folha vira comparação entre fechamento, repouso e direção.",
        rights: "Public domain"
      }
    ]
  },
  {
    id: "cabeca-em-variacao",
    kicker: "EXPRESSÃO",
    title: "Cabeça em variação",
    thesis: "Perfil, inclinação, idade e expressão mudam sem exigir um rosto-padrão. O objetivo é observar relações, não diagnosticar pessoas.",
    rule: "Sem fisiognomia determinista: nunca inferir caráter, inteligência ou personalidade a partir de traços físicos.",
    destination: "Cabeça · expressão · direção",
    sources: [
      {
        creator: "John Singer Sargent",
        title: "Studies of a Man's Head",
        source: "National Gallery of Art",
        url: "https://www.nga.gov/artworks/184327-studies-mans-head",
        observe: "O mesmo rosto muda inclinação, olhar e eixo do pescoço sem perder identidade.",
        rights: "Public domain"
      },
      {
        creator: "Daniel Huntington",
        title: "Recruit; Two Studies of Heads",
        source: "National Gallery of Art",
        url: "https://www.nga.gov/artworks/57012-recruit-two-studies-heads",
        observe: "Figura inteira e estudos de cabeça ligam leitura facial à atitude corporal.",
        rights: "Public domain"
      },
      {
        creator: "Jean-Jacques de Boissieu",
        title: "Seven Studies of Heads",
        source: "National Gallery of Art",
        url: "https://www.nga.gov/artworks/72031-seven-studies-heads",
        observe: "Idade, barba, olhos, chapéu e direção criam uma série comparativa de diferenças visíveis.",
        rights: "Public domain"
      },
      {
        creator: "Joseph-Ferdinand Lancrenon",
        title: "Study of Heads for Castor and Pollux Freeing Helen",
        source: "The Met",
        url: "https://www.metmuseum.org/art/collection/search/387996",
        observe: "Expressão facial aparece dentro de uma sequência preparatória maior: composição, figura e drapeado.",
        rights: "Public domain"
      },
      {
        creator: "Karel Dujardin",
        title: "Study of heads in profile view",
        source: "The Met",
        url: "https://www.metmuseum.org/art/collection/search/399419",
        observe: "Perfis pequenos e sobrepostos mostram como silhueta e distância sustentam relação.",
        rights: "Public domain"
      },
      {
        creator: "Carlo Marchionni",
        title: "Studies of Heads",
        source: "Cooper Hewitt / Smithsonian",
        url: "https://www.si.edu/object/studies-heads%3Achndm_1938-88-7294",
        observe: "Direções de cabeça e exagero controlado ajudam a perceber estrutura.",
        rights: "CC0"
      }
    ]
  }
];
