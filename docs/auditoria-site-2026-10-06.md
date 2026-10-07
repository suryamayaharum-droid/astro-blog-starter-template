# HARUM NOIR — relatório de auditoria visual e didática
Data da inspeção: 2026-10-06 · complemento: 2026-10-07

## Escopo conferido ao vivo
- Página inicial e assistente Lume: respostas determinísticas de navegação funcionam; carregamento do modelo de IA é opcional.
- Temporadas: 7 percursos com capas, perguntas, exercícios e resultados esperados.
- Bancos: 13 instituições e 8 guias temáticos.
- Banco Nacional Digital: seis botões “copiar termo”, abertura do menu Explorar e ação Estante testados; os três controles responderam na interface. Integrei seis recortes editoriais originais, um por tema, com texto alternativo e aviso de que não são imagens do acervo. A página oferece links oficiais para o acervo, catálogo Sophia, orientações de pesquisa e direitos de uso.
- Guia de mãos e gesto: navegação entre fontes e conteúdo do tema.
- Outliers: imagens didáticas e links de acervos institucionais.
- Escola: exercício guiado de 12 minutos, etapas e progresso persistido localmente.
- Coleção gesto e figura: imagem e sequência de prática.
- Portadas em inglês e espanhol: idioma do conteúdo, capas, links e rotas principais.

## Correções aplicadas
1. Guia temático de mãos e gesto: retirado o bloco vazio “Períodos fortes”; o botão da fonte agora leva ao conjunto de acervos usados pelo tema.
2. Portada EN: nota de idioma corrigida para distinguir esta portada e suas rotas traduzidas do arquivo mais amplo em português.
3. Portada ES: mesma correção de idioma aplicada e publicada no GitHub Pages.
4. BNDigital: criada e publicada uma prancha visual em seis recortes temáticos nos cartões de estudo; procedência separada claramente de documentos originais.
5. Cadernos: preenchidas as seis fichas que estavam sem imagem (Sully, Reynolds, Wright, Bluemner, Whistler e Edmonds) com mídia oficial identificada como domínio público nas fontes. As 26 imagens do catálogo foram copiadas para `public/noir/sketchbooks/`, otimizadas em WebP e ligadas aos cartões por caminho interno ao GitHub Pages; as fichas institucionais e a procedência dos arquivos foram mantidas.
6. Bierstadt: corrigido o identificador de uma mídia NGA preexistente que não carregava; a capa oficial do caderno foi conferida no navegador.
7. Smithsonian: corrigidos sete identificadores de imagem que retornavam 404 ou imagem vazia (seis páginas de Kenyon Cox e o caderno de William Trost Richards); as fichas oficiais confirmam CC0.
8. Cézanne: corrigido o endpoint NGA da capa, verificado na ficha oficial de domínio público e aberto no navegador.
9. Catálogo de sketchbooks: removida a dependência de carregamento em tempo de navegação dos endpoints de imagem do Met, NGA, Smithsonian e Commons; os cartões agora abrem cópias internas otimizadas.

## Estado dos testes
- Inspeção manual: nove áreas/categorias do site, incluindo EN, ES e Banco Nacional Digital.
- Defeitos confirmados e corrigidos: duas falhas de conteúdo e nove URLs de imagem inválidas; as 26 imagens do catálogo agora carregam de cópias locais.
- Cadernos: 26/26 imagens locais carregaram na página publicada; nenhum arquivo quebrou e os 26 cartões abrem a cópia interna no mesmo domínio.
- CI e GitHub Pages: build e publicação concluídos com sucesso no commit `9dcad56981aa52a77e1319673bd84a22ae977db1`.
- Auditoria móvel automatizada: sucesso no commit publicado. A matriz percorreu 52 rotas em quatro larguras de celular; os testes internacionais EN/ES e os limites responsivos também passaram. Uma tentativa anterior encontrou um 503 transitório; a execução completa posterior concluiu com sucesso.
- Inventário de mídia: 117 arquivos de código e páginas de `src/` e `public/studio23/` revisados; o repositório contém 681 arquivos de imagem; as 26 cópias locais do catálogo somam 1,65 MB em WebP. A mídia do Studio 23 referencia arquivos do mesmo GitHub Pages.

## Pendências que permanecem
- A revisão editorial profunda não cobre integralmente todos os conteúdos do arquivo: a inspeção manual desta rodada passou por nove áreas; a matriz automatizada conferiu 52 rotas em responsividade, não a qualidade de cada texto, exercício e CTA.
- Exceção encontrada: a busca da página Museus consulta Met, Art Institute of Chicago e Cleveland em tempo real e exibe imagens fornecidas pelas APIs oficiais. O GitHub Pages é estático; para essas imagens também ficarem locais, seria necessário limitar as buscas a uma coleção curada e pré-espelhada ou adicionar um backend. As imagens específicas seguem úteis e têm fallback local se a API de mídia falhar.
- O Lume funciona como guia determinístico de navegação. Um modelo de IA integrado e operacional não foi confirmado nesta auditoria; a camada opcional não deve ser apresentada como IA nativa funcional.
- Inglês e espanhol cobrem as portadas e rotas principais. O arquivo mais amplo permanece em português, conforme a preferência registrada.

## Mapa resumido
```text
Início
├── Escola e exercícios
├── Temporadas (7)
├── Coleções visuais
├── Bancos de referência
│   ├── Instituições (13)
│   └── Guias temáticos (8)
├── Outliers e história da arte
├── Lume (busca assistida)
├── Studio 23
└── Idiomas
    ├── Inglês (portada e rotas principais)
    └── Espanhol (portada e rotas principais)
```

Este registro descreve páginas e estados efetivamente verificados; não é uma certificação integral de cada página profunda do arquivo.
