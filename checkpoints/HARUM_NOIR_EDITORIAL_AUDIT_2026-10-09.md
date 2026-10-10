# HARUM NOIR · Auditoria editorial página a página · 9 out 2026

**Escopo:** rotas públicas do GitHub Pages. Revisão por lotes; páginas boas ficam sem reescrita cosmética.

## Progresso

`███████░░░ 66% · 49/74 arquivos de rota revisados manualmente`

- [x] Varredura estrutural das 74 rotas Astro: títulos, presença de imagens, quantidade e rótulos de ações, marcadores de conteúdo provisório.
- [x] Conferir o caminho de entrada: home → escola → primeira prática → museus.
- [x] Revisar as portas centrais: Ateliê, busca, Museus, Referências, Biblioteca, Percursos e Sobre.
- [x] Revisar a busca transversal: chips, acentos, parâmetro `q`, estado vazio e destinos da coleção.
- [x] Corrigir os cinco fallbacks de redirecionamento que mostravam apenas “Continuar”.
- [x] Revisar os cinco Cadernos e seus destinos; acrescentar roteiros com tempo, saída e conferência em Olhar e Vestígio.
- [x] Revisar o molde do perfil de artista e conferir 101 fichas / 208 links cadastrados.
- [ ] Conferir as promessas e a qualidade das fontes em cada ficha, substituindo intermediários por links primários quando possível.
- [x] Revisar a página Atlas Histórico: períodos paralelos, práticas próprias, fontes institucionais e distinção de direitos; remover cifra volátil do Open Access da NGA.
- [x] Revisar o hub de Bancos e o guia dinâmico dos acervos: portas, direitos, modos de acesso, leques e destinos coerentes.
- [ ] Revisar outras rotas de História da Arte e conferir links institucionais individuais.
- [x] Conferir paridade dos hubs EN/ES de História, Museus e Referências; destinos em PT estão rotulados.
- [x] Revisar páginas EN/ES de Coleções tonal, figura e lugares; conferir tradução, prática, imagens e retorno entre línguas.
- [x] Comparar Cultura Visual Brasileira e Tatuagem em Salvador nas versões PT/EN/ES; ligar cartões de cultura visual a leques específicos e confirmar que o material não traduzido está rotulado (PT).
- [x] Revisar Cabeça & Expressão, Mãos e Corpo em Relação: imagens pertinentes, práticas acionáveis e fontes articuladas; sem alterações necessárias.
- [x] Comparar os hubs de Desenho PT/EN/ES: cards equivalentes, imagens do componente compartilhado, rotas e rótulos de idioma coerentes.
- [ ] Continuar a paridade EN/ES nas demais páginas prioritárias.
- [x] Fechar auditoria móvel pós-release: execução #38002723488 passou em 9 out 2026.

## Revisão do primeiro percurso

| Página/rota | Resultado editorial | Decisão |
|---|---|---|
| Home `/` | Apresenta uma sequência didática coerente — observar, estruturar, organizar e traduzir — com imagem própria e ações diretas. Os quatro destinos existem. | Manter. Evitar mudar texto que já explica o que o visitante fará. |
| Escola PT/EN/ES | A primeira prática tem 15 minutos, instruções divididas por etapa, saída concreta e progresso salvo localmente. Os três wrappers usam a mesma sequência com tradução correspondente. | Manter; revisar links e linguagem novamente na etapa de paridade. |
| Ateliê | As propostas pedem ações observáveis: achar apoio, fazer miniaturas, comparar e registrar uma decisão. | Manter o método; rever visualmente os botões junto da auditoria móvel. |
| Buscar e Busca | A página principal explica o alcance da pesquisa e oferece termos menores; `/busca/` informa a mudança para `/buscar/`. | Manter; conferir a interação de busca e seus estados vazios no próximo lote. |
| Museus | Diferencia três APIs conectadas, serviços avançados, datasets e fontes que exigem chave; explica direitos e leva às fichas institucionais. | Manter a distinção; não chamar todas as fontes de “busca ao vivo”. |
| Referências | Orienta comparar duas ou três fontes, escrever a relação e sair com uma pergunta própria. A capa de IA é identificada como editorial. | Manter; revisar fichas individuais e links de vídeo depois. |
| Biblioteca e Percursos | As ações retornam a fontes, Cadernos e prática. Os fragmentos `#carvao` e `#figura` da home correspondem a IDs criados pelos dados dos percursos. | Manter; conferir cada destino na varredura seguinte. |
| Sobre | Diferencia Arte Harum, HARUM NOIR e Studio 23 e explica como pesquisa volta à prática. | Manter. |
| Cadernos | O índice e os cinco cadernos têm perguntas e práticas próprias; Presença, Gesto e Memória já descrevem encontros com ações específicas. Olhar e Vestígio não apresentavam um tempo curto nem uma saída resumida no início. | Acrescentados roteiros de 20 e 15 minutos, respectivamente, com passos, resultado e pergunta de conferência. Manter o restante do texto, que já explica o fundamento de cada caderno. |
| Redirects: `/about`, `/artists`, `/classics`, `/newsletter`, `/vault` | O redirecionamento automático estava correto, mas o fallback era sempre “Continuar” com o mesmo título genérico. | Corrigido neste lote: destino explicado, CTA específico, título contextual e apresentação acessível coerente com a marca. |

