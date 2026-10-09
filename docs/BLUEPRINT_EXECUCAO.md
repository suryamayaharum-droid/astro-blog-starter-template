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
