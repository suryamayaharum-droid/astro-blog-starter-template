# HARUMVERSO — CHECKPOINT PAGE FEEDS 2026-10-01

Estado: malha editorial programada em branch isolada, sincronizada com main no momento da validação.

Branch: `harumverso/page-feeds-2026-10-01`

## Arquitetura criada
- `src/data/ecosystem.ts`: registro central de hubs do ecossistema.
- `src/components/EcosystemRail.astro`: navegação reutilizável com BASE_URL e exclusão automática da página atual.

## Páginas conectadas
- /atelier
- /cadernos
- /temporadas
- /historia-da-arte
- /referencias
- /percursos
- /arquivo
- /cadernos/presenca
- /cadernos/gesto
- /cadernos/olhar
- /cadernos/memoria
- /cadernos/vestigio

## Alimentação editorial específica
- Ateliê → matéria/carvão/grafite e história.
- Cadernos → sketchbooks históricos.
- Temporadas → gesto/corpo/presença.
- Navegação cruzada → hubs do ecossistema sem retorno obrigatório à home.

## Correções
- Links internos adicionados à Temporada agora respeitam `import.meta.env.BASE_URL`.
- Home não foi inflada nesta frente.

## Validação estática
- branch: ahead 17 / behind 0 na checagem.
- EcosystemRail usa BASE_URL.
- EcosystemRail filtra hub atual.
- Caderno Memória mantém frontmatter válido e recebeu rail.
- Temporadas sem links absolutos `/biblioteca` e `/historia-da-arte` introduzidos por esta frente.

## Próximos gates
- [ ] PR/preview Cloudflare
- [ ] inspeção visual mobile
- [ ] navegação real entre rotas
- [ ] merge somente com gate técnico aceitável
- [ ] registrar recibo JEV/HIVE

## Recuperação
Se build/deploy falhar, retomar desta branch. Não remover a malha editorial sem erro técnico atribuído aos arquivos desta frente.