## Correção aplicada neste lote

A revisão também deixou uma melhoria didática nos cadernos Olhar e Vestígio: cada um agora abre com um roteiro curto, duração, saída e pergunta de conferência.

Foi criado `src/components/LegacyRedirect.astro`. As cinco rotas antigas continuam direcionando às páginas canônicas, mas agora oferecem uma tela de contingência identificável caso o redirecionamento automático não aconteça:

- `/about/` → Sobre o HARUM NOIR;
- `/artists/` → Referências;
- `/classics/` → História da Arte;
- `/newsletter/` → Carta HARUM NOIR;
- `/vault/` → Arquivo editorial.

A tela informa o destino, oferece um link com rótulo específico, mantém `noindex,follow` e aponta o canonical para a rota final.

## Leitura da varredura

Não encontrei texto “Lorem ipsum” nem páginas de conteúdo com placeholder de template no primeiro inventário. Os termos de placeholder nas rotas de Busca e Museus são dicas de consulta; os usos de “todo” apareceram em frases portuguesas como “todo o site”, não como conteúdo provisório. Os redirects acima eram a fragilidade editorial concreta deste lote.

## Próximo lote

Conferir fontes primárias e títulos das fichas de artistas, revisar as rotas restantes de História da Arte e completar a paridade EN/ES. Bancos/acervos e hubs EN/ES de História, Museus e Referências já foram revisados.


## Atlas de Referências · revisão do molde e inventário de fontes

A rota dinâmica `src/pages/referencias/[slug].astro` gera 101 fichas, apoiadas por 208 links. A inspeção estrutural encontrou 15 referências vidIQ em nove perfis: várias tinham título de vídeo, tutorial ou obra, mas o destino era um painel de estatísticas do canal; seis dessas referências repetiam um mesmo destino dentro do perfil. O perfil agora exclui todos os 15 destinos vidIQ dos cards de referência e dos dados estruturados; esses links não levam aos vídeos ou obras citados. O botão de canal oficial, vídeos diretos e outras fontes permanecem, destinos repetidos são deduplicados e a prática de 10 minutos continua disponível.

Esta edição corrige a expectativa do clique sem alegar que cada URL externa foi verificada ao vivo. Próximo passo: conferir fontes primárias e títulos em lotes pequenos, começando pelos perfis que dependem de intermediários; depois revisar bancos/acervos e História da Arte.


## Atlas Histórico · revisão de uma rota

A rota `/historia-da-arte/` foi conferida junto com `src/data/artHistory.ts`: os períodos têm perguntas e práticas próprias, datas são qualificadas como aproximações, e a página explica que esta é uma rota inicial com trilhas paralelas. As fichas distinguem orientação de domínio público de direitos variáveis. Retirei a cifra “mais de 60 mil” da nota da NGA, porque é um total que pode envelhecer; a instrução de confirmar o status em cada objeto foi mantida.


## Bancos e acervos · revisão de duas rotas

As rotas `/bancos/` e `/bancos/[id]/` foram conferidas com o catálogo de instituições. O hub distingue busca federada de dataset e serviço com chave; os guias dinâmicos mostram caminhos, direitos, leques de observação e retorno à instituição. Os oito leques temáticos apontam para IDs existentes e cada um oferece um experimento visual. Não encontrei chamada que prometa busca ao vivo para um serviço que não está conectado; mantive o conteúdo e não fiz reescrita cosmética.


## Hubs internacionais · História, Museus e Referências

Comparei as versões EN/ES dos três hubs. A estrutura de cartões e respostas mantém a mesma intenção editorial; caminhos para páginas que só existem em português informam “(PT)” no próprio rótulo. As páginas internacionais funcionam como portas explicativas, sem prometer tradução completa da busca viva ou do Atlas de artistas. Revisão concluída para estas seis rotas; outras páginas localizadas continuam na fila.


## Integração e validação · PR #90

