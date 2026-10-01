export type EcosystemHub = {
  id: string;
  title: string;
  kicker: string;
  description: string;
  href: string;
};

export const ecosystemHubs: EcosystemHub[] = [
  {id:"atlas",title:"Atlas Harum Noir",kicker:"MAPA DO ECOSSISTEMA",description:"Uma mesa de orientação entre referências, museus, história, biblioteca, percursos e prática.",href:"atlas"},
  {id:"percursos",title:"Percursos",kicker:"ENTRAR POR UMA PERGUNTA",description:"Cinco caminhos curatoriais que ligam referência, caderno, fonte e prática.",href:"percursos"},
  {id:"referencias",title:"Atlas de Referências",kicker:"OLHAR POR DECISÕES",description:"Artistas, professores e processos organizados por foco, não por imitação.",href:"referencias"},
  {id:"museus",title:"Museus Abertos",kicker:"ACERVOS INSTITUCIONAIS",description:"Porta de entrada para buscas em acervos, APIs e objetos de museus com origem verificável.",href:"museus"},
  {id:"biblioteca",title:"Biblioteca Aberta",kicker:"FONTE ANTES DE FÓRMULA",description:"Fontes públicas e institucionais organizadas por problemas de desenho.",href:"biblioteca"},
  {id:"historia-da-arte",title:"Atlas Histórico",kicker:"TEMPO & CONSTRUÇÃO",description:"Períodos, mestres, pensamento visual, exercícios e fontes abertas.",href:"historia-da-arte"},
  {id:"outliers",title:"Outliers",kicker:"DESVIOS ÚTEIS",description:"Referências que ampliam o repertório por matéria, silêncio, transferência e imaginação.",href:"outliers"},
  {id:"cadernos",title:"Cadernos de Presença",kicker:"PERGUNTA → PRÁTICA → VESTÍGIO",description:"Gesto, olhar, memória, presença e vestígio como investigações contínuas.",href:"cadernos"},
  {id:"atelier",title:"Ateliê Aberto",kicker:"VOLTAR PARA A MÃO",description:"Fundamentos, exercícios e ciclos de observação, correção e retorno.",href:"atelier"},
  {id:"temporadas",title:"Temporadas",kicker:"APROFUNDAMENTO",description:"Sete percursos editoriais de corpo, expressão, anatomia, personagem, relação, matéria e síntese.",href:"temporadas"},
  {id:"noir",title:"Harum Noir",kicker:"TRAÇO · CORPO · PRESENÇA",description:"A página identitária que reúne os princípios editoriais e as portas de entrada do Harum Noir.",href:"noir"},
  {id:"arquivo",title:"Arquivo Aberto",kicker:"O QUE PODE CIRCULAR, CIRCULA",description:"Materiais públicos prontos, cartas, textos abertos, RSS e portas do ecossistema.",href:"arquivo"},
  {id:"carta",title:"Carta do Ateliê",kicker:"PUBLICAÇÃO ABERTA",description:"Uma ideia, uma referência e um exercício colocados em relação.",href:"carta"},
  {id:"metodo",title:"Roubar como artista",kicker:"MÉTODO DE REFERÊNCIA",description:"Um protocolo para extrair princípios de referências sem copiar assinatura.",href:"roubar-como-artista"},
  {id:"sobre",title:"Sobre Harum Noir",kicker:"COMO O SISTEMA PENSA",description:"A linguagem, os limites e o fluxo editorial que conectam pesquisa, prática e arquivo.",href:"sobre"},
];
