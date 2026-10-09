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
| Alta | Auditoria editorial rota a rota para achar explicações genéricas, telas sem propósito e destinos com pouco conteúdo | Ainda não concluída integralmente. CI cobre build, links, assets, SEO, hreflang e contratos; isso não julga a qualidade pedagógica de cada página. | Inventariar rotas públicas, agrupar por tema, comparar cada promessa do link com seu destino e editar em lotes pequenos com evidência. |
| Média | Sketchbooks, bancos e navegação do ecossistema | A varredura técnica encontrou 74 arquivos de rota .astro e 194 páginas HTML no build. O acervo atual tem 13 galerias e 26 referências a imagens locais; não estão vazias. PRs #29 e #30 seguem divergentes, sem mergeabilidade, e propõem enriquecer algumas imagens e a navegação. A revisão de #30 também apontou termos de busca FR/IT não reconhecidos. | Comparar as imagens locais com as fontes externas propostas antes de escolher uma só implementação; reconciliar com main e corrigir o classificador FR/IT. Manter as galerias atuais até validação e CI + QA móvel. |
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

**Estado: em correção; a experiência móvel ainda não está validada como verde.**

PR [#87](https://github.com/suryamayaharum-droid/astro-blog-starter-template/pull/87) foi integrada no commit `24db848`; CI e publicação do GitHub Pages passaram. A auditoria pós-deploy #368 terminou com falha em 22 combinações de rota/largura por controles e links que intersectam o dock fixo na posição inicial. Foram identificados estes grupos:

| Largura | Rotas afetadas |
|---|---|
| 320×568 | Radar, Buscar, Busca, Museus, Referências, Biblioteca, Percursos e Ritual do Carvão |
| 360×800 | Atlas |
| 390×844 | Buscar, Busca, Referências, Ateliê e Sobre |
| 412×915 | Escola, Escola EN, Escola ES, Buscar, Busca, Referências, Ateliê e Sobre |

O relatório registrou `HTTP 200`, sem overflow horizontal, imagens quebradas, recursos same-origin com erro ou erros de console. Os itens são links/controles que podem ser alcançados por rolagem, mas o teste anterior media apenas a posição inicial e não verificava essa possibilidade. A revisão do PR #87 também identificou que `aria-hidden` e `inert` não devem ser tratados como ocultação visual.

**Em andamento:** corrigir o teste para medir bloqueios persistentes após centralizar o controle na área visível. A checagem deve continuar usando estilos de renderização e `hidden`/fechamento de `details`; atributos de acessibilidade não devem mascarar sobreposições visuais.

**Critério de conclusão:** CI verde, nova auditoria pós-deploy concluída sem controles irrecuperavelmente encobertos e atualização deste painel com o resultado real. Se algum controle continuar sob o dock mesmo depois da rolagem, corrigir o layout da rota afetada antes de declarar concluído.

## Próximo alvo

O inventário estrutural cobriu 74 arquivos .astro; o build publica 194 HTMLs e a auditoria automática não encontrou links ou assets quebrados. Falta a leitura editorial manual rota a rota: identificar promessas genéricas, páginas sem prática e destinos que não correspondem ao rótulo. Para sketchbooks, verificar se as imagens locais representam corretamente os registros antes de adotar as imagens externas propostas.
