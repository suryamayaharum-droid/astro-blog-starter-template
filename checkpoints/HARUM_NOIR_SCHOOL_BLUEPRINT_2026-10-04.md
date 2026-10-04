# Blueprint público · Escola HARUM NOIR

Data: 4 de outubro de 2026  
Repositório: suryam.../astro-blog-starter-template  
Decisão de marca: **HARUM NOIR** é o nome público. **Harumverso** continua apenas como referência interna ao conjunto de projetos.

## Barra de progresso

**Entrega desta versão:** [█████████░] 90% — CI, imagens e a matriz móvel passaram para 26 rotas nas larguras 320, 360, 390 e 412 px. A home e a escola foram conferidas ao vivo. Esta revisão separa destinos duplicados nas etapas EN/ES; faltam CI, novo deploy e repetir a matriz.

A barra mede esta entrega do site, não o avanço de quem estuda. A barra de aprendizagem da escola é pessoal, salva no navegador e pode ser apagada pela pessoa.

## O que a inspeção encontrou

| Área | Problema observado | Tratamento nesta entrega |
|---|---|---|
| Página inicial | Muitas seções e trilhos competiam entre si; havia cartões repetidos e a escola não aparecia como caminho principal. | Entrada simplificada, quatro etapas com imagens e três portas de início. |
| Links de estudo | Sessões levavam a busca genérica; oito leques repetiam o mesmo destino. | A home liga cada etapa a uma rota adequada; gesto vai ao Atlas das Mãos. Na escola EN/ES, organizar abre referências e traduzir volta à prática, sem destinos repetidos entre etapas. |
| Imagens | A primeira dobra de Mãos era quase toda tipográfica; cartões de arquivo e continuidade eram apenas texto. | Capas locais na página Mãos, no Arquivo e nos cartões de continuidade. |
| Identidade pública | Algumas páginas ainda chamavam a navegação de Harumverso. | Páginas de busca, Biblioteca, sketchbooks e README usam HARUM NOIR. |
| Entrada internacional | As home pages em inglês e espanhol não ofereciam um curso como primeiro passo. | Rotas de escola localizadas em inglês e espanhol, com entrada nas páginas correspondentes. |
| Integridade das rotas | O verificador conferia arquivos, mas não âncoras dentro das páginas. | CI passa a verificar destinos e fragmentos, incluindo links na própria página. |
| Integridade das imagens | A auditoria móvel encontrou duas capas WebP salvas com bytes inválidos; a página reservava o espaço, mas não as exibia. | Capas reconstruídas a partir das artes geradas; CI valida assinaturas WebP, PNG, JPEG, GIF e AVIF. |
| Navegação internacional móvel | As escolas EN/ES tinham cabeçalho localizado, mas não ofereciam a barra fixa do restante do site em telas pequenas; a primeira barra repetia destinos. | Dock com Início, Escola, Prática de desenho, Referências e Museus em destinos únicos; a matriz anterior passou e esta revisão revalida os links. |

Não apareceram marcadores genéricos de rascunho como Lorem ou TODO nas páginas inspecionadas. O ruído vinha principalmente da hierarquia, de destinos repetidos e de nomes inconsistentes.

## Estrutura da escola

1. **Observar:** escolher uma imagem e formular uma pergunta visual.
2. **Estruturar:** ler gesto, silhueta, peso e massas principais.
3. **Organizar:** comparar referências no caderno e guardar uma descoberta.
4. **Traduzir:** voltar ao papel e tomar uma decisão visual própria.

A primeira prática leva 12 minutos e divide o tempo entre pergunta, estrutura, borda e síntese. O painel guarda quatro marcos no aparelho, sem conta ou alegação de certificação.

## Arquivos em trabalho

- **public/noir/visual-atlas/harum-noir-escola-hero.webp** (1200×485) e **harum-noir-hands-study.webp** (900×600) — capas reconstruídas a partir das artes geradas.
- **src/pages/index.astro** — nova porta de entrada da escola.
- **src/components/School.astro** e **src/pages/escola.astro** — plano, primeira prática, progresso local e dock localizado para as rotas EN/ES.
- **src/pages/en/school.astro** e **src/pages/es/escuela.astro** — rotas localizadas.
- **src/data/ecosystem.ts** e **src/components/EcosystemRail.astro** — rotas pesquisáveis e cartões com capa.
- **src/pages/maos.astro**, **src/pages/atlas.astro**, **src/pages/arquivo.astro** — imagem e orientação nas entradas principais.
- **src/components/Header.astro**, **src/components/LumeGuide.astro**, **src/pages/busca.astro** — atalhos para a escola e destino correto para gesto.
- **scripts/check_internal_links.mjs** — teste de links, âncoras e assinaturas de imagens.
- **.github/workflows/noir-mobile-visual-audit.yml** — matriz móvel inclui as três páginas de escola e Mãos.

## Próximas revisões

| Prioridade | Trabalho que segue |
|---|---|
| 1 | Ler no celular as páginas longas de cada rota e confirmar que a promessa do cartão corresponde à aula aberta. |
| 2 | Verificar capas, alt text, contraste e âncoras das páginas antigas à medida que forem revisadas. |
| 3 | Ampliar traduções das lições além da porta inicial; as páginas profundas continuam majoritariamente em português. |
| 4 | Repetir a conferência visual e de links quando novas rotas ou módulos forem publicados. |

### Critério de conclusão desta entrega

Build verde; verificador sem destinos ou âncoras quebradas; rotas de escola legíveis em 320–412 px; GitHub Pages publicado e conferido.
