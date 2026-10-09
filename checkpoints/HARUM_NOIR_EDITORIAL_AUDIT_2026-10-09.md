# HARUM NOIR · Auditoria editorial página a página · 9 out 2026

**Escopo:** rotas públicas do GitHub Pages. Revisão por lotes; páginas boas ficam sem reescrita cosmética.

## Progresso

`███░░░░░░░ 31% · 23/74 arquivos de rota revisados manualmente`

- [x] Varredura estrutural das 74 rotas Astro: títulos, presença de imagens, quantidade e rótulos de ações, marcadores de conteúdo provisório.
- [x] Conferir o caminho de entrada: home → escola → primeira prática → museus.
- [x] Revisar as portas centrais: Ateliê, busca, Museus, Referências, Biblioteca, Percursos e Sobre.
- [x] Corrigir os cinco fallbacks de redirecionamento que mostravam apenas “Continuar”.
- [x] Revisar os cinco Cadernos e seus destinos; acrescentar roteiros com tempo, saída e conferência em Olhar e Vestígio.
- [ ] Conferir fichas de artistas e promessas dos links externos.
- [ ] Revisar páginas de bancos/acervos e as rotas de História da Arte.
- [ ] Conferir paridade editorial EN/ES nas páginas prioritárias.
- [ ] Fechar a auditoria móvel pós-release em painel próprio.

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

A revisão também deixou uma melhoria didática nos cadernos Olhar e Vestígio: cada um agora abre com um roteiro curto, duração, saída e pergunta de conferência.\n\nFoi criado `src/components/LegacyRedirect.astro`. As cinco rotas antigas continuam direcionando às páginas canônicas, mas agora oferecem uma tela de contingência identificável caso o redirecionamento automático não aconteça:

- `/about/` → Sobre o HARUM NOIR;
- `/artists/` → Referências;
- `/classics/` → História da Arte;
- `/newsletter/` → Carta HARUM NOIR;
- `/vault/` → Arquivo editorial.

A tela informa o destino, oferece um link com rótulo específico, mantém `noindex,follow` e aponta o canonical para a rota final.

## Leitura da varredura

Não encontrei texto “Lorem ipsum” nem páginas de conteúdo com placeholder de template no primeiro inventário. Os termos de placeholder nas rotas de Busca e Museus são dicas de consulta; os usos de “todo” apareceram em frases portuguesas como “todo o site”, não como conteúdo provisório. Os redirects acima eram a fragilidade editorial concreta deste lote.

## Próximo lote

Começar pelos Cadernos: verificar se cada título leva a uma prática própria, se a saída é verificável e se o link de retorno preserva o percurso. Depois revisar fichas de artistas com foco em fonte primária, status de vídeo e correspondência entre promessa e destino.
