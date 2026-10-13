# Home inicial do ecossistema HARUM NOIR — especificação de design

Data: 2026-10-12  
Repositório público: `suryamayaharum-droid/astro-blog-starter-template`  
Branch: `codex/harumverso-home-tour-20261012`

## Objetivo

Elevar a home pública do ecossistema do GitHub a uma porta de entrada editorial clara e memorável. A pessoa deve entender o que pode explorar, escolher uma trilha e avançar pelas páginas HARUM NOIR com navegação confortável em celular. A home de estudo já existe; esta entrega evolui essa página como índice/tour do ecossistema sem apagar seu ciclo de aprendizagem.

## Contexto verificado

- O JEV canônico identifica `astro-blog-starter-template` como a superfície pública editorial HARUM NOIR; `arte-harum-tattoo-site` é a fonte privada mais ampla do Studio 23.
- A home atual está em `src/pages/index.astro`. Ela introduz a Escola Aberta de Desenho, apresenta o ciclo de estudo e quatro movimentos.
- `src/data/ecosystem.ts` é o catálogo de hubs públicos com slugs, descrições e capas já associadas a rotas reais.
- `src/components/RailEnhancer.astro` adiciona botões acessíveis e navegação por teclado a trilhos existentes; overflow horizontal e scroll snap já são padrões do site.
- A página Studio 23 servida dentro do Pages usa `/studio23/`; sua fonte canônica continua no repositório privado.
- Existem PRs abertos para sketchbooks e navegação; esta mudança não deve sobrepor alterações desses PRs.
- O trabalho é uma evolução de conteúdo/editorial do site público já existente. Não alterar hosting, visibilidade, domínio ou arquitetura do HIVE.

## Experiência proposta

1. **Hero de entrada:** imagem original em formato amplo, sem texto embutido, com atmosfera de ateliê escuro e espaço para o título; sobreposição de contraste mantém a cópia legível em todos os recortes.
2. **Tour fácil de começar:** CTA primário leva a `#tour`; uma linha introdutória explica que o site combina estudo, referências, cadernos e prática autoral.
3. **Trilhas curadas:** uma prateleira acessível destaca Escola, Atlas, Percursos, Cadernos, Sketchbooks e Biblioteca; os textos existentes em `ecosystem.ts` alimentam títulos, capas e descrições para evitar rotas inventadas.
4. **Continuidade do aprendizado:** manter o ciclo de estudo e as quatro etapas já presentes, agora abaixo da entrada do tour, sem remover o primeiro exercício gratuito.
5. **Navegação por imagens:** revisar trilhos e galerias com múltiplas imagens. Usar rolagem horizontal nativa em toque, scroll snap, controles de anterior/próximo, foco de teclado, rótulos acessíveis e movimento reduzido. Não bloquear o toque de links.
6. **Ponte de ecossistema:** preservar o acesso ao Studio 23 em `/studio23/` e às rotas multilíngues existentes sem criar seletores ou páginas não confirmados.

## Implementação e limites

- Alterar a fonte Astro em `src/pages/index.astro`, os componentes compartilhados de trilho apenas se a auditoria encontrar uma lacuna, e os testes/contratos já usados pelo CI.
- Guardar o novo fundo original em `public/noir/page-wallpapers/` e referenciá-lo com `BASE_URL`.
- Não alterar conteúdo das rotas de Sketchbooks ou outras rotas cobertas pelos PRs abertos; reutilizar o catálogo público de hubs.
- Manter conteúdo em português da home e manter as traduções existentes inalteradas.
- Não apresentar estudos editoriais ou imagens assistidas por IA como tatuagens reais, clientes ou sessões.
- Não adicionar dependências, backend, credenciais ou URLs privadas.
- Abrir um PR da branch e usar CI e preview visual para validar. Publicar a versão final na superfície GitHub Pages somente após os checks aprovarem.

## Critérios de aceite

- A home tem CTA funcional `#tour`, hero local carregado e contraste suficiente em celular e desktop.
- As seis trilhas curadas apontam para hubs existentes, preservando a subpágina `/studio23/` e o exercício gratuito.
- Trilhos de imagem em telas estreitas podem ser navegados por toque e pelos controles existentes; teclado, foco e `prefers-reduced-motion` continuam funcionando.
- Os testes de contrato, build Astro, typecheck e auditoria responsiva passam.
- Nenhuma rota existente nem PR aberto sofre substituição silenciosa.
- O progresso registra o branch/PR, checks, estado publicado e URL verificada.