PR [#90](https://github.com/suryamayaharum-droid/astro-blog-starter-template/pull/90) integrada em `12eb3c6` após CI e auditoria responsiva verdes. O PR #89 foi encerrado como substituído porque partia de uma base divergente. A revisão editorial continua em 43/74 rotas; a integração deste lote não marca a auditoria página a página como concluída.


## Correção de fonte externa · PR #91 integrada

A primeira edição identificava vidIQ como análise externa, mas ainda permitia o clique para fora do site. A PR #91 remove os 15 destinos vidIQ das fichas públicas e do schema, mantendo o canal oficial, vídeos diretos e demais fontes. Assim, um painel de métricas não aparece como fonte de aprendizagem.


## Busca transversal · revisão e acessibilidade

A rota `/buscar/` reúne Cadernos, artistas, períodos, Biblioteca, Radar e hubs; os chips alimentam consultas reais, a busca normaliza acentos, mantém `q` na URL e oferece orientação quando não há correspondência. O chip “Quero uma fonte aberta” consulta “open access” e encontra registros do Radar marcados com esses direitos. Ajustei a contagem de resultados como região `role=status` com anúncio educado, para que mudanças na busca sejam percebidas por leitores de tela.


## Mobile QA após PR #90 · concluído

A auditoria pós-deploy #38003813788 teve dois 503 transitórios em imagens já existentes na primeira captura. O retry do job passou em matriz móvel, smoke internacional, limites responsivos e envio de screenshots. Não houve falha de rota ou sobreposição de dock; o gate móvel está fechado.


## Integração e validação · PR #91

PR [#91](https://github.com/suryamayaharum-droid/astro-blog-starter-template/pull/91) integrada em `6912b68`. CI passou e a auditoria responsiva completa passou no commit de interface. O retry do mobile após PR #90 passou; a auditoria móvel do deploy após #91 ainda está em execução.


## Coleções internacionais · revisão de três páginas

Comparei tonal, figura/gesto e lugares em inglês e espanhol. A intenção didática, os tempos de prática e os créditos de imagem são equivalentes; a navegação volta ao hub no idioma certo e o seletor aponta às três versões. Encontrei importações duplicadas de `InternationalLessonChrome` em EN Figura, EN Tonal e ES Figura. PR #92 remove as declarações repetidas, sem alterar o conteúdo mostrado.

## Mobile QA após PR #91 · acompanhamento

O retry #38003813788 passou. A auditoria pós-deploy #38005500299 do commit `3c91c91` passou; a captura do deploy #92 (#38006094950, commit `e631761`) segue em execução.


## Atlas de Referências · correção pontual de destino

Na ficha de Mark Crilley, dois cartões levavam à mesma página inicial, embora o segundo prometesse uma demonstração de 30 segundos. Conferi a página oficial de aparições e ela descreve a demonstração ao vivo; substituí o destino repetido por `https://www.markcrilley.com/publicappearancesbio.html` e ajustei o rótulo/observação ao que a página realmente oferece. O vídeo de tutorial permanece como fonte separada. A contagem 43/74 mede arquivos de rota Astro e não muda com esta correção de dado do Atlas.


## Cultura visual e tatuagem · revisão de seis rotas PT/EN/ES

Comparei as três versões de Cultura Visual Brasileira e as três de Tatuagem em Salvador. A página de tatuagem mantém dados de atendimento coerentes e distingue HARUM NOIR (pesquisa editorial) de Studio 23 (portfólio e agendamento); não precisei alterar o conteúdo. Em Cultura Visual, Bahia, botânica e cultura impressa repetiam links a hubs amplos, apesar de já existirem destinos temáticos. As rotas PT agora apontam para `/bancos/brasil-memoria/`, `/bancos/flor-ornamento/` e `/bancos/arquivo-impressos/`. EN/ES apontam aos mesmos leques em português e identificam o idioma no próprio rótulo.


## Integração e validação · PR #93

PR [#93](https://github.com/suryamayaharum-droid/astro-blog-starter-template/pull/93) integrada em `121270a`. CI e auditoria responsiva passaram no commit de interface; a captura móvel #38006094950 da publicação anterior passou. CI #38016057381 e GitHub Pages #38016057361 do merge #93 estão na fila; aguardar a auditoria móvel pós-deploy deste conteúdo.


## Atlas de Referências · deduplicação e fontes primárias

A varredura dos destinos repetidos encontrou uma segunda home em Chloe Rose, o mesmo vídeo em dois cards de Sycra, a mesma página de vídeos em dois cards de Emanuele Dascanio e a home de New Masters Academy repetida como se fosse referência de modelo vivo. PR #94 troca esses caminhos por catálogo oficial de produtos, vídeo único com prática explícita, portfólio oficial de desenhos e catálogo curricular de figura, respectivamente. A contagem de rotas Astro permanece 49/74; os perfis são dados gerados pela rota dinâmica já revisada.

## Auditoria pós-deploy da PR #93 · estado

A auditoria responsiva completa #131 e o CI #652 passaram antes do merge da PR #93. A captura móvel pós-deploy #38016153717 também passou. CI #38016078850 e Pages #38016078797 da publicação #93 passaram após as atualizações documentais.


## Linguagem corporal · revisão de três rotas

Revisei `/cabeca-expressao/`, `/maos/` e `/corpo-em-relacao/`. Cabeça separa estrutura de expressão e termina em exercício de cinco direções; Mãos parte da ação e do contato, oferece uma prática de 15 minutos e fontes institucionais identificadas; Corpo em Relação ensina apoio, distância, contato e forças com um laboratório de 20 minutos. As imagens e os links internos servem ao exercício; não encontrei um problema editorial que justificasse reescrita.


## Desenho · revisão de três hubs PT/EN/ES

Os hubs `/desenho/`, `/en/drawing/` e `/es/dibujo/` compartilham a entrada por carvão, figura, coleções de estudo e tatuagem autoral. Embora as rotas individuais não tenham tags de imagem, o componente `PortugueseTopicHub` injeta quatro imagens editoriais correspondentes nos cards; EN/ES usam o trilho visual do componente internacional. Os destinos e a promessa editorial equivalem entre idiomas. Nenhuma correção necessária.
