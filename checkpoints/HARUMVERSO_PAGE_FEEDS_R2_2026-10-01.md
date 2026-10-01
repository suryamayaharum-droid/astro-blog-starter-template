# HARUMVERSO — PAGE FEEDS R2 · 2026-10-01

Base de criação: main pós-Radar R3. Divergência posterior verificada: apenas Header recebeu navegação do catálogo de museus; não há colisão com esta frente.

## Arquitetura
- `src/data/ecosystem.ts`: registro central dos hubs.
- `src/components/EcosystemRail.astro`: rail horizontal nativo, scroll-snap, BASE_URL, sem JavaScript adicional.

## Conectado
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

## Alimentação específica
- Ateliê → matéria negra + história.
- Cadernos → arquivo vivo / sketchbooks.
- Temporadas → gesto-corpo-presença.
- Cadernos internos → saída para o restante do ecossistema.

## UX
- Reutiliza `.rail` e `.card` existentes.
- Mobile usa swipe horizontal e cards largos.
- Home não foi alterada.
