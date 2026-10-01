export type ArtHistorySource = {
  name: string;
  url: string;
  access: string;
  note: string;
};

export type ArtHistoryArtist = {
  name: string;
  life?: string;
  focus: string;
  rights?: string;
};

export type ArtHistoryPeriod = {
  id: string;
  dates: string;
  title: string;
  region: string;
  thesis: string;
  construction: string[];
  thought: string;
  curiosity: string;
  study: string;
  diagram: "axis"|"grid"|"triangle"|"diagonal"|"curve"|"rhythm"|"flat"|"fragment";
  diagramLabel: string;
  artists: ArtHistoryArtist[];
};

export const artHistorySources: ArtHistorySource[] = [
  {
    name: "The Met · Heilbrunn Timeline of Art History",
    url: "https://www.metmuseum.org/essays/timeline-of-art-history",
    access: "Cronologias + ensaios",
    note: "Referência institucional para navegar história da arte por tempo, região e tema. O texto é fonte de estudo; não presumir domínio público do conteúdo editorial."
  },
  {
    name: "The Met · Open Access",
    url: "https://www.metmuseum.org/hubs/open-access",
    access: "Imagens OA / CC0",
    note: "Use apenas obras/imagens marcadas como Open Access / Public Domain na ficha do objeto."
  },
  {
    name: "National Gallery of Art · Open Access",
    url: "https://www.nga.gov/artworks/free-images-and-open-access",
    access: "Imagens abertas",
    note: "Mais de 60 mil imagens disponíveis para download aberto; confirme a indicação de Open Access em cada objeto."
  },
  {
    name: "Cleveland Museum of Art · Open Access",
    url: "https://www.clevelandart.org/open-access",
    access: "CC0",
    note: "Imagens de obras em domínio público e dados abertos sob CC0 quando indicados."
  },
  {
    name: "Rijksmuseum · Data Services",
    url: "https://data.rijksmuseum.nl/",
    access: "Public Domain / CC0 / CC BY",
    note: "Grande acervo em alta resolução. Verifique o aviso de direitos de cada registro."
  },
  {
    name: "Getty · Open Content Program",
    url: "https://www.getty.edu/projects/open-content-program/",
    access: "CC0",
    note: "Imagens de obras em domínio público disponibilizadas para estudo, ensino e reutilização."
  },
  {
    name: "Smithsonian · Open Access",
    url: "https://www.si.edu/openaccess",
    access: "CC0",
    note: "Milhões de itens 2D, 3D e dados; procure o ícone CC0 antes de reutilizar."
  },
  {
    name: "Art Institute of Chicago · API",
    url: "https://api.artic.edu/docs/",
    access: "Dados CC0 + IIIF",
    note: "Ótima fonte técnica para pesquisa. Para imagem de obra, confirme o campo de domínio público e os termos do objeto."
  }
];

const pd = "Priorize fichas institucionais marcadas Public Domain / Open Access / CC0.";
const restricted = "Estude pela instituição; direitos de imagem podem variar e não devem ser presumidos.";

