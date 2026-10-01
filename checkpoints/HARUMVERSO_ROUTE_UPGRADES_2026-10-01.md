# HARUMVERSO — CHECKPOINT ROUTE UPGRADES 2026-10-01

Estado: rotas estratégicas promovidas de aliases para páginas reais em branch isolada.

## Implementado
- /outliers → página editorial real com fontes institucionais e retorno à prática.
- /atlas → hub real de orientação entre Referências, História, Biblioteca, Percursos, Outliers e Arquivo.
- /noir → página identitária com princípios e portas de entrada.
- /classics → alias corrigido para /historia-da-arte.
- Header/Footer → Atlas exposto globalmente sem adicionar Outliers/Noir ao menu principal.

## Mantidos como alias
- /artists → /referencias
- /newsletter → /carta
- /vault → /arquivo
- /about → /sobre

Razão: não duplicar conteúdo nem simular funcionalidades inexistentes.

## Regras
- Respeitar BASE_URL.
- Não inflar a home.
- Rotas reais só quando têm função editorial própria.
- Fontes externas abrem com rel=noreferrer.
- Outliers decompõem princípios; não promovem imitação de estilo.

## Próximos gates
- preview/build
- inspeção mobile
- validar navegação Atlas → hubs → prática
- merge após gate técnico aceitável


## Baseline de infraestrutura
- Main validado no commit `1e7b94203b06e197a771ffbbbab6933de8ea141d`.
- Harumverso CI: success.
- GitHub Pages deploy: success.
- Este commit de checkpoint força nova validação do PR contra o baseline corrigido.
