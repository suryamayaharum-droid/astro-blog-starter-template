# HARUM INTELLIGENCE CORE

Estado: protocolo operacional v0.1 — 2026-10-09

## Missão
Converter pesquisa, decisões e execução em um sistema fluido de **pull**, com tarefas pequenas, evidência verificável e dependências explícitas. Este arquivo coordena trabalho; não concede permissões, não executa em background e não substitui revisão humana.

## Círculos concêntricos

### C0 — Núcleo de estado
Fonte de verdade: GitHub para código; JEV para contexto, decisões e handoff.
Mantém: objetivo atual, backlog, bloqueios, evidências, branch/PR, última ação válida e próxima ação.

### C1 — Sensoriamento
Pesquisa referências, métricas, conteúdo, UX e problemas do site. Saída obrigatória: achado + fonte/evidência + impacto + sugestão original HARUM.

### C2 — Síntese
Agrupa achados e transforma-os em decisões reutilizáveis: componentes, padrões de conteúdo, dados e critérios de aceite. Evita duplicação e cópia de terceiros.

### C3 — Construção
Puxa somente itens READY. Cada unidade deve declarar arquivos afetados, dependências e critério de conclusão. Trabalhos independentes podem ocorrer em paralelo; alterações sobre o mesmo arquivo/estado são serializadas.

### C4 — Verificação
Build, links, acessibilidade, responsividade, conteúdo, regressão e coerência. Uma mudança só vira VERIFIED com evidência. Falha volta para C3 com diagnóstico.

### C5 — Integração/publicação
PR pequena, revisão, preview/deploy quando disponível. Nunca tratar branch, PR ou preview como produção. Credenciais, checkout e ações irreversíveis exigem o fluxo de autorização da ferramenta correspondente.

### C6 — Observação
SEO, comportamento, erros e resultados alimentam C1. Métrica sem contexto não gera mudança automática.

## Máquina de estados
BACKLOG -> READY -> CLAIMED -> DOING -> VERIFY -> VERIFIED -> INTEGRATE -> DONE
Bloqueios: BLOCKED_PERMISSION | BLOCKED_DEPENDENCY | BLOCKED_EVIDENCE | FAILED

## Contrato de tarefa
```yaml
id: HIC-000
circle: C1|C2|C3|C4|C5|C6
objective: resultado verificável
status: BACKLOG
priority: P0|P1|P2|P3
depends_on: []
resources: []
files: []
evidence: []
acceptance: []
next: []
owner_capability: research|content|code|qa|seo|deploy|coordination
```

## Regra de pull
1. Ler estado.
2. Selecionar maior prioridade em READY cuja capability exista e dependências estejam satisfeitas.
3. Marcar CLAIMED antes de mutar estado compartilhado.
4. Executar a menor mudança que produza avanço verificável.
5. Anexar evidência e enviar para VERIFY.
6. Verificação independente quando possível.
7. Liberar dependentes somente após VERIFIED.

## Paralelismo seguro
Pode paralelizar: pesquisa de referências diferentes; auditorias somente leitura; criação de componentes em arquivos distintos; SEO e conteúdo quando não disputam a mesma fonte.
Serializar: mesmo arquivo; merge; configuração de deploy; checkout; migração de dados; qualquer ação irreversível.

## Metacognição operacional
A cada ciclo registrar somente:
- o que sabemos e a evidência;
- o que mudou;
- o que continua incerto;
- bloqueios reais;
- próxima ação de maior valor.
Não registrar raciocínio privado/chain-of-thought.

## Política de autonomia
Mudanças reversíveis, locais e alinhadas ao blueprint podem avançar em branch de revisão. Publicação, credenciais, compras, mudanças irreversíveis e permissões seguem os controles nativos. GitHub Actions não é usado como orquestrador.

## Primeira fila
- HIC-001 P0 C4: validar PR #78 e registrar falhas concretas.
- HIC-002 P0 C1: continuar benchmark pedagógico e UX.
- HIC-003 P1 C2: consolidar modelo de Lesson/LearningPath.
- HIC-004 P1 C3: implementar componentes pedagógicos reutilizáveis após HIC-001.
- HIC-005 P1 C4: QA mobile, teclado, links e scroll horizontal/vertical.
- HIC-006 P2 C6: estabelecer baseline SEO antes de otimizações amplas.
- HIC-007 P2 C3: melhorar funil Studio 23 sem misturar serviço e escola.

## Invariante
Toda automação deve aumentar capacidade sem apagar autoria, rastreabilidade ou segurança. O sistema otimiza fluxo; não inventa autoridade.