export const artHistoryPeriods: ArtHistoryPeriod[] = [
  {
    id: "origens",
    dates: "antes de 3000 a.C.",
    title: "Origens · imagem, corpo e rito",
    region: "África, Europa e múltiplas culturas pré-históricas",
    thesis: "Antes de existir 'arte' como categoria moderna, imagem, objeto, corpo, memória e rito já estavam misturados.",
    construction: ["silhueta antes do detalhe", "ritmo por repetição", "contorno econômico", "uso expressivo da superfície"],
    thought: "Estude intenção e síntese: quanto pode ser dito com poucas marcas?",
    curiosity: "Paredes, pedra, osso e pigmento funcionavam como suporte, matéria e contexto ao mesmo tempo.",
    study: "Escolha um animal e reduza-o a 5 massas, depois a 12 linhas. Compare o que permaneceu.",
    diagram: "flat",
    diagramLabel: "silhueta · ritmo · suporte",
    artists: [
      {name:"Lascaux e Chauvet", focus:"movimento animal, sobreposição, economia de linha", rights:pd},
      {name:"Vênus paleolíticas", focus:"massa, símbolo, exagero e escala", rights:pd},
      {name:"mestres anônimos do Neolítico", focus:"padrão, gesto, narrativa coletiva", rights:pd}
    ]
  },
  {
    id: "egito-mesopotamia",
    dates: "c. 3000–500 a.C.",
    title: "Egito & Mesopotâmia",
    region: "Vale do Nilo, Mesopotâmia e Levante",
    thesis: "Imagem como ordem: hierarquia, frontalidade, perfil, registro e repetição constroem uma linguagem de poder e continuidade.",
    construction: ["grade e proporção", "hierarquia de escala", "perfil + frontalidade", "narrativa por faixas"],
    thought: "A forma serve a uma estrutura cultural; não é apenas observação naturalista.",
    curiosity: "Em muitos contextos egípcios, a legibilidade simbólica importava mais do que a ilusão óptica.",
    study: "Monte uma figura usando perfil de cabeça, olho frontal e tronco frontal. Depois quebre uma regra de propósito.",
    diagram: "grid",
    diagramLabel: "grade · hierarquia · registro",
    artists: [
      {name:"Imhotep", life:"c. 27º séc. a.C.", focus:"arquitetura, sistema e monumentalidade", rights:pd},
      {name:"atelier de Thutmose", focus:"retrato, oficina e estudo de cabeça", rights:pd},
      {name:"mestres de relevos neoassírios", focus:"ritmo narrativo, animais, guerra e movimento", rights:pd}
    ]
  },
  {
    id: "grecia-roma",
    dates: "c. 800 a.C.–500 d.C.",
    title: "Grécia & Roma",
    region: "Mediterrâneo",
    thesis: "O corpo vira laboratório de proporção, equilíbrio, peso e idealização; Roma expande retrato, narrativa e arquitetura.",
    construction: ["contrapposto", "eixo de peso", "proporção", "volume por planos", "perspectiva arquitetônica"],
    thought: "A anatomia interessa como estrutura em movimento, não apenas como catálogo de músculos.",
    curiosity: "Muitas esculturas gregas conhecidas hoje sobreviveram por cópias romanas.",
    study: "Desenhe uma figura em pé marcando apenas linha de ação, pelve, caixa torácica e perna de apoio.",
    diagram: "axis",
    diagramLabel: "peso · eixo · contrapposto",
    artists: [
      {name:"Policleto", life:"séc. V a.C.", focus:"cânone, equilíbrio e contrapposto", rights:pd},
      {name:"Praxíteles", life:"séc. IV a.C.", focus:"curva, suavidade e deslocamento de peso", rights:pd},
      {name:"Lisipo", life:"séc. IV a.C.", focus:"proporção mais esguia e corpo no espaço", rights:pd},
      {name:"mestres romanos de retrato e Pompeia", focus:"fisionomia, espaço, parede e narrativa", rights:pd}
    ]
  },
  {
    id: "asia-antiga",
    dates: "c. 200 a.C.–1000 d.C.",
    title: "Índia, China & rotas budistas",
    region: "Sul, Centro e Leste da Ásia",
    thesis: "Linha, gesto, símbolo e espiritualidade produzem soluções diferentes do naturalismo mediterrâneo.",
    construction: ["linha caligráfica", "ritmo de contorno", "gesto contínuo", "hierarquia simbólica"],
    thought: "Observe como a linha pode carregar tempo, respiração e intenção.",
    curiosity: "As rotas budistas conectaram oficinas, iconografias e técnicas por enormes distâncias.",
    study: "Faça 20 linhas longas sem apagar. Depois construa uma figura escolhendo 5 dessas linhas como esqueleto visual.",
    diagram: "curve",
    diagramLabel: "linha · respiração · fluxo",
    artists: [
      {name:"Gu Kaizhi", life:"c. 344–406", focus:"linha, figura e narrativa em rolo", rights:pd},
      {name:"mestres de Ajanta", focus:"figura, cor, gesto e narrativa budista", rights:pd},
      {name:"mestres de Gandhara", focus:"escultura, drapeado e encontro de tradições", rights:pd}
    ]
  },
  {
    id: "medieval",
    dates: "c. 500–1400",
    title: "Bizantino & Medieval",
    region: "Europa, Mediterrâneo e Bizâncio",
    thesis: "Imagem como presença, devoção e sistema narrativo; profundidade e escala obedecem a funções espirituais e sociais.",
    construction: ["frontalidade", "ouro e campo plano", "ritmo de pregas", "narrativa sequencial"],
    thought: "Nem toda imagem quer imitar o mundo; algumas querem organizar significado.",
    curiosity: "Iluminuras combinavam texto, imagem, pigmento raro e trabalho coletivo em objetos de uso e devoção.",
    study: "Crie uma composição frontal com uma figura central e três níveis de hierarquia sem usar perspectiva linear.",
    diagram: "flat",
    diagramLabel: "ícone · plano · hierarquia",
    artists: [
      {name:"Cimabue", life:"c. 1240–1302", focus:"transição entre tradição bizantina e maior volume", rights:pd},
      {name:"Giotto", life:"c. 1267–1337", focus:"peso, gesto, espaço e emoção", rights:pd},
      {name:"Duccio", life:"c. 1255–1319", focus:"cor, narrativa e elegância linear", rights:pd},
      {name:"irmãos Limbourg", life:"séc. XV", focus:"miniatura, calendário e detalhe", rights:pd}
    ]
  },
  {
    id: "renascimento",
    dates: "c. 1400–1600",
    title: "Renascimento",
    region: "Itália e Europa",
    thesis: "Perspectiva, anatomia, observação e projeto convergem; desenho passa a funcionar como ferramenta de pensamento.",
    construction: ["perspectiva linear", "triângulo compositivo", "anatomia estrutural", "claro-escuro", "estudo preparatório"],
    thought: "Desenhar pode ser investigar: corpo, máquina, espaço, luz e narrativa.",
    curiosity: "Cadernos e desenhos preparatórios revelam que muitas obras nasceram de dezenas de problemas menores.",
    study: "Pegue uma obra renascentista e reduza-a a horizonte, ponto de fuga, triângulo principal e três massas de valor.",
    diagram: "triangle",
    diagramLabel: "perspectiva · triângulo · anatomia",
    artists: [
      {name:"Leonardo da Vinci", life:"1452–1519", focus:"anatomia, sfumato, projeto e caderno", rights:pd},
      {name:"Michelangelo", life:"1475–1564", focus:"corpo, torção, escultura e desenho", rights:pd},
      {name:"Rafael", life:"1483–1520", focus:"clareza, equilíbrio e organização de grupos", rights:pd},
      {name:"Sandro Botticelli", life:"c. 1445–1510", focus:"linha, ritmo e figura", rights:pd},
      {name:"Albrecht Dürer", life:"1471–1528", focus:"proporção, gravura, observação e autorretrato", rights:pd}
    ]
  },
  {
    id: "maneirismo",
    dates: "c. 1520–1600",
    title: "Maneirismo",
    region: "Itália, Espanha e Europa",
    thesis: "Depois do equilíbrio renascentista, artistas alongam, comprimem, tensionam e tornam o espaço deliberadamente estranho.",
    construction: ["figura alongada", "torção", "espaço instável", "cor não naturalista"],
    thought: "A distorção pode ser uma decisão expressiva consciente.",
    curiosity: "O 'erro' anatômico muitas vezes é justamente o motor estilístico da obra.",
    study: "Desenhe uma pose correta; depois alongue apenas pescoço, mãos e pernas mantendo o centro de massa legível.",
    diagram: "curve",
    diagramLabel: "torção · alongamento · tensão",
    artists: [
      {name:"Pontormo", life:"1494–1557", focus:"cor, instabilidade e figura", rights:pd},
      {name:"Parmigianino", life:"1503–1540", focus:"alongamento e elegância artificial", rights:pd},
      {name:"Bronzino", life:"1503–1572", focus:"retrato, superfície e precisão", rights:pd},
      {name:"El Greco", life:"1541–1614", focus:"verticalidade, luz e espiritualização da figura", rights:pd}
    ]
  },
  {
    id: "barroco",
    dates: "c. 1600–1750",
    title: "Barroco",
    region: "Europa e Américas",
    thesis: "Luz, gesto, diagonal e teatralidade transformam a imagem em acontecimento.",
    construction: ["diagonal dominante", "chiaroscuro", "gesto interrompido", "profundidade por sobreposição"],
    thought: "A composição não descreve só o que aconteceu; ela controla quando e onde o olhar descobre.",
    curiosity: "Caravaggio e Rembrandt usam luz de modos diferentes, mas em ambos a luz organiza narrativa e atenção.",
    study: "Faça um desenho com 70% de sombra e apenas duas zonas de luz. Veja se a história continua legível.",
    diagram: "diagonal",
    diagramLabel: "luz · diagonal · drama",
    artists: [
      {name:"Caravaggio", life:"1571–1610", focus:"luz, corte, presença e drama", rights:pd},
      {name:"Rembrandt", life:"1606–1669", focus:"luz, matéria, retrato e processo", rights:pd},
      {name:"Diego Velázquez", life:"1599–1660", focus:"espaço, pincelada e olhar", rights:pd},
      {name:"Gian Lorenzo Bernini", life:"1598–1680", focus:"escultura, movimento e instante", rights:pd},
      {name:"Artemisia Gentileschi", life:"1593–c. 1654", focus:"narrativa, gesto e tensão", rights:pd},
      {name:"Peter Paul Rubens", life:"1577–1640", focus:"massa, energia e composição", rights:pd}
    ]
  },
  {
    id: "rococo",
    dates: "c. 1715–1780",
    title: "Rococó",
    region: "França e Europa",
    thesis: "Curva, leveza, ornamento, intimidade e cor substituem parte da gravidade barroca.",
    construction: ["arabesco", "curvas em S", "grupos assimétricos", "cores luminosas"],
    thought: "Leveza também é construção; ritmo pode organizar a imagem sem eixos rígidos.",
    curiosity: "Chardin convive com o Rococó mas escolhe cenas silenciosas e materiais comuns, oferecendo um ótimo contraponto.",
    study: "Construa uma composição inteira usando duas curvas em S e uma área de repouso vazia.",
    diagram: "curve",
    diagramLabel: "arabesco · leveza · assimetria",
    artists: [
      {name:"Antoine Watteau", life:"1684–1721", focus:"gesto, atmosfera e grupo", rights:pd},
      {name:"Jean-Honoré Fragonard", life:"1732–1806", focus:"movimento, pincelada e jogo visual", rights:pd},
      {name:"François Boucher", life:"1703–1770", focus:"ornamento, cor e superfície", rights:pd},
      {name:"Jean-Baptiste-Siméon Chardin", life:"1699–1779", focus:"silêncio, objeto, matéria e cotidiano", rights:pd}
    ]
  },
  {
    id: "neo-romantismo",
    dates: "c. 1750–1850",
    title: "Neoclassicismo & Romantismo",
    region: "Europa e Américas",
    thesis: "Razão, história, disciplina e desenho convivem com sublime, emoção, ruína, natureza e revolução.",
    construction: ["contorno e clareza", "pirâmide clássica", "escala sublime", "atmosfera"],
    thought: "Compare duas perguntas: como ordenar o mundo? e como mostrar forças maiores que nós?",
    curiosity: "Goya atravessa convenções de corte, guerra, sátira e imaginação, escapando de rótulos simples.",
    study: "Faça duas versões do mesmo tema: uma com contorno limpo e estrutura clássica; outra com massa, vento e contraste.",
    diagram: "triangle",
    diagramLabel: "ordem × sublime",
    artists: [
      {name:"Jacques-Louis David", life:"1748–1825", focus:"clareza, gesto e política da forma", rights:pd},
      {name:"Jean-Auguste-Dominique Ingres", life:"1780–1867", focus:"linha, retrato e distorção controlada", rights:pd},
      {name:"Antonio Canova", life:"1757–1822", focus:"escultura, acabamento e ideal clássico", rights:pd},
      {name:"Francisco Goya", life:"1746–1828", focus:"retrato, crítica, guerra e imaginação", rights:pd},
      {name:"J. M. W. Turner", life:"1775–1851", focus:"luz, atmosfera e dissolução", rights:pd},
      {name:"Eugène Delacroix", life:"1798–1863", focus:"cor, gesto e drama", rights:pd}
    ]
  },
  {
    id: "realismo",
    dates: "c. 1830–1880",
    title: "Realismo & Academia",
    region: "Europa e Américas",
    thesis: "Observação social, trabalho, vida comum e sistemas acadêmicos coexistem e entram em conflito.",
    construction: ["desenho por observação", "massa tonal", "anatomia acadêmica", "narrativa cotidiana"],
    thought: "É útil estudar tanto o método acadêmico quanto as escolhas que artistas realistas fizeram contra ele.",
    curiosity: "Ateliês do século XIX sistematizaram cópia de gravura, gesso, modelo vivo e pintura em etapas.",
    study: "Desenhe uma mão ou ferramenta de trabalho como protagonista, sem embelezar o gesto.",
    diagram: "axis",
    diagramLabel: "observação · peso · trabalho",
    artists: [
      {name:"Gustave Courbet", life:"1819–1877", focus:"matéria, escala e assunto contemporâneo", rights:pd},
      {name:"Jean-François Millet", life:"1814–1875", focus:"peso, trabalho e figura", rights:pd},
      {name:"Honoré Daumier", life:"1808–1879", focus:"gesto, caricatura e síntese", rights:pd},
      {name:"Rosa Bonheur", life:"1822–1899", focus:"animal, observação e estrutura", rights:pd},
      {name:"William-Adolphe Bouguereau", life:"1825–1905", focus:"acabamento acadêmico e figura", rights:pd},
      {name:"Jean-Léon Gérôme", life:"1824–1904", focus:"desenho, narrativa e atelier", rights:pd}
    ]
  },
  {
    id: "ukiyoe",
    dates: "c. 1603–1868",
    title: "Edo & Ukiyo-e · trilha paralela",
    region: "Japão",
    thesis: "Contorno, recorte, repetição, padrão e vazio constroem imagens de enorme clareza gráfica.",
    construction: ["silhueta", "recorte assimétrico", "espaço negativo", "padrão", "perspectiva não ocidental"],
    thought: "A força de uma imagem pode vir do corte e do vazio, não da modelagem volumétrica.",
    curiosity: "Gravuras japonesas circularam na Europa do século XIX e influenciaram composição, cor e enquadramento de muitos artistas.",
    study: "Pegue uma cena complexa e reconstrua usando apenas contorno externo, três padrões e uma grande área vazia.",
    diagram: "flat",
    diagramLabel: "recorte · padrão · vazio",
    artists: [
      {name:"Katsushika Hokusai", life:"1760–1849", focus:"onda, montanha, gesto e serialidade", rights:pd},
      {name:"Utagawa Hiroshige", life:"1797–1858", focus:"paisagem, clima, recorte e percurso", rights:pd},
      {name:"Utagawa Kuniyoshi", life:"1798–1861", focus:"figura, narrativa, guerreiros e fantasia", rights:pd},
      {name:"Kitagawa Utamaro", life:"c. 1753–1806", focus:"retrato, linha e padrão", rights:pd},
      {name:"Tōshūsai Sharaku", life:"ativo 1794–95", focus:"expressão e presença gráfica", rights:pd}
    ]
  },
  {
    id: "impressionismo",
    dates: "c. 1860–1905",
    title: "Impressionismo & Pós-Impressionismo",
    region: "França e redes internacionais",
    thesis: "Luz, instante e vida moderna abrem caminho para pesquisas muito diferentes de cor, estrutura e expressão.",
    construction: ["corte fotográfico", "cor por justaposição", "pincelada visível", "estrutura por planos"],
    thought: "Não trate o período como um estilo único: Monet, Degas, Cézanne, Van Gogh e Seurat resolvem problemas diferentes.",
    curiosity: "Tubos de tinta portáteis, fotografia, ferrovias e novas teorias da cor mudaram a prática do artista.",
    study: "Faça o mesmo motivo em três versões: luz, estrutura e emoção. Não mude o objeto; mude a pergunta.",
    diagram: "rhythm",
    diagramLabel: "cor · instante · estrutura",
    artists: [
      {name:"Claude Monet", life:"1840–1926", focus:"luz, série e atmosfera", rights:pd},
      {name:"Edgar Degas", life:"1834–1917", focus:"corte, gesto, repetição e corpo", rights:pd},
      {name:"Mary Cassatt", life:"1844–1926", focus:"figura, intimidade e desenho", rights:pd},
      {name:"Berthe Morisot", life:"1841–1895", focus:"pincelada, luz e vida cotidiana", rights:pd},
      {name:"Vincent van Gogh", life:"1853–1890", focus:"ritmo, cor e energia da marca", rights:pd},
      {name:"Paul Cézanne", life:"1839–1906", focus:"plano, volume e estrutura", rights:pd},
      {name:"Georges Seurat", life:"1859–1891", focus:"óptica, desenho tonal e construção", rights:pd}
    ]
  },
  {
    id: "simbolismo",
    dates: "c. 1880–1914",
    title: "Simbolismo & Art Nouveau",
    region: "Europa e redes internacionais",
    thesis: "Sonho, ornamento, linha e psicologia deslocam a arte do registro exterior para mundos mentais e decorativos.",
    construction: ["linha ornamental", "campo plano", "motivo recorrente", "figura + símbolo"],
    thought: "Símbolo funciona melhor quando nasce de relações visuais, não apenas de explicação textual.",
    curiosity: "Cartaz, livro, arquitetura, mobiliário e pintura se aproximam; arte e design passam a dialogar intensamente.",
    study: "Escolha um símbolo pessoal e repita-o em três escalas dentro da mesma composição.",
    diagram: "curve",
    diagramLabel: "ornamento · símbolo · repetição",
    artists: [
      {name:"Odilon Redon", life:"1840–1916", focus:"carvão, sonho e metamorfose", rights:pd},
      {name:"Gustav Klimt", life:"1862–1918", focus:"figura, padrão e ouro", rights:pd},
      {name:"Alphonse Mucha", life:"1860–1939", focus:"linha, cartaz e ornamento", rights:pd},
      {name:"Aubrey Beardsley", life:"1872–1898", focus:"preto e branco, recorte e linha", rights:pd},
      {name:"Edvard Munch", life:"1863–1944", focus:"psicologia, linha e repetição temática", rights:pd}
    ]
  },
  {
    id: "modernismos",
    dates: "c. 1905–1945",
    title: "Modernismos",
    region: "Europa, Rússia e redes transatlânticas",
    thesis: "A obra deixa de precisar esconder sua construção: cor, plano, geometria, fragmento e abstração tornam-se assunto.",
    construction: ["plano explícito", "geometrização", "fragmentação", "cor autônoma", "grade"],
    thought: "Pergunte o que acontece quando representação deixa de ser a única medida de qualidade.",
    curiosity: "Muitos movimentos coexistem e discordam entre si; 'modernismo' é uma constelação, não um estilo único.",
    study: "Reduza uma figura a planos; depois reconstrua-a sem voltar ao contorno original.",
    diagram: "fragment",
    diagramLabel: "plano · fragmento · abstração",
    artists: [
      {name:"Henri Matisse", life:"1869–1954", focus:"cor, recorte, ritmo e simplificação", rights:pd},
      {name:"Wassily Kandinsky", life:"1866–1944", focus:"cor, música e abstração", rights:pd},
      {name:"Paul Klee", life:"1879–1940", focus:"linha, sistema, jogo e ensino", rights:pd},
      {name:"Kazimir Malevich", life:"1879–1935", focus:"geometria e redução", rights:pd},
      {name:"Piet Mondrian", life:"1872–1944", focus:"grade, equilíbrio e redução", rights:pd},
      {name:"Amedeo Modigliani", life:"1884–1920", focus:"alongamento, retrato e síntese", rights:pd},
      {name:"Pablo Picasso & Georges Braque", focus:"cubismo, múltiplos pontos de vista e fragmentação", rights:restricted}
    ]
  },
  {
    id: "pos-guerra",
    dates: "1945–hoje",
    title: "Pós-guerra & Contemporâneo",
    region: "Global",
    thesis: "Meios, instituições, política, mercado, corpo, tecnologia e ideia passam a fazer parte explícita da obra.",
    construction: ["campo", "gesto", "serialidade", "apropriação", "instalação", "processo"],
    thought: "Aqui a pergunta muda: além de 'como foi feito?', pergunte 'que sistema, contexto ou ideia a obra ativa?'.",
    curiosity: "Grande parte desta faixa ainda possui direitos autorais ativos; estudar não significa copiar nem republicar imagens.",
    study: "Escolha uma obra contemporânea e escreva três coisas separadas: material, operação e ideia. Depois crie outra solução para a mesma ideia.",
    diagram: "fragment",
    diagramLabel: "processo · contexto · ideia",
    artists: [
      {name:"Jackson Pollock", life:"1912–1956", focus:"gesto, campo e processo", rights:restricted},
      {name:"Mark Rothko", life:"1903–1970", focus:"campo de cor, escala e presença", rights:restricted},
      {name:"Louise Bourgeois", life:"1911–2010", focus:"corpo, memória, objeto e espaço", rights:restricted},
      {name:"Andy Warhol", life:"1928–1987", focus:"repetição, mídia e circulação", rights:restricted},
      {name:"Yayoi Kusama", life:"1929–", focus:"repetição, ambiente e obsessão", rights:restricted},
      {name:"Anselm Kiefer", life:"1945–", focus:"matéria, memória e história", rights:restricted}
    ]
  }
];
