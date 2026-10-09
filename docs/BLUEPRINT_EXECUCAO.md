# HARUM NOIR — BLUEPRINT DE EXECUÇÃO

> Painel operacional da evolução do GitHub Pages. Este arquivo existe para impedir perda de contexto, duplicação de trabalho e avanço sem validação.

## REGRA DE ATAQUE

Fluxo obrigatório:

`DIAGNOSTICAR → PRIORIZAR → CORRIGIR → VALIDAR → REGISTRAR → PRÓXIMO ALVO`

Uma frente só recebe **CONCLUÍDO** quando há evidência. Build verde não significa que revisão visual/mobile está concluída.

## PAINEL GERAL

```text
HARUM NOIR · GITHUB PAGES
Progresso estrutural estimado: 94%

[████████████████████] CI / Astro / TypeScript ........ CONCLUÍDO
[████████████████████] Cloudflare dry-run ............. CONCLUÍDO
[████████████████████] Links internos / assets ........ CONCLUÍDO pelo CI
[████████████████████] hreflang recíproco ............. CONCLUÍDO pelo CI
[████████████████████] SEO estrutural / JSON-LD ....... CONCLUÍDO pelo CI
[████████████████████] contrato Studio23 ↔ Noir ....... CONCLUÍDO pelo CI
[████████████████████] ciclo pedagógico ............... CONCLUÍDO / QA VERDE
[███████████████████░] coerência entre páginas ........ 96% / CONCLUÍDO
[████████████████████] responsividade visual .......... QA #72 VERDE
[██████████████████░░] acessibilidade visual/teclado .. 88% / VERIFYING
[██████████████████░░] EN/ES / redundâncias .......... 90% / VERIFYING
[████████████████████] dependências / segurança ...... TRIAGEM CONCLUÍDA
[███████░░░░░░░░░░░░░] merge/publicação .............. 35% / DRAFT
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

Última evidência verde confirmada de produto: **HARUM NOIR CI #562** + **Responsive Audit #72** no head `a367f2f`. A auditoria responsiva usa o estado integrado da PR com a `main`, incluindo o fluxo Referências → Cadernos.


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

Isso transforma o painel em um controlador de execução: ele não apenas mostra progresso; ele diz **quando atacar, quando testar, quando recuar e o que pode avançar em paralelo sem colisão**.


## ONDA EXECUTACIONAL ATUAL

```text
LANE A · CRÍTICA — PRONTIDÃO DE RELEASE
CI #562 ................................... VERDE
Responsive Audit #72 ...................... VERDE
Estado integrado PR + main ............... TESTADO
PR #78 .................................... DRAFT
Merge automático/publicação ............... NÃO AUTORIZADO

LANE B · PRODUTO
Ciclo pedagógico .......................... DONE
Mesa Referências → Cadernos ............... DONE
Rituais / pesquisa assimilada ............. DONE
Radar → fonte / aplicação ................. DONE
Busca → item exato do Radar ............... DONE

LANE C · I18N / ACESSIBILIDADE
Rotas internacionais ...................... 12 EN + 12 ES
Google Translate no código auditado ....... 0
Chrome nativo de aulas EN/ES .............. APLICADO
Alvos de toque em headers/seletor idiomas . AMPLIADOS
Revisão fina de copy ...................... VERIFYING

LANE D · SEGURANÇA / INFRA
npm / dependências ........................ TRIADO
Vite 6.4.1 ................................ manutenção futura
@astrojs/cloudflare 12.6.12 ............... manutenção futura
Astro 5.16.9 .............................. site atual é static
npm audit fix --force ..................... PROIBIDO
Workers Build externo ..................... FALHA / CAUSA NÃO PROVADA
Cloudflare dry-run do CI .................. VERDE

BARREIRA
PR continua draft. Separar falha externa de Cloudflare da prontidão real do GitHub Pages antes de qualquer merge.
```

## PESQUISA DE SITES COMO PROPOSTA — ASSIMILAÇÃO ATUAL

A pesquisa não entra como lista de links. Cada referência externa precisa produzir uma mudança de método, navegação, repertório ou prática.

### Padrões assimilados

- **Project Zero / Harvard:** observação, evidência, pergunta e documentação do pensamento.
- **MoMA:** desacelerar e variar o ponto de vista antes de interpretar.
- **Smarthistory:** separar descrição formal de contexto e narrativa.
- **Getty:** olhar, conferir a fonte, produzir e refletir.
- **Rijksmuseum:** comparar, criar conjuntos e transformar acervo em relação.
- **Smithsonian Open Access:** coleção aberta como matéria-prima para criação.
- **Public Domain Review:** tema, época, mídia e curadoria como portas de entrada.
- **Google Arts & Culture:** múltiplas entradas para quem ainda não sabe o nome do que procura.
- **Royal Drawing School:** repertório + exercício + processo convivendo no mesmo arquivo.
- **Art Prof:** trilhas auto-organizadas, continuidade e saídas concretas.
- **Proko:** conceito → demonstração → projeto → crítica/retorno.

### O que já virou produto

```text
/rituais-de-olhar ............. CRIADO
Home → Observar ............... aponta para Rituais
Ateliê ........................ ganhou preparação do olhar
Museus ........................ conecta acervo a ritual
Referências ................... conecta estudo a ritual
Atlas ......................... 5 etapas: observar/pesquisar/estruturar/organizar/praticar
Busca ......................... ganhou perguntas de entrada
Radar ......................... novo repertório aberto + métodos de desenho
llms.txt ...................... nova rota registrada
```

### Regra

`PESQUISAR → EXTRAIR PRINCÍPIO → REESCREVER NA LINGUAGEM HARUM → APLICAR → VALIDAR`

Não copiar texto, identidade, rotina nomeada ou arquitetura alheia. O valor está em **assimilar o mecanismo** e fazê-lo servir ao ciclo pedagógico HARUM NOIR.


## MICROCURADORIA — COMPARAR ANTES DE ACUMULAR

A assimilação da pesquisa avançou da navegação para **relação entre referências**.

```text
REFERÊNCIAS
selecionar 2–3
      ↓
MESA DE COMPARAÇÃO
o que permanece?
onde divergem?
o que vira decisão minha?
      ↓
NOTA DO ALUNO
      ↓
CADERNOS
receber a nota
      ↓
ATELIÊ
testar sem a referência aberta
```

A seleção e a nota ficam somente no navegador do aluno. A intenção é transformar “salvar referência” em uma microcuradoria com saída verificável.

Barreira atual: CI + QA responsivo completo do fluxo Referências → Cadernos.


## TRIAGEM DE SEGURANÇA — SEM UPGRADE CEGO

A frente de dependências foi analisada sem `npm audit fix --force`.

- **Vite 6.4.1** aparece na árvore e possui advisories de dev server corrigidos em 6.4.2. A condição relevante exige servidor de desenvolvimento exposto; o produto público atual é estático.
- **@astrojs/cloudflare 12.6.12** está instalado, mas não é importado pelo `astro.config.mjs`; o site usa `output: "static"`. A atualização para a linha corrigida deve ser uma onda própria de manutenção/compatibilidade.
- **Astro 5.16.9** tem advisory posterior relacionado a SSR/custom-server. O caminho público do HARUM NOIR é `output: "static"`, então não corresponde ao cenário de produção atual.
- O check externo **Workers Builds** continua falhando em PRs enquanto o `Cloudflare dry-run` interno passa. Sem log autenticado do painel Cloudflare, a causa externa permanece não provada.

Decisão: não transformar uma PR editorial grande em upgrade de framework. Registrar, isolar e corrigir dependências em uma manutenção compatível e testada.
