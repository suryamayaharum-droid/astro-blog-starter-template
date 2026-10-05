# Blueprint público · Escola HARUM NOIR

Data: 4 de outubro de 2026  
Repositório: suryam.../astro-blog-starter-template  
Decisão de marca: **HARUM NOIR** é o nome público. **Harumverso** continua apenas como referência interna ao conjunto de projetos.

## Barra de progresso

**Entrega desta versão:** [██████████] 100% — CI e publicação concluídos. A auditoria móvel passou em 26 rotas nas larguras 320, 360, 390 e 412 px; 16 rotas EN/ES em 390 px; e 9 testes responsivos em 760, 761 e 1024 px. Nenhum overflow, imagem quebrada, erro de console ou recurso interno falho. Home, Escola, barra móvel e destinos das etapas foram conferidos ao vivo. [Ver auditoria final](https://github.com/suryamayaharum-droid/astro-blog-starter-template/actions/runs/37227696748).

A barra mede esta entrega do site, não o avanço de quem estuda. A barra de aprendizagem da escola é pessoal, salva no navegador e pode ser apagada pela pessoa.

## O que a inspeção encontrou

| Área | Problema observado | Tratamento nesta entrega |
|---|---|---|
| Página inicial | Muitas seções e trilhos competiam entre si; havia cartões repetidos e a escola não aparecia como caminho principal. | Entrada simplificada, quatro etapas com imagens e três portas de início. |
| Links de estudo | Sessões levavam a busca genérica; oito leques repetiam o mesmo destino. | Home liga cada etapa a uma rota adequada; gesto vai ao Atlas das Mãos. Na escola EN/ES, Organizar abre Referências e Traduzir volta à prática de 12 minutos. |
| Imagens | A primeira dobra de Mãos era quase toda tipográfica; cartões de arquivo e continuidade eram apenas texto. As duas novas capas também haviam sido enviadas com bytes inválidos. | Capas editoriais locais na home, Escola, Mãos, Arquivo e trilhos; WebP reconstruídos; CI valida assinaturas de imagem antes do deploy. |
| Identidade pública | Algumas páginas ainda chamavam a navegação de Harumverso. | Páginas de busca, Biblioteca, sketchbooks e README usam HARUM NOIR. |
| Entrada internacional | As home pages em inglês e espanhol não ofereciam um curso como primeiro passo. | Rotas de escola localizadas em inglês e espanhol, com entrada nas páginas correspondentes. |
| Integridade das rotas | O verificador conferia arquivos, mas não âncoras dentro das páginas. | CI passa a verificar destinos e fragmentos, incluindo links na própria página. |
| Integridade das imagens | A auditoria móvel encontrou duas capas WebP salvas com bytes inválidos; a página reservava o espaço, mas não as exibia. | Capas reconstruídas a partir das artes geradas; CI valida assinaturas WebP, PNG, JPEG, GIF e AVIF. |
| Navegação internacional móvel | As escolas EN/ES não tinham dock fixo e a primeira barra repetia destinos. | Dock com cinco destinos localizados e distintos; matriz final passou em 320–412 px. |

Não apareceram marcadores genéricos de rascunho como Lorem ou TODO nas páginas inspecionadas. O ruído vinha principalmente da hierarquia, de destinos repetidos e de nomes inconsistentes.

## Estrutura da escola

1. **Observar:** escolher uma imagem e formular uma pergunta visual.
2. **Estruturar:** ler gesto, silhueta, peso e massas principais.
3. **Organizar:** comparar referências no caderno e guardar uma descoberta.
4. **Traduzir:** voltar ao papel e tomar uma decisão visual própria.

A primeira prática leva 12 minutos e divide o tempo entre pergunta, estrutura, borda e síntese. O painel guarda quatro marcos no aparelho, sem conta ou alegação de certificação.

## Entregas concluídas no GitHub

| PR integrado | Resultado |
|---|---|
| [#31 · Escola Aberta](https://github.com/suryamayaharum-droid/astro-blog-starter-template/pull/31) | Nova home com quatro movimentos, rotas de Escola em PT/EN/ES, exercício de 12 minutos, progresso local, capas e destinos de navegação revistos. |
| [#32 · Imagens e CI](https://github.com/suryamayaharum-droid/astro-blog-starter-template/pull/32) | Duas capas WebP reconstruídas; CI agora detecta assinaturas inválidas de imagens locais, além de links e âncoras quebrados. |
| [#33 · Navegação móvel EN/ES](https://github.com/suryamayaharum-droid/astro-blog-starter-template/pull/33) | Dock móvel traduzido nas rotas da Escola em inglês e espanhol. |
| [#34 · Destinos distintos](https://github.com/suryamayaharum-droid/astro-blog-starter-template/pull/34) | “Organizar” leva a Referências; “Traduzir” retorna ao exercício. Os atalhos móveis não repetem destinos. |

## Arquivos principais

- `src/pages/index.astro` — nova entrada do site.
- `src/components/School.astro`, `src/pages/escola.astro`, `src/pages/en/school.astro`, `src/pages/es/escuela.astro` — plano de estudo, prática, barra local e navegação localizada.
- `public/noir/visual-atlas/harum-noir-escola-hero.webp` e `harum-noir-hands-study.webp` — capas geradas para o projeto, otimizadas e versionadas no repositório.
- `src/data/ecosystem.ts`, `src/components/EcosystemRail.astro`, `src/components/Header.astro` e `src/components/LumeGuide.astro` — caminhos encontrados na navegação e busca.
- `src/pages/maos.astro`, `src/pages/atlas.astro`, `src/pages/arquivo.astro` e `src/pages/busca.astro` — capas, orientação e destinos.
- `scripts/check_internal_links.mjs` — valida links locais, âncoras e assinaturas WebP, PNG, JPEG, GIF e AVIF.
- `.github/workflows/noir-mobile-visual-audit.yml` — matriz móvel inclui home, Escola PT/EN/ES, Mãos e rotas principais.

## Entrega atual — Coleções Visuais

**Estado:** PRs #38 e #39 integrados. Build Astro/TypeScript, links, âncoras, imagens locais, Pages e auditoria visual móvel passaram.

**Progresso desta rodada:** [██████████] 100% — a página foi confirmada ao vivo e `/colecoes/` entrou na matriz móvel. Run [37243440463](https://github.com/suryamayaharum-droid/astro-blog-starter-template/actions/runs/37243440463): 27 rotas × 4 larguras (108 capturas), 16 rotas EN/ES e 9 verificações em 760, 761 e 1024 px; zero falhas, overflow, imagem quebrada ou recurso interno falho.

| Área | Mudança desta rodada | Estado |
|---|---|---|
| `/colecoes/` | Nova entrada com quatro coleções de estudo: gesto e corpo, forma e luz, matéria e borda, Caderno como universo. A quarta entrada reaproveita a rota `/cadernos/` já existente; não duplica a coleção editorial em construção. | Publicada; visual confirmada |
| `/atlas/` e menu Explorar | Adicionar caminho visual com imagem própria para as coleções. | Publicada e validada no CI |
| `/maos/` | Retirar dez explicações em cartões redundantes, encurtar a entrada visual e criar ligação direta ao exercício de seis gestos. | Publicada e validada no CI |
| Imagem de abertura | Prancha editorial tripla gerada para forma/luz, gesto e carvão; exportada como WebP local otimizado, sem texto embutido. | Publicada e exibida no Pages |
| Auditoria móvel | Incluir `/colecoes/` na matriz e verificar os pontos de quebra. | Concluída; run 37243440463 verde |

## Próximas revisões — fila seguinte

| Prioridade | Próxima revisão |
|---|---|
| 1 | Revisar `/historia-da-arte/`, `/desenho/` e `/referencias/` para trocar explicações extensas por imagem quando isso tornar a decisão visual mais clara; manter fonte e contexto em texto curto. |
| 2 | Ampliar Coleções Visuais com novas lições guiadas além desta primeira versão, sempre ligadas a uma prática. |
| 3 | Localizar Coleções Visuais e aprofundar conteúdo de desenho em EN/ES; concluído no PR #42. |
| 4 | Rever alt text, contraste e correspondência entre cartões e aulas nas rotas antigas. |

### Critério de conclusão desta entrega

**Concluído:** PRs #38 e #39 integrados; build e CI verdes; verificador sem links, âncoras ou imagens inválidas; deploy verificado; 108 capturas de 27 rotas em 320–412 px; 16 rotas internacionais e 9 testes de limite aprovados.

## Recibo de continuidade

- **TENHO:** página `/colecoes/` publicada com quatro portas e arte local; `/maos/` aponta diretamente ao exercício de seis gestos. 
- **PRECISO:** nenhuma dependência para esta entrega.
- **CONCLUÍDO:** PR #42 integrado; hubs EN/ES e hubs prioritários PT agora abrem coleções com imagem e notas didáticas; `/historia-da-arte/` ganhou quatro lentes visuais.
- **PRONTO:** [PR #42 e CI de produção](https://github.com/suryamayaharum-droid/astro-blog-starter-template/actions/runs/37245298142), [publicação Pages](https://github.com/suryamayaharum-droid/astro-blog-starter-template/actions/runs/37245298165), [PR #38](https://github.com/suryamayaharum-droid/astro-blog-starter-template/pull/38), [PR #39](https://github.com/suryamayaharum-droid/astro-blog-starter-template/pull/39), [PR #42 (integrado)](https://github.com/suryamayaharum-droid/astro-blog-starter-template/pull/42), [CI e Pages](https://github.com/suryamayaharum-droid/astro-blog-starter-template/actions/runs/37243373048), [auditoria móvel](https://github.com/suryamayaharum-droid/astro-blog-starter-template/actions/runs/37243440463).
- **BLOQUEIO:** nenhum.
- **PASSO:** abrir a próxima unidade de revisão visual somente após comparar com as coleções existentes.
- **CONFLITO:** nenhum; a trilha Caderno como universo aponta ao `/cadernos/` existente.
- **ADIADO:** auditoria visual, responsiva e de fontes em cada item dos 613 assets do Studio 23; expandir novas aulas depois que a versão multilíngue passar.


## Continuidade — coleção Do gesto ao valor · 5 de outubro de 2026

**Estado desta rodada:** [████████░░] 80% — imagem original criada, modelo visual HARUM NOIR empacotado, aula e cartão conectados no código; aguardando CI, auditoria móvel e publicação.

| Item | Mudança | Estado |
|---|---|---|
| Template visual | Modelo reutilizável de prancha didática em carvão, papel quente e acento ocre. | Criado nesta conversa; pacote disponível |
| Nova aula | `/colecoes/estudo-tonal/` ensina gesto, silhueta, massas tonais e síntese em 12 minutos, com pergunta de ateliê. | Em revisão no GitHub |
| Cartão Forma · Luz | Leva diretamente à nova aula visual em vez de retornar ao início genérico da Escola. | Em revisão no GitHub |
| Auditoria responsiva | Adiciona a rota à matriz móvel de quatro larguras. | Em revisão no GitHub |
| Próxima fila | Fazer leitura visual de `/historia-da-arte/`, `/desenho/` e `/referencias/`; reduzir texto onde uma imagem didática ensinar melhor e preservar texto para contexto e fontes. | Próxima rodada |

