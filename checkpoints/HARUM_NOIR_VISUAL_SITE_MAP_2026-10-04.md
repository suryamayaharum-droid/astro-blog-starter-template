# HARUM NOIR — mapa visual do site
Data da auditoria: 2026-10-04
Escopo: inventário de rotas e imagens do repositório público; integração das lacunas didáticas confirmadas. A auditoria de uso de imagem percorreu componentes compartilhados, páginas de estudo, dados de cadernos/referências e nomes de assets; os 613 arquivos do Studio 23 foram contados, não avaliados individualmente por conteúdo nesta rodada.

## Mapa de rotas e famílias

| Família | Rotas/fonte | Idiomas e notas visuais |
|---|---|---|
| Portas do site | `/`, `/en/`, `/es/` | PT/EN/ES. Capas locais específicas; EN/ES usam `atelier-desk.webp`. |
| Escola aberta | `/escola/`, `/en/school/`, `/es/escuela/` | Componente compartilhado `School.astro`; hero e quatro etapas já tinham imagens próprias. A primeira prática agora tem prancha didática em quatro decisões, com legenda e texto alternativo nos três idiomas. |
| Prática e aprendizagem | `/desenho/`, `/en/drawing/`, `/es/dibujo/`, `/en/collections/`, `/es/colecciones/`, `/maos/`, `/temporadas/`, `/percursos/`, `/sketchbooks/`, `/roubar-como-artista/`, `/colecoes/` | `/maos/` ganhou prancha com seis ações para o exercício sem imagem. Percursos usam SVG temáticos; temporadas e desenho foram inventariados para revisão de conteúdo. |
| Cadernos | `/cadernos/` e `/cadernos/{presenca,gesto,olhar,memoria,vestigio}/` | Cinco entradas têm imagens SVG temáticas (`figure`, `gesture`, `eye`, `memory`, `trace`). |
| História, cultura e acervos | `/historia-da-arte/`, `/cultura-visual-brasileira/`, `/museus/`, `/arquivo/`, `/biblioteca/`, `/atlas/`, `/referencias/` | Imagens de museus/atlas locais ou registros ligados à fonte institucional; evitar substituir por imagens que imitem artistas reais. |
| Referências individuais | `/referencias/{slug}/` | 101 perfis no catálogo; capas editoriais temáticas locais e fontes originais. Capa gerada não é obra do artista nem tatuagem executada. |
| Bancos de imagem | `/bancos/`, `/bancos/{id}/` | 13 bancos registrados; cada coleção mantém a fonte/licença como origem. |
| Conteúdo/editorial e descoberta | `/about/`, `/sobre/`, `/atelier/`, `/noir/`, `/carta/`, `/classics/`, `/composicoes-autorais/`, `/outliers/`, `/vault/`, `/busca/`, `/buscar/`, `/newsletter/` | Rotas mapeadas no inventário de páginas Astro. Busca e newsletter são fluxos utilitários, não espaços que precisem de imagem decorativa. |
| Studio 23 | `/studio23/`, `/studio23/agendar/`, `/studio23/biblioteca/`, `/studio23/contato/`, `/studio23/cuidados/`, `/studio23/faq/`, `/studio23/harum-noir/`, `/studio23/localizacao/`, `/studio23/portfolio/`, `/studio23/privacidade/`, `/studio23/servicos/`, `/studio23/sobre/` | 12 páginas HTML nativas. 613 imagens locais sob `public/studio23/`; preservadas. |
| Infraestrutura | `/catalog.json`, `/image-sitemap.xml`, `/sitemap-index.xml` | Artefatos gerados pelo site, fora das páginas editoriais. |

## Lacunas e ações

| Local | Antes | Ação nesta alteração |
|---|---|---|
| Escola — primeira prática, em PT/EN/ES | Instruções de quatro passos sem imagem de demonstração | Adicionada prancha 2×2 do mesmo objeto: gesto, massas, bordas e estudo seletivo. Arte original assistida por IA, sem texto embutido e com legenda localizada. |
| `/maos/` — “Uma mão, seis verbos” | Seis cartões textuais sem referência visual | Adicionada prancha 3×2 com repouso, toque, segurar, pressionar, tensionar e proteger. A legenda explica que é apoio de desenho, não referência anatômica clínica. |
| `/colecoes/`, `/atlas/`, menu Explorar e `/maos/` | Estudos visuais e explicações estavam espalhados; a matriz móvel não conhecia a rota nova | Nova entrada com quatro coleções ligadas a exercícios e aos Cadernos existentes; bloco de dez cartões textuais em Mãos substituído por orientação curta ligada ao exercício visual de seis gestos; rota incluída na matriz de celulares. |
| Arquivos `blog-placeholder-1..5.jpg`, `blog-placeholder-about.jpg` e `reference-fallback.svg` | Nomes genéricos encontrados no repositório | A busca nas fontes não encontrou uso. Mantidos: não são necessários para esta correção e não foram removidos sem prova adicional de obsolescência no build publicado. |

## Critério visual e proveniência

As pranchas didáticas existentes seguem papel marfim, carvão/grafite e pequenos acentos ocres do atlas HARUM NOIR. Todas são arquivos locais WebP (`public/noir/visual-atlas/`), sem dependência de Drive ou hotlink. As legendas identificam assistência de IA. Não foram usadas referências de estilo de franquias ou de artistas vivos. Assets de portfólio Studio 23, imagens institucionais e coleções de museus permanecem intactos.


## Continuação multilíngue e coleções — em revisão

**Progresso:** [████████░░] 80% — visualização integrada; CI, verificação móvel e publicação pendentes.

A revisão atual amplia as Coleções Visuais para os caminhos em inglês e espanhol, com as novas rotas `/en/collections/` e `/es/colecciones/`. Os hubs compartilhados apresentam imagens locais em primeiro plano, links localizados e descrições didáticas em notas expansíveis. As duas home pages internacionais também passam a oferecer as coleções na navegação. O conteúdo português usa o mesmo padrão nos hubs de Desenho, Cultura Visual Brasileira e Tatuagem em Salvador.

A rota `/historia-da-arte/` recebe quatro lentes visuais (corpo/gesto, forma/luz, botânica/ornamento, matéria/superfície), conectadas aos períodos relevantes. Cada imagem é identificada como estudo editorial, não como obra histórica. `/referencias/` já tem capas por artista e permanece source-first; suas imagens e créditos foram preservados.

A nova imagem `brasil-acervo-editorial.webp` é uma composição conceitual assistida por IA, marcada como ilustração e não como mapa ou documento histórico. A coleção de Tatuagem usa fotografias já publicadas no portfólio oficial do Studio 23, sem banners promocionais.

**Pontos ainda em validação:** links internos localizados, acessibilidade/alt text, rotas novas, build e matriz móvel.

## Validação

PRs #38 e #39 integrados. CI e GitHub Pages passaram; a rota `/colecoes/` foi aberta ao vivo e a prancha e os quatro cartões apareceram. A auditoria [37243440463](https://github.com/suryamayaharum-droid/astro-blog-starter-template/actions/runs/37243440463) aprovou 27 rotas × 4 larguras (108 capturas), 16 rotas EN/ES e 9 limites em 760/761/1024 px, sem falhas de rota, overflow, imagem ou recurso interno. Esta alteração não muda o portão separado de publicação integral/cutover do site.
