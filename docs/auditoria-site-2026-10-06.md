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
5. Cadernos: preenchidas as seis fichas que estavam sem imagem (Sully, Reynolds, Wright, Bluemner, Whistler e Edmonds) com mídia oficial identificada como domínio público nas fontes. Os links de imagem apontam aos servidores do Met/NGA.

## Estado dos testes
- Inspeção manual: nove áreas/categorias do site, incluindo EN, ES e Banco Nacional Digital.
- Defeitos de conteúdo confirmados nesta rodada: 2 tipos; as correções estão publicadas.
- Imagens quebradas confirmadas nas páginas inspecionadas: nenhuma.
- CI e implantação do site: sucesso.
- Auditoria móvel automatizada: sucesso. A matriz percorreu 52 rotas em 4 larguras de celular; os testes internacionais EN/ES e os limites responsivos também passaram. Uma tentativa anterior encontrou um 503 transitório; a execução completa posterior concluiu com sucesso.

## Pendências que permanecem
- A revisão editorial profunda não cobre integralmente todos os conteúdos do arquivo: a inspeção manual desta rodada passou por nove áreas; a matriz automatizada conferiu 52 rotas em responsividade, não a qualidade de cada texto, exercício e CTA.
- As seis imagens novas dos cadernos são servidas pelos endpoints oficiais do Met/NGA. O espelhamento das imagens para dentro de `public/` ainda falta para eliminar dependência desses servidores; também é necessário inventariar outros assets externos antes de afirmar que todas as imagens estão hospedadas no GitHub.
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
