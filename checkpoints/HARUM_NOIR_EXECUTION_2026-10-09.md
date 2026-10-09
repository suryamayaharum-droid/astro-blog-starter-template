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
| Alta | Sketchbook galleries, bancos de imagem e navegação do ecossistema | PRs [#29](https://github.com/suryamayaharum-droid/astro-blog-starter-template/pull/29) e [#30](https://github.com/suryamayaharum-droid/astro-blog-starter-template/pull/30) ainda abertas e sem mergeabilidade; disputam escopo semelhante e estão atrás da base atual. A revisão de #30 também apontou frases de busca não reconhecidas em francês/italiano. | Escolher uma só implementação-base, reconciliar com `main`, corrigir o classificador de idioma, verificar as imagens e executar CI + QA móvel. Não integrar nenhuma das duas sem reconciliação. |
| Média | Identidade de fonte de Jake Parker no Atlas | PR [#22](https://github.com/suryamayaharum-droid/astro-blog-starter-template/pull/22) permanece draft e não mergeável. | Atualizar a branch; manter canal oficial e deixar `videoId` vazio até validar um vídeo específico. |
| Média · infra separada | Workers Builds no Cloudflare | Issue [#82](https://github.com/suryamayaharum-droid/astro-blog-starter-template/issues/82) aberta. Várias prévias falham; o detalhe decisivo está no dashboard autenticado. GitHub Pages continua sendo a publicação canônica. | Registrar a primeira mensagem de erro real no dashboard antes de alterar comando ou configuração. |
| Média · manutenção separada | Astro/Vite/`@astrojs/cloudflare` | Issue [#83](https://github.com/suryamayaharum-droid/astro-blog-starter-template/issues/83) aberta. | Atualizar em lote pequeno, sem `npm audit fix --force`, mantendo `output: "static"` salvo decisão explícita. |

## Acordos de execução

1. Diagnosticar e localizar a rota antes de editar.
2. Não preencher página com texto decorativo: cada porta precisa prometer uma ação e entregar uma prática ou um destino útil.
3. Reutilizar imagem local quando ela corresponde ao assunto; identificar arte editorial e ligar fontes reais.
4. Rodar CI, auditoria responsiva e verificação de publicação para cada lote que afete a interface.
5. Atualizar este painel com o estado observado, não com o estado desejado.

## Próximo alvo

Começar o inventário editorial completo das rotas públicas e priorizar as páginas genéricas por promessa quebrada, destino vazio, falta de imagem ou falta de próximo passo. Em paralelo, destravar a reconciliação de uma única PR de sketchbooks, depois da auditoria da diferença entre #29 e #30.
