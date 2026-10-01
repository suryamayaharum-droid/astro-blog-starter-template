# HARUMVERSO — MAPA DE PARALELISMO 2026-10-01

## Trilha A — Publicação R2
Owner lógico: deploy/integrador
Branch: harumverso/radar-2026-10-01-r2
Estado: conteúdo validado; preview Cloudflare vermelho.
Pode fazer: investigar logs/configuração de build, revalidar preview, merge somente com gate verde.
Não pode fazer: remover coleções sem erro técnico atribuído ao dataset.

## Trilha B — Radar editorial NEXT
Owner lógico: pesquisa/curadoria
Branch: harumverso/radar-next-2026-10-01
Estado: fila curada ativa.
Pode fazer: descobrir, verificar direitos, deduplicar, registrar princípio/destino.
Não pode fazer: promover para main enquanto R2 não estiver resolvida.

## Trilha C — UX Biblioteca
Owner lógico: design/front-end
Base recomendada: main em branch própria.
Escopo: mobile swipe, carrosséis, hierarquia editorial, leitura progressiva, performance e acessibilidade.
Regra: não editar openLibrary.ts. Consumir o dataset existente.

## Trilha D — Acervo visual
Owner lógico: arquivo/licenças
Escopo: inventário de imagens reutilizáveis; hash/origem/licença/autor/obra/instituição.
Regra: nenhuma imagem entra no site sem proveniência e direitos registrados.

## Trilha E — JEV/HIVE
Owner lógico: coordenação
Escopo: consolidar recibos, branches, checkpoints, decisões e handoffs.
Regra: JEV aponta para estados; não duplica o acervo inteiro.

## Convergência
R2 verde + UX validada + radar NEXT deduplicado -> rebase sequencial -> preview -> merge -> recibo JEV.
