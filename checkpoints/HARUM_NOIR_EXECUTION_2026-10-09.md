# HARUM NOIR · Painel de execução GitHub · 9 out 2026

**Escopo:** GitHub Pages e o repositório que o publica.  
**Identidade:** HARUM NOIR é o nome público; “Harumverso” fica como nome interno do ecossistema.

## Barra de progresso · ciclo de escola e coleções

`██████████ 100% · PRs #78, #84 e #85 integradas; rotas EN/ES publicadas e verificadas`

- [x] Reestruturar a entrada da página inicial como escola: observar → praticar → comparar → registrar → voltar.
- [x] Ligar a primeira aula e os percursos a imagens, temas e ações que fazem sentido.
- [x] Integrar a trilha pedagógica e as rotas internacionais da PR #78.
- [x] Criar a Coleção 08 “Lugares para desenhar”, com quatro imagens editoriais, exercícios de oito minutos e fontes oficiais.
- [x] Criar as versões EN/ES, colocar imagens pertinentes nos mosaicos e ligar as rotas aos hubs.
- [x] Incluir as duas rotas novas na auditoria móvel e criar hreflang recíproco PT/EN/ES.
- [x] Passar CI e auditoria móvel nas PRs; verificar EN/ES publicados no GitHub Pages.

## Entregas concluídas

