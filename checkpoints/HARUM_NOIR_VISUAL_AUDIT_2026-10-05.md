# HARUM NOIR — auditoria e mapa visual

Data: 2026-10-05  
Repositório: `suryamayaharum-droid/astro-blog-starter-template`  
Alvo público: GitHub Pages · HARUM NOIR

## Levantamento

A varredura percorreu **65 rotas Astro** e **88 arquivos de código** em páginas, componentes e dados. Foram rastreadas as capas esquemáticas em SVG, as texturas genéricas `charcoal-marks` e `graphite-texture`, os caminhos de imagem e os textos alternativos.

| Área | Lacuna encontrada | Implementação nesta revisão |
|---|---|---|
| Cadernos, índice e cinco páginas individuais | Capas de traço abstrato sem relação com o tema | Capas temáticas com texto alternativo e crédito; duas imagens com legenda agora acompanham cada tema no índice |
| Percursos e Biblioteca | Capas em rabiscos; a miniatura de reserva também era um rabisco | Coleções locais de gesto, modelo articulado, olho, sketchbook e tecido, com texto alternativo e créditos editoriais |
| Coleções em PT, EN e ES | A matéria/carvão não mostrava um assunto didático; EN/ES ainda tinham quatro entradas | Cinco entradas por idioma: gesto, forma, figura, matéria e caderno; figura e equilíbrio ligada à coleção própria em cada idioma |
| Escola e cartões de ecossistema | A etapa final e algumas portas usavam marcas/texturas abstratas | Pranchas de ateliê e estudos temáticos locais |
| Início, Ateliê, Harum Noir, Mãos, Atlas, Arquivo e Sobre | Algumas capas não identificavam o tema da página | Imagens de mão, modelo, ateliê, tecido, sketchbook, natureza-morta ou galeria conforme o destino |
| Referências, História da Arte e sitemap visual | Texturas genéricas apareciam em capas, fallback ou metadados | Capa temática HARUM NOIR com crédito explícito; metadados descrevem a imagem específica |
| Assets já sem uso | Sete SVGs esquemáticos e duas imagens genéricas de marcas/textura | Removidos depois de retirar suas referências no código |

**Escopo:** todas as rotas foram inspecionadas no código; não houve captura manual de cada rota nas três larguras. Imagens vindas de museus, artistas ou YouTube continuam ligadas às fontes de origem e não foram copiadas para substituir o acervo.

## Imagens criadas

| Arquivo | Conteúdo | Formato |
|---|---|---|
| `public/noir/visual-atlas/harum-noir-caderno-estudo.webp` | Mão com carvão, modelo articulado, sketchbook, íris botânica e tecido apagado | WebP · 1600×1067 · ~232 KB |
| `public/noir/visual-atlas/harum-noir-caderno-olhar.webp` | Olho construído sobre esfera, pálpebras e variações da direção do olhar | WebP · 1600×1067 · ~234 KB |

As imagens são estudos editoriais criados com assistência de IA, hospedados dentro do próprio repositório. As legendas esclarecem que não são obras de artistas nem documentos de acervo. O portfólio real do Studio 23 segue separado.

## Coleções visuais dos Cadernos

| Caderno | Pranchas da coleção | Foco |
|---|---|---|
| Presença | Estudo de ateliê + desenho em quatro etapas | Eixo, peso e relação entre formas |
| Gesto | Seis gestos de mão + construção em carvão | Direção e pressão antes do contorno |
| Olhar | Estudo ocular + íris botânica | Globo, pálpebras, direção e observação |
| Memória | Sketchbook + estudo de lembrança | Reconstrução sem consultar |
| Vestígio | Tecido em carvão + marcas apagadas | Bordas perdidas, retirada e resíduo |

## Próxima camada

1. O Atlas de 50 referências ainda usa capas temáticas HARUM NOIR em várias fichas. Para atribuir uma imagem real a cada artista, será necessário mapear fontes oficiais, domínio público e direitos antes de incorporá-las.
2. Os links de imagem de museus, artistas e vídeo permanecem externos por escolha editorial e conservam a procedência original.
3. A verificação de layout rota a rota será concluída pelo CI do pull request; esta varredura cobre caminhos de asset, conteúdo e código.

## QA

- Varredura estática: 65 rotas Astro, 88 arquivos de código.
- Substituições aplicadas nos hubs de português, inglês e espanhol.
- Ativos novos convertidos para WebP e apontados por caminhos locais do site.
- Assets genéricos sem referência removidos.
- Build Astro, links internos, `hreflang` e SEO: aguardando execução do CI no pull request.
