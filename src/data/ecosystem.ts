export type EcosystemHub = {
  id: string;
  title: string;
  kicker: string;
  description: string;
  href: string;
  cover: string;
};

export const ecosystemHubs: EcosystemHub[] = [
  {id:"escola",title:"Escola Aberta de Desenho",kicker:"APRENDER A OLHAR",description:"Plano de estudo em quatro movimentos: observar, estruturar, organizar e traduzir.",href:"escola/",cover:"harum-noir-escola-hero"},
  {id:"radar",title:"Radar HARUM NOIR",kicker:"PESQUISA VIVA",description:"Descobertas verificadas com direitos, princípio Noir e destino editorial.",href:"radar/",cover:"tools-paper"},
  {id:"atlas",title:"Atlas HARUM NOIR",kicker:"MAPA DO ECOSSISTEMA",description:"Uma mesa de orientação entre referências, museus, história, biblioteca, percursos e prática.",href:"atlas/",cover:"tools-paper"},
  {id:"buscar",title:"Busca HARUM NOIR",kicker:"UMA PERGUNTA · VÁRIAS PORTAS",description:"Busca transversal por rotas, artistas, técnicas, períodos, cadernos, coleções e temporadas.",href:"buscar/",cover:"moonlit-landscape"},
  {id:"percursos",title:"Percursos",kicker:"ENTRAR POR UMA PERGUNTA",description:"Cinco caminhos curatoriais que ligam referência, caderno, fonte e prática.",href:"percursos/",cover:"drapery-still-life"},
  {id:"referencias",title:"Atlas de Referências",kicker:"OLHAR POR DECISÕES",description:"Artistas, professores e processos organizados por foco, não por imitação.",href:"referencias/",cover:"harum-noir-caderno-estudo"},
  {id:"museus",title:"Museus Abertos",kicker:"ACERVOS INSTITUCIONAIS",description:"Porta de entrada para buscas em acervos, APIs e objetos de museus com origem verificável.",href:"museus/",cover:"museum-gallery"},
  {id:"biblioteca",title:"Biblioteca Aberta",kicker:"FONTE ANTES DE FÓRMULA",description:"Fontes públicas e institucionais organizadas por problemas de desenho.",href:"biblioteca/",cover:"open-sketchbook"},
  {id:"historia-da-arte",title:"Atlas Histórico",kicker:"TEMPO & CONSTRUÇÃO",description:"Períodos, mestres, pensamento visual, exercícios e fontes abertas.",href:"historia-da-arte/",cover:"iris-study"},
  {id:"outliers",title:"Outliers",kicker:"DESVIOS ÚTEIS",description:"Referências que ampliam o repertório por matéria, silêncio, transferência e imaginação.",href:"outliers/",cover:"moonlit-landscape"},
  {id:"cadernos",title:"Cadernos de Presença",kicker:"PERGUNTA → PRÁTICA → VESTÍGIO",description:"Gesto, olhar, memória, presença e vestígio como investigações contínuas.",href:"cadernos/",cover:"open-sketchbook"},
  {id:"maos",title:"Atlas das Mãos",kicker:"GESTO · FORMA · AÇÃO",description:"Estudos para ler direção, pressão, contato e intenção antes dos detalhes.",href:"maos/",cover:"harum-noir-hands-study"},
  {id:"corpo-em-relacao",title:"Corpo em Relação",kicker:"DUAS FIGURAS · UMA ESTRUTURA",description:"Apoio, distância, contato, resistência e peso compartilhado como narrativa corporal.",href:"corpo-em-relacao/",cover:"figure-gesture"},
  {id:"cabeca-expressao",title:"Cabeça & Expressão",kicker:"ESTRUTURA · DIREÇÃO · PRESENÇA",description:"Crânio, perfil, inclinação, olhar e expressão estudados sem fórmulas de rosto.",href:"cabeca-expressao/",cover:"harum-noir-caderno-olhar"},
  {id:"atelier",title:"Ateliê Aberto",kicker:"VOLTAR PARA A MÃO",description:"Fundamentos, exercícios e ciclos de observação, correção e retorno.",href:"atelier/",cover:"atelier-desk"},
  {id:"temporadas",title:"Temporadas",kicker:"APROFUNDAMENTO",description:"Sete percursos editoriais de corpo, expressão, anatomia, personagem, relação, matéria e síntese.",href:"temporadas/",cover:"moonlit-landscape"},
  {id:"noir",title:"HARUM NOIR",kicker:"TRAÇO · CORPO · PRESENÇA",description:"Princípios editoriais e portas de entrada da escola aberta de desenho.",href:"noir/",cover:"atelier-desk"},
  {id:"arquivo",title:"Arquivo Aberto",kicker:"O QUE PODE CIRCULAR, CIRCULA",description:"Materiais públicos prontos, cartas, textos abertos, RSS e portas do ecossistema.",href:"arquivo/",cover:"tools-paper"},
  {id:"carta",title:"Carta do Ateliê",kicker:"PUBLICAÇÃO ABERTA",description:"Uma ideia, uma referência e um exercício colocados em relação.",href:"carta/",cover:"drapery-still-life"},
  {id:"metodo",title:"Roubar como artista",kicker:"MÉTODO DE REFERÊNCIA",description:"Um protocolo para extrair princípios de referências sem copiar assinatura.",href:"roubar-como-artista/",cover:"exercicio-quatro-decisoes"},
  {id:"sobre",title:"Sobre HARUM NOIR",kicker:"COMO O SISTEMA PENSA",description:"A linguagem, os limites e o fluxo editorial que conectam pesquisa, prática e arquivo.",href:"sobre/",cover:"atelier-desk"}
];