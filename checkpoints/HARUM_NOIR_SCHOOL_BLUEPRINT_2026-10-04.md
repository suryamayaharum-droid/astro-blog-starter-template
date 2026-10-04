# Blueprint público · Escola HARUM NOIR

Data: 4 de outubro de 2026  
Repositório: suryam.../astro-blog-starter-template  
Decisão de marca: **HARUM NOIR** é o nome público. **Harumverso** continua apenas como referência interna ao conjunto de projetos.

## Barra de progresso

**Entrega desta versão:** [█████████░] 90% — build, links e âncoras, hreflang e SEO passaram no CI; falta a captura móvel e conferir a versão publicada.

A barra mede esta entrega do site, não o avanço de quem estuda. A barra de aprendizagem da escola é pessoal, salva no navegador e pode ser apagada pela pessoa.

## O que a inspeção encontrou

| Área | Problema observado | Tratamento nesta entrega |
|---|---|---|
| Página inicial | Muitas seções e trilhos competiam entre si; havia cartões repetidos e a escola não aparecia como caminho principal. | Entrada simplificada, quatro etapas com imagens e três portas de início. |
| Links de estudo | Sessões levavam a busca genérica; oito leques repetiam o mesmo destino. | A home agora liga cada etapa a uma rota adequada; gesto vai ao Atlas das Mãos. |
| Imagens | A primeira dobra de Mãos era quase toda tipográfica; cartões de arquivo e continuidade eram apenas texto. | Capas locais na página Mãos, no Arquivo e nos cartões de continuidade. |
| Identidade pública | Algumas páginas ainda chamavam a navegação de Harumverso. | Páginas de busca, Biblioteca, sketchbooks e README usam HARUM NOIR. |
| Entrada internacional | As home pages em inglês e espanhol não ofereciam um curso como primeiro passo. | Rotas de escola localizadas em inglês e espanhol, com entrada nas páginas correspondentes. |
| Integridade das rotas | O verificador conferia arquivos, mas não âncoras dentro das páginas. | CI passa a verificar destinos e fragmentos, incluindo links na própria página. |

Não apareceram marcadores genéricos de rascunho como Lorem ou TODO nas páginas inspecionadas. O ruído vinha principalmente da hierarquia, de destinos repetidos e de nomes inconsistentes.

## Estrutura da escola

1. **Observar:** escolher uma imagem e formular uma pergunta visual.
2. **Estruturar:** ler gesto, silhueta, peso e massas principais.
3. **Organizar:** comparar referências no caderno e guardar uma descoberta.
4. **Traduzir:** voltar ao papel e tomar uma decisão visual própria.

A primeira prática leva 12 minutos e divide o tempo entre pergunta, estrutura, borda e síntese. O painel guarda quatro marcos no aparelho, sem conta ou alegação de certificação.

## Arquivos em trabalho

- **src/pages/index.astro** — nova porta de entrada da escola.
- **src/components/School.astro** e **src/pages/escola.astro** — plano, primeira prática e progresso local.
- **src/pages/en/school.astro** e **src/pages/es/escuela.astro** — rotas localizadas.
- **src/data/ecosystem.ts** e **src/components/EcosystemRail.astro** — rotas pesquisáveis e cartões com capa.
- **src/pages/maos.astro**, **src/pages/atlas.astro**, **src/pages/arquivo.astro** — imagem e orientação nas entradas principais.
- **src/components/Header.astro**, **src/components/LumeGuide.astro**, **src/pages/busca.astro** — atalhos para a escola e destino correto para gesto.
- **scripts/check_internal_links.mjs** — teste de links e âncoras.
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
