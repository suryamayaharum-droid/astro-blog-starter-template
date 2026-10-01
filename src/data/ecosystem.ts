export type EcosystemHub = {
  id: string;
  title: string;
  kicker: string;
  description: string;
  href: string;
};

export const ecosystemHubs: EcosystemHub[] = [
  {id:"percursos",title:"Percursos",kicker:"ENTRAR POR UMA PERGUNTA",description:"Cinco caminhos curatoriais que ligam referência, caderno, fonte e prática.",href:"percursos"},
  {id:"referencias",title:"Atlas de Referências",kicker:"OLHAR POR DECISÕES",description:"Artistas, professores e processos organizados por foco, não por imitação.",href:"referencias"},
  {id:"biblioteca",title:"Biblioteca Aberta",kicker:"FONTE ANTES DE FÓRMULA",description:"Fontes públicas e institucionais organizadas por problemas de desenho.",href:"biblioteca"},
  {id:"historia-da-arte",title:"Atlas Histórico",kicker:"TEMPO & CONSTRUÇÃO",description:"Períodos, mestres, pensamento visual, exercícios e fontes abertas.",href:"historia-da-arte"},
  {id:"cadernos",title:"Cadernos de Presença",kicker:"PERGUNTA → PRÁTICA → VESTÍGIO",description:"Gesto, olhar, memória, presença e vestígio como investigações contínuas.",href:"cadernos"},
  {id:"atelier",title:"Ateliê Aberto",kicker:"VOLTAR PARA A MÃO",description:"Fundamentos, exercícios e ciclos de observação, correção e retorno.",href:"atelier"},
  {id:"temporadas",title:"Temporadas",kicker:"APROFUNDAMENTO",description:"Sete percursos editoriais de corpo, expressão, anatomia, personagem, relação, matéria e síntese.",href:"temporadas"},
  {id:"arquivo",title:"Arquivo Aberto",kicker:"O QUE PODE CIRCULAR, CIRCULA",description:"Materiais públicos prontos, cartas, textos abertos, RSS e portas do ecossistema.",href:"arquivo"},
];
