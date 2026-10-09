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
| Alta | Auditoria editorial rota a rota para achar explicações genéricas, telas sem propósito e destinos com pouco conteúdo | Varredura estrutural concluída (74 rotas); revisão manual está em 37/74 (50%). PRs #90 e #91 integradas; PR #92 limpa três importações repetidas nas páginas internacionais de Coleções. A auditoria móvel do deploy atual ainda está em execução. | Continuar em lotes pequenos por tema; conferir fonte primária, destino de cada promessa e paridade editorial EN/ES. |
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

**Estado: execução #38002723488 concluída com sucesso após a correção e publicação da PR #88. A auditoria pós-deploy #38003813788 passou no retry após a integração da PR #90; a tentativa inicial capturou dois 503 temporários em imagens existentes. A PR #91 foi integrada em `6912b68`; a verificação de publicação e a auditoria móvel deste novo deploy ainda estão em andamento.**

A execução #368 identificou 22 combinações de rota/largura com controles sob o dock na posição inicial. A correção ajustou o teste para distinguir sobreposição inicial de bloqueio persistente após rolagem, sem tratar `aria-hidden` ou `inert` como ocultação visual.

PR [#88](https://github.com/suryamayaharum-droid/astro-blog-starter-template/pull/88) foi integrada; CI, GitHub Pages e a auditoria pós-deploy [#38002723488](https://github.com/suryamayaharum-droid/astro-blog-starter-template/actions/runs/38002723488) passaram. A matriz de rotas, o contrato de pré-lançamento, o smoke test internacional, os limites responsivos e o envio de screenshots terminaram com sucesso.

**Gate móvel:** #38003813788 passou depois de a publicação estabilizar. A nova auditoria pós-PR #91 aguarda o término do deploy `6912b68`.

## Próximo alvo

O inventário estrutural cobriu 74 arquivos .astro; o build publica 194 HTMLs e a auditoria automática não encontrou links ou assets quebrados. A leitura editorial manual segue em lotes: 37/74 rotas verificadas; priorizar fontes primárias do Atlas, rotas históricas restantes e paridade EN/ES. Para sketchbooks, verificar se as imagens locais representam corretamente os registros antes de adotar as imagens externas propostas.
