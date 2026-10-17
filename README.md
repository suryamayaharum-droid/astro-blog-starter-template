# HARUM NOIR — site público

Escola aberta de desenho e arquivo editorial para estudar carvão, figura, observação, processo e pesquisa visual.

## Estrutura pública
- Escola Aberta de Desenho: observar, estruturar, organizar e traduzir
- Primeira prática guiada e progresso salvo apenas no aparelho
- Programa Regular: 33 técnicas e procedimentos em seis módulos, com 96 horas sugeridas, aulas próprias e referências públicas
- Cadernos de Presença
- Ateliê Aberto
- Temporadas
- Carta do Ateliê
- Arquivo Aberto
- Sobre

## Princípio
O site publica somente material autoral ou conteúdo curado para circulação pública. Pesquisa bruta, benchmarking, mapas internos e inteligência editorial não fazem parte deste repositório público.

## Imagens
As capas temáticas ficam no repositório para a navegação funcionar sem thumbnails externas. As novas cenas editoriais foram criadas com assistência de IA e não representam obras de museus ou artistas.

## Build
```bash
npm ci
npm run build
```

Publicado gratuitamente via GitHub Pages. O nome público é HARUM NOIR; Harumverso permanece uma designação interna do projeto.

## Programa Regular

Entrada: `/escola/programa-regular/`. A escola e a busca oferecem acesso às 33 aulas. O conteúdo é uma seleção independente de técnicas tradicionais com exercícios editoriais próprios; não reproduz a ementa ou as aulas de terceiros. A carga de 96 horas corresponde a uma proposta de estudo independente, sem anúncio de turma, tutoria ou certificação.

As referências históricas mantêm créditos e links aos acervos. As três novas reproduções de pinturas têm metadados de domínio público e procedência em `public/noir/programa-regular/proveniencia.json`. As imagens editoriais com assistência de IA estão identificadas nas legendas. O progresso do programa usa chave própria, sem alterar as marcações da primeira prática da escola.

Verificação do programa: `node scripts/check_regular_program.mjs`, após o build. A auditoria responsiva do PR executa também `scripts/check_regular_program_browser.mjs` para persistência, navegação e acesso sem JavaScript.