| Frente | Arquivos / páginas | Evidência |
|---|---|---|
| Escola e navegação | Home, escola, rituais, referências, percursos, cadernos e rotas EN/ES da PR #78 | PR [#78](https://github.com/suryamayaharum-droid/astro-blog-starter-template/pull/78) integrada em `381772e`; CI #584 e auditoria responsiva #94 verdes; revisão automática concluída sem apontamentos. |
| Coleção em português | `src/pages/colecoes/lugares.astro`, `src/pages/colecoes.astro`, auditoria móvel | PR [#84](https://github.com/suryamayaharum-droid/astro-blog-starter-template/pull/84) integrada em `d15a5c5`; rota pública verificada; quatro imagens e fontes carregam. |
| Localização da coleção | `src/pages/en/collections/places.astro`, `src/pages/es/colecciones/lugares.astro`, hubs EN/ES, `InternationalHub.astro`, workflow móvel e hreflang da rota PT | PR [#85](https://github.com/suryamayaharum-droid/astro-blog-starter-template/pull/85) integrada em `375992b`; CI #597 e auditoria móvel #96 verdes; EN e ES conferidas ao vivo. |
| Painel | Este arquivo | Atualizado após a integração das três frentes e da checagem pública. |

A nova aula ensina escala, luz, estrutura vegetal, composição e leitura responsável de arquivo. As imagens são identificadas como arte editorial; fontes oficiais levam ao acervo real, cuja ficha deve ser consultada para contexto e direitos.

## Fila de correções e edições

| Prioridade | Item | Estado atual | Próxima ação |
|---|---|---|---|
| Alta | Auditoria editorial rota a rota para achar explicações genéricas, telas sem propósito e destinos com pouco conteúdo | Varredura estrutural concluída (74 rotas); revisão manual está em 53/75 (71%). PRs #90, #91 e #92 integradas; PR #92 limpou três importações e corrigiu um destino genérico no Atlas. PR #93 integrou portas temáticas em Cultura Visual (commit `121270a`). CI e auditoria responsiva passaram. PR #100 foi integrada em `7e2e6fa` após CI #38078728950 e responsivo #38078728928 verdes. O CI #38078829381 e Pages #38078829417 do merge estão em execução; a auditoria móvel pós-deploy deste conteúdo ainda precisa iniciar. | Continuar em lotes pequenos por tema; conferir fonte primária, destino de cada promessa e paridade editorial EN/ES. |
| Média | Sketchbooks, bancos e navegação do ecossistema | A verificação pós-Atlas encontrou 75 arquivos de rota .astro e 414 páginas HTML no build; o CI checou 17.543 href/src e 290 fragmentos sem erros. O acervo atual tem 13 galerias e 26 referências a imagens locais; não estão vazias. PRs #29 e #30 seguem divergentes, sem mergeabilidade, e propõem enriquecer algumas imagens e a navegação. A revisão de #30 também apontou termos de busca FR/IT não reconhecidos. | Comparar as imagens locais com as fontes externas propostas antes de escolher uma só implementação; reconciliar com main e corrigir o classificador FR/IT. Manter as galerias atuais até validação e CI + QA móvel. |
| Média | Identidade de fonte de Jake Parker no Atlas | PR [#22](https://github.com/suryamayaharum-droid/astro-blog-starter-template/pull/22) permanece draft e não mergeável. | Atualizar a branch; manter canal oficial e deixar `videoId` vazio até validar um vídeo específico. |
| Média · infra separada | Workers Builds no Cloudflare | Issue [#82](https://github.com/suryamayaharum-droid/astro-blog-starter-template/issues/82) aberta. Várias prévias falham; o detalhe decisivo está no dashboard autenticado. GitHub Pages continua sendo a publicação canônica. | Registrar a primeira mensagem de erro real no dashboard antes de alterar comando ou configuração. |
| Média · manutenção separada | Astro/Vite/`@astrojs/cloudflare` | Issue [#83](https://github.com/suryamayaharum-droid/astro-blog-starter-template/issues/83) aberta. | Atualizar em lote pequeno, sem `npm audit fix --force`, mantendo `output: "static"` salvo decisão explícita. |

## Acordos de execução

1. Diagnosticar e localizar a rota antes de editar.
2. Não preencher página com texto decorativo: cada porta precisa prometer uma ação e entregar uma prática ou um destino útil.
3. Reutilizar imagem local quando ela corresponde ao assunto; identificar arte editorial e ligar fontes reais.
4. Rodar CI, auditoria responsiva e verificação de publicação para cada lote que afete a interface.
5. Atualizar este painel com o estado observado, não com o estado desejado.

## Auditoria móvel pós-release · 9 out 2026

**Estado: execução #38002723488 concluída com sucesso após a correção e publicação da PR #88. A auditoria pós-deploy #38003813788 passou no retry após a integração da PR #90; a tentativa inicial capturou dois 503 temporários em imagens existentes. A PR #91 foi integrada em `6912b68`; a PR #92 foi integrada em `85dfaa5`. Link Health passou para o merge #92; CI e GitHub Pages ainda estão em andamento. A auditoria móvel pós-deploy anterior permanece em andamento.**

A execução #368 identificou 22 combinações de rota/largura com controles sob o dock na posição inicial. A correção ajustou o teste para distinguir sobreposição inicial de bloqueio persistente após rolagem, sem tratar `aria-hidden` ou `inert` como ocultação visual.

PR [#88](https://github.com/suryamayaharum-droid/astro-blog-starter-template/pull/88) foi integrada; CI, GitHub Pages e a auditoria pós-deploy [#38002723488](https://github.com/suryamayaharum-droid/astro-blog-starter-template/actions/runs/38002723488) passaram. A matriz de rotas, o contrato de pré-lançamento, o smoke test internacional, os limites responsivos e o envio de screenshots terminaram com sucesso.

**Gate móvel:** #38003813788 passou depois de a publicação estabilizar. A nova auditoria pós-PR #91 aguarda o término do deploy `6912b68`.

## Próximo alvo

O inventário estrutural cobriu 74 arquivos .astro; o build publica 194 HTMLs e a auditoria automática não encontrou links ou assets quebrados. A leitura editorial manual segue em lotes: 49/74 rotas verificadas; priorizar destinos primários e duplicados no Atlas (PR #94), rotas históricas restantes e paridade EN/ES. Três rotas de linguagem corporal foram revisadas sem correção necessária. Para sketchbooks, verificar se as imagens locais representam corretamente os registros antes de adotar as imagens externas propostas.


## Revisão internacional · Cultura Visual e Tatuagem

Seis rotas PT/EN/ES foram comparadas. Cultura Visual agora direciona para os leques específicos de memória gráfica, botânica e impressão; EN/ES deixam claro que esses três destinos ainda estão em português. A rota Tatuagem mantém o conteúdo e a distinção entre pesquisa HARUM NOIR e atendimento Studio 23, sem alteração editorial necessária.


## Atlas · próxima correção de qualidade

PR #94 corrige quatro destinos repetidos/genéricos em cinco fichas: Chloe Rose, Sycra, Emanuele Dascanio e New Masters Academy. O perfil do Sycra fica com um card para o vídeo, mais o canal; os outros passam a oferecer páginas oficiais mais específicas.


## Revisão de três páginas didáticas

Cabeça & Expressão, Mãos e Corpo em Relação oferecem práticas concretas, imagens contextualizadas e fontes/retornos coerentes. Permanecem sem mudanças cosméticas. Progresso estrutural/manual: 49/74 (66%).


## Revisão dos hubs de Desenho

Desenho PT/EN/ES apresenta entradas equivalentes para carvão, figura e coleções, com imagens vindas dos componentes compartilhados e rótulos/destinos adequados ao idioma. Revisão concluída sem alterações nas páginas. Progresso: 49/74 (66%).


## História da Arte · revisão internacional

Os hubs EN/ES tinham o card “lentes de estudo” ligado à busca de museus. PR #95 redireciona a promessa para a aula localizada de Figura e Gesto, com rótulos específicos em cada idioma. Revisão manual: 52/74 rotas (70%). PR #94 foi integrada em `5a369bd`; validar CI e auditoria responsiva do próximo lote antes do merge.


## Integração editorial · PR #95

PR [#95](https://github.com/suryamayaharum-droid/astro-blog-starter-template/pull/95) integrada em `ec182fe`. O card de lentes de estudo nos hubs EN/ES de História agora leva à aula localizada de Figura e Gesto. CI #38016764680 e auditoria responsiva #38016764681 passaram. A captura móvel do deploy da PR #94 (#38016761776) permanece em execução; acompanhar até concluir. Revisão editorial: 52/74 rotas (70%).


## Atlas 1101 · integração nativa · PR #100

PR [#100](https://github.com/suryamayaharum-droid/astro-blog-starter-template/pull/100) integrada em `7e2e6fa`. Bancos, Sketchbooks, Composições Autorais e Artistas em Foco aparecem no Atlas e no índice compartilhado; 15 cadernos e três perfis de artistas são apresentados com fontes institucionais e práticas. O Lume ganhou encaminhamento local para Bancos/BNDigital em dez idiomas, rótulos (PT) para páginas sem tradução e detecção mais fiel do idioma de consulta.

Estado observado: CI #38078728950 e auditoria responsiva #38078728928 passaram. CI #38078829381 e Pages #38078829417 do merge estão ativos; esperar a publicação e a captura móvel antes de marcar o gate como fechado. Progresso editorial: 53/75 (71%).


## Estado observado · qualidade editorial e publicação · 10 out 2026

**Barra editorial:** `███████░░░ 72% · 54/75 rotas revisadas manualmente`.

- **PRONTO:** Outliers revisada com fontes institucionais; Appian agora exibe 1868–70. O Atlas inclui o canal oficial canônico do Jake Parker, sem atribuir vídeo não verificado.
- **PRONTO:** CI #38079190116 e GitHub Pages #38079190149 passaram.
- **FAZENDO:** auditoria móvel pós-deploy #38079254634 ainda está em execução.
- **PASSO:** acompanhar o resultado móvel e continuar a fila editorial com fonte, imagem e prática verificáveis.