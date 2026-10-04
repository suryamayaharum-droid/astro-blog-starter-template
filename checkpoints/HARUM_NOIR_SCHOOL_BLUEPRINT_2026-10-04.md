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

**Estado:** implementação em andamento no branch `codex/harum-noir-visual-collections-20261004`; imagem criada e otimizada localmente; PR ainda não aberto.

| Área | Mudança desta rodada | Estado |
|---|---|---|
| `/colecoes/` | Nova entrada com três coleções de estudo: gesto e corpo, forma e luz, matéria e borda. Cada cartão usa imagem didática e leva a uma prática existente. | Em construção |
| `/atlas/` e menu Explorar | Adicionar caminho visual com imagem própria para as coleções. | Em construção |
| `/maos/` | Retirar dez explicações em cartões redundantes, encurtar a entrada visual e criar ligação direta ao exercício de seis gestos. | Em construção |
| Imagem de abertura | Prancha editorial tripla gerada para forma/luz, gesto e carvão; exportada como WebP local otimizado, sem texto embutido. | Pronta; aguarda validação no build |
| Blueprint | Atualizar registro de rota, conteúdo, progresso, próximos reparos e critérios de aceite após CI e publicação. | Em construção |

## Próximas revisões — fila seguinte

| Prioridade | Próxima revisão |
|---|---|
| 1 | Ampliar Coleções Visuais com novas lições guiadas além da primeira coleção, mantendo cada estudo ligado a uma prática. |
| 2 | Localizar Coleções Visuais e aprofundar conteúdo de desenho em EN/ES; algumas rotas ainda abrem portais amplos. |
| 3 | Rever alt text, contraste e correspondência entre cartões e aulas nas rotas antigas, incluindo História da Arte e Referências. |
| 4 | Repetir CI, links, âncoras e matriz móvel ao publicar novos módulos. |

### Critério de conclusão desta entrega

**Concluído:** build e CI verdes; verificador sem links, âncoras ou imagens inválidas; rotas da escola sem overflow em 320–412 px; deploy e conferência visual do GitHub Pages; auditoria móvel e internacional aprovadas.
