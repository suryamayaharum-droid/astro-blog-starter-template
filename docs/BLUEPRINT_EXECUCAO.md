# HARUM NOIR — BLUEPRINT DE EXECUÇÃO

> Painel operacional da evolução do GitHub Pages. Este arquivo existe para impedir perda de contexto, duplicação de trabalho e avanço sem validação.

## REGRA DE ATAQUE

Fluxo obrigatório:

`DIAGNOSTICAR → PRIORIZAR → CORRIGIR → VALIDAR → REGISTRAR → PRÓXIMO ALVO`

Uma frente só recebe **CONCLUÍDO** quando há evidência. Build verde não significa que revisão visual/mobile está concluída.

## PAINEL GERAL

```text
HARUM NOIR · GITHUB PAGES
Progresso estrutural estimado: 80%

[████████████████████] CI / Astro / TypeScript ........ CONCLUÍDO
[████████████████████] Cloudflare dry-run ............. CONCLUÍDO
[████████████████████] Links internos / assets ........ CONCLUÍDO pelo CI
[████████████████████] hreflang recíproco ............. CONCLUÍDO pelo CI
[████████████████████] SEO estrutural / JSON-LD ....... CONCLUÍDO pelo CI
[████████████████████] contrato Studio23 ↔ Noir ....... CONCLUÍDO pelo CI
[████████████████░░░░] ciclo pedagógico ............... EM CONSOLIDAÇÃO
[██████████████░░░░░░] coerência entre páginas ........ EM AÇÃO
[██████████░░░░░░░░░░] responsividade visual .......... PENDENTE QA
[████████░░░░░░░░░░░░] acessibilidade visual/teclado .. PENDENTE QA
[██████░░░░░░░░░░░░░░] EN/ES / redundâncias .......... PENDENTE AUDITORIA
[████░░░░░░░░░░░░░░░░] dependências / segurança ...... PENDENTE TRIAGEM
[░░░░░░░░░░░░░░░░░░░░] merge/publicação .............. BLOQUEADO ATÉ QA
```

## ESTADO DA PR #78

- Branch: `melhoria/escola-primeira-pratica-2026-10-09`
- PR: #78 — draft.
- Correção crítica mais recente: `museus.astro` restaurado após truncamento do script.
- Commit da correção: `eac8bcd0df6b83787596c3a1871efc20927c1e64`.
- CI HARUM NOIR run #481: **verde**.
- Astro + TypeScript: **verde**.
- Cloudflare dry-run: **verde**.
- Rotas/assets, hreflang, SEO/JSON-LD e contrato Studio23 ↔ Noir: **verdes**.

## FILA DE ATAQUE

### P0 — estabilidade
- [x] Localizar falha do build.
- [x] Restaurar script de Museus.
- [x] Confirmar CI verde.
- [ ] Triar as vulnerabilidades npm sem `--force` e separar transitivas de corrigíveis.

### P1 — experiência real
- [ ] QA visual 320 / 390 / tablet / desktop.
- [ ] Encontrar overflow horizontal não intencional.
- [ ] Verificar navegação por teclado, foco e touch targets.
- [ ] Conferir carrosséis/rails e scroll-snap.
- [ ] Verificar imagens quebradas, cortes ruins e páginas visualmente vazias.

### P2 — coerência pedagógica
- [ ] Resolver definitivamente 12 min × 15 min na primeira prática.
- [ ] Garantir em cada página: objetivo → ação → entrega → autoavaliação → próximo passo.
- [ ] Fazer Museus, Referências, Percursos, Ateliê e Cadernos funcionarem como um ciclo, não como ilhas.
- [ ] Trocar jargão interno exposto quando não ajuda o aluno.

### P3 — arquitetura de informação
- [ ] Auditar EN/ES antes de manter ou remover.
- [ ] Auditar Header/Footer/alternates após decisão de idiomas.
- [ ] Reduzir rotas redundantes e becos sem saída.
- [ ] Separar claramente Escola HARUM NOIR e atendimento Studio 23 sem fragmentar a marca.

### P4 — acabamento e descoberta
- [ ] Revisão editorial de títulos, CTAs e microcopy.
- [ ] Auditoria de metadados por rota.
- [ ] Search Console somente quando houver propriedade GSC conectada.
- [ ] Performance de imagens/fontes/scripts.
- [ ] Revisão final antes de tirar PR de draft.

## BLUEPRINT PEDAGÓGICO

Toda página de aprendizagem deve responder, quando aplicável:

1. **O que estudo aqui?**
2. **O que faço agora?**
3. **Quanto tempo/material preciso?**
4. **O que produzo ao sair?**
5. **Como confiro meu estudo?**
6. **Onde registro?**
7. **Para onde continuo?**

Ciclo-base:

`ACERVO → PERGUNTA → OBSERVAÇÃO → MICROPRÁTICA → ENTREGA → AUTOAVALIAÇÃO → CADERNO → NOVO PERCURSO`

## COMO ATUALIZAR ESTE PAINEL

Após cada ataque:
1. mover o item de PENDENTE para EM AÇÃO ou CONCLUÍDO;
2. registrar evidência (commit, CI, rota ou teste);
3. se surgir regressão, promover para P0;
4. atacar o próximo item de maior impacto;
5. nunca declarar publicação sem evidência de deploy.

Última evidência: CI HARUM NOIR run #481 concluído com sucesso após a correção de Museus.


## TECNOLOGIA DO PAINEL — V2

O painel deixou de ser apenas uma barra manual. O estado estruturado vive em `systems/harum_execution_panel.json` e segue quatro princípios pesquisados:

