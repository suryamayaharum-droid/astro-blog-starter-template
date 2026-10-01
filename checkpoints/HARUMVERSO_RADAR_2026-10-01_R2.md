# HARUMVERSO — CHECKPOINT RADAR 2026-10-01 R2

Estado: lote reconciliado sobre o main atual após detectar divergência da branch R1.
Branch: `harumverso/radar-2026-10-01-r2`
Commit de conteúdo: `97d33284200cb53b71344f800d2c37637291b0b8`

## Motivo da R2
A branch original ficou 5 commits atrás de main enquanto outras instâncias avançaram o site. O preview Cloudflare da R1 falhou e o PR ficou não-mergeável. Em vez de forçar merge, este checkpoint reaplica somente o lote editorial verificado sobre o main atual.

## Preservado
- Todo o trabalho novo já presente em main.
- 3 coleções do radar: sketchbooks, gesto/corpo/presença e matéria negra.
- Metadados de direitos e política link-only para recursos educacionais.
- Histórico R1 continua disponível para auditoria.

## Gates
- [ ] preview/build Cloudflare da R2
- [ ] inspeção visual /biblioteca mobile
- [ ] link-health
- [ ] merge em main
- [ ] registro JEV/HIVE pós-publicação

## Regra de recuperação
Se houver falha, retomar desta branch e deste commit. Não voltar à R1 nem reconstruir o lote.


## Diagnóstico de continuidade — gate Cloudflare
- PR #4 confirmado mergeável e sincronizado: ahead 2 / behind 0.
- Auditoria do dataset: 8 coleções, 36 URLs, 0 IDs duplicados, 0 URLs duplicadas.
- `/biblioteca` consome `openLibraryCollections`.
- Cloudflare tentou preview do commit `f2e4c05...` e retornou Build Failed.
- GitHub não fornece checks/statuses de CI para este projeto; inclusive o head atual de main aparece pending com 0 statuses.
- Portanto a falha de preview deve ser tratada como gate de infraestrutura/deploy até haver log técnico que atribua erro ao lote.
- NÃO alterar/remover as coleções para “corrigir build” sem evidência de erro em `openLibrary.ts`.
- NÃO fazer merge enquanto o preview estiver vermelho.


## Baseline de infraestrutura
- Main validado no commit `1e7b94203b06e197a771ffbbbab6933de8ea141d`.
- Harumverso CI: success.
- GitHub Pages deploy: success.
- Este commit de checkpoint força nova validação do PR contra o baseline corrigido.
