# HARUM Workspace Skill — v0.1

> Skill de projeto. Não é uma skill global instalada no runtime do ChatGPT.

## Trigger
Quando a solicitação envolver HARUM NOIR, Arte Harum, Studio 23, JEV, escola, site, conteúdo, UX, SEO, QA, deploy ou continuidade do ecossistema.

## Boot compacto
1. Ler este arquivo.
2. Ler docs/HARUM_INTELLIGENCE_CORE.md.
3. Consultar o estado/PR/issue relevante no GitHub/JEV.
4. Construir ou atualizar ProjectVector com src/scripts/harum-project-vector.ts.
5. Selecionar trabalho por src/scripts/harum-intelligence-core.ts.
6. Executar apenas pelas ferramentas/capacidades realmente disponíveis.
7. Verificar evidência antes de marcar conclusão.
8. Persistir somente delta significativo + próximo passo.

## Modelo global em camadas
V = [S | C | P | D | F | E | R | B | X]
- S: distribuição de status
- C: distribuição de capacidades
- P: distribuição de prioridade
- D: densidade de dependências
- F: densidade de conflitos de arquivos
- E: cobertura de evidências
- R: prontidão
- B: bloqueios
- X: conclusão

Assinatura H = FNV1a(canonical(tasks)). H muda quando o estado canônico relevante muda.

Saúde operacional:
Q = .30E + .25X + .20R + .15(1-B) + .10(1-F)
Q é indicador operacional, não verdade semântica nem avaliação artística.

## Duplo espelho
- Espelho A — semântico: GitHub/JEV, decisões, arquivos, evidências e contexto humano.
- Espelho B — compacto: ProjectVector + signature + deltas.
A é fonte de verdade. B serve para orientação rápida, comparação e detecção de mudança.

## Delta
Em vez de repetir o estado completo, registrar Δ = V(t) - V(t-1), assinatura anterior/nova, tarefas alteradas e evidências novas. Reidratar detalhes do Espelho A somente quando necessário.

## Regras
- Nunca inferir permissão a partir do vetor.
- Nunca tratar assinatura como prova de correção.
- Não armazenar chain-of-thought; somente estado, decisões e evidências.
- Não copiar conteúdo de concorrentes; abstrair padrões.
- Não usar GitHub Actions como orquestrador.
- Não declarar deploy/merge/publicação sem confirmação da ferramenta.
- Paralelizar apenas tarefas sem conflito de estado/arquivo.

## Objetivo
Máxima continuidade com mínimo contexto: carregar o mapa compacto, identificar o delta e expandir apenas a região do projeto necessária à demanda atual.