- **Kanban:** visualizar trabalho, limitar WIP e tornar políticas explícitas.
- **DORA:** mudanças pequenas, medir fluxo + estabilidade e atacar o maior gargalo.
- **GitHub Projects:** estados e campos estruturados em vez de progresso enterrado em texto.
- **ADR/MADR:** decisões duráveis ficam explícitas; histórico não é apagado silenciosamente.

### Máquina de estados

`QUEUED → READY → ATTACKING → VERIFYING → DONE`

Saídas excepcionais: `BLOCKED` e `STALE`.

### WIP

- ataque principal: **máximo 1**;
- investigações de apoio: **máximo 2**;
- nenhum novo ataque principal enquanto o atual não entra em VERIFYING, DONE ou BLOCKED.

### Progresso confiável

A porcentagem é apenas orientação visual. O estado real vem de **evidência fresca**:
`branch/CI ao vivo > teste recente > leitura do código > JEV/HIVE > checkpoint histórico > estimativa`.

Se a evidência foi produzida para um head anterior e o código mudou na mesma superfície, o item volta para **STALE** até ser revalidado.

### Próximo alvo

O próximo ataque deve ser o item READY de maior impacto que:
1. não esteja bloqueado por dependência;
2. caiba em uma mudança pequena e reversível;
3. tenha critério de conclusão verificável;
4. reduza um gargalo real do produto.

Estado estruturado atual: `systems/harum_execution_panel.json`.


## CAMADA ESTRATÉGICA — ARTE DA GUERRA + METACOGNIÇÃO

Esta camada usa a **Arte da Guerra como metáfora de estratégia de produto**: o adversário é a incerteza, o retrabalho, o gargalo e a regressão — nunca pessoas.

### Terreno
Antes de agir, ler o terreno atual: branch, CI, rotas, viewport, dependências e superfície executável. Evidência de um deploy antigo não prova o head atual.

### Concentração
Um ataque principal por vez. Máximo de duas investigações auxiliares. Se tudo é prioridade, nada é prioridade.

### Inteligência
Antes de qualquer write relevante:
- **FATO:** o que sabemos por evidência?
- **HIPÓTESE:** qual causa provável?
- **CONFIANÇA:** baixa, média ou alta?
- **FALSIFICADOR:** o que provaria que a hipótese está errada?
- **MENOR AÇÃO:** qual mudança reversível gera informação útil?

### Terreno favorável
Preferir a camada em que a mudança é menor, reversível e fácil de verificar. Corrigir a causa antes de mascarar o sintoma.

### Recuo
Se uma mudança piorar build, navegação ou coerência, voltar ao último estado verificado e reformular a hipótese. Não empilhar remendos sobre hipótese falsificada.

## HORIZONTE DE PARALELISMO EXECUCIONAL

O objetivo não é fazer tudo ao mesmo tempo. É **executar simultaneamente apenas o que é realmente independente**, mantendo uma faixa crítica protegida contra colisões.

### Modelo de faixas

```text
LANE A · CRÍTICA       1 mutação principal por vez
LANE B · VERIFICAÇÃO   CI / QA / links / testes somente leitura
LANE C · PESQUISA      diagnóstico e inventário sem write conflitante
LANE D · ISOLADA       subtarefa com arquivos e dependências disjuntas

                 ↓ BARREIRA DE INTEGRAÇÃO ↓

          BUILD + CONTRATOS + QA AFETADO
```

### Teste PARALLEL_OK

Uma tarefa pode avançar em paralelo somente se:
1. toca arquivos/rotas diferentes;
2. não depende do resultado da outra;
3. pode ser revertida separadamente;
4. sua validação não mascara a outra;
5. existe uma barreira de integração no final.

Se qualquer resposta for **não**, serializar. Se o escopo for desconhecido, serializar até descobrir.

### Frescor por superfície

Evidência não vence apenas por idade; vence por **escopo afetado**.

- alteração só em docs/painel **não invalida** QA visual das páginas;
- alteração em CSS global **invalida** QA visual relacionado;
- alteração em config/build/dependências pode invalidar toda a cadeia.

### Anti-overparallelism

- nunca duas escritas no mesmo arquivo;
- nunca refatoração global em paralelo com QA final;
- nunca duas frentes tentando provar a mesma hipótese;
- capacidade disponível não é motivo suficiente para abrir outra lane.

A regra é: **paralelizar independência, serializar conflito, sincronizar na barreira**.


## MOTOR DE PRIORIDADE

Entre itens READY:

`score = 3×impacto + 2×desbloqueio + 2×redução_de_risco + confiança − esforço`

Cada fator usa escala 0–5. Exceções:
- P0 verificável vence o score;
- BLOCKED não compete;
- STALE precisa ser revalidado;
- empate favorece menor esforço e maior reversibilidade.

## CICLO ESTRATÉGICO

`VER TERRENO → ESCOLHER GARGALO → FORMULAR HIPÓTESE → TESTE PEQUENO → MEDIR → ATUALIZAR MODELO → AVANÇAR OU RECUAR`

Isso transforma o painel em um controlador de execução: ele não apenas mostra progresso; ele diz **quando atacar, quando testar, quando recuar e quando uma análise já virou paralisia**.


## ONDA EXECUTACIONAL ATUAL

```text
LANE A · CRÍTICA
HN-COHERENCE-15MIN
Resolver incoerência 12 min × 15 min ........ READY

LANE B · VERIFICAÇÃO
Responsive QA da PR .......................... DONE
Run #4 / 320 / 390 / 761 / 1024 ............. PASSOU

LANE C · PESQUISA
Inventário EN/ES e links de entrada .......... READY (somente leitura)

LANE D · DIAGNÓSTICO
Triagem de dependências ...................... READY (sem alterar pacote)

BARREIRA
CI + contratos + QA das superfícies tocadas .. OBRIGATÓRIA
```
