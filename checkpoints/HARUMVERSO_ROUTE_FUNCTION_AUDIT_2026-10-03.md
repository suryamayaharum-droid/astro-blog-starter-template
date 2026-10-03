# Auditoria funcional de rotas — 2026-10-03

## Escopo e evidência

Inventário gerado do tree Astro de `main`: 33 arquivos de rota, incluindo duas famílias dinâmicas. A página pública `/bancos/bndigital/` foi aberta no navegador antes da correção; seis botões de tema apontavam para a mesma página inicial do acervo. O repositório tem 13 fichas de bancos que compartilham `src/pages/bancos/[id].astro`.

## Correção em andamento

- Nas fichas não federadas, cada tema passa a oferecer cópia do termo e uma porta oficial para o acervo.
- BNDigital passa a apontar a pesquisa para o catálogo oficial Sophia; a porta de visão geral do Acervo Digital e a página de direitos continuam disponíveis.
- A Lume escolhe Qwen quantizado Q4F16/WebGPU quando há `shader-f16`; caso contrário tenta Q8/CPU-WASM. Os pesos ficam no cache do navegador após ativação. Isso não instala um aplicativo no Android.
- A checagem de build valida as 13 fichas, as seis ações BNDigital e os dois caminhos quantizados; o verificador de links internos já percorre todas as páginas HTML geradas.

## Inventário de rotas

| Rota ou família | Estado do inventário | Estado de navegação manual |
|---|---|---|
| `/about/` | Inventariado no fonte | Não percorrido no navegador nesta rodada |
| `/arquivo/` | Inventariado no fonte | Não percorrido no navegador nesta rodada |
| `/artists/` | Inventariado no fonte | Não percorrido no navegador nesta rodada |
| `/atelier/` | Inventariado no fonte | Não percorrido no navegador nesta rodada |
| `/atlas/` | Inventariado no fonte | Não percorrido no navegador nesta rodada |
| `/bancos/` | Inventariado no fonte | Não percorrido no navegador nesta rodada |
| `/bancos/{id}/ (13 bancos; ficha compartilhada)` | Inventariado no fonte | Não percorrido no navegador nesta rodada |
| `/biblioteca/` | Inventariado no fonte | Não percorrido no navegador nesta rodada |
| `/busca/` | Inventariado no fonte | Não percorrido no navegador nesta rodada |
| `/buscar/` | Inventariado no fonte | Não percorrido no navegador nesta rodada |
| `/cadernos/` | Inventariado no fonte | Não percorrido no navegador nesta rodada |
| `/cadernos/gesto/` | Inventariado no fonte | Não percorrido no navegador nesta rodada |
| `/cadernos/memoria/` | Inventariado no fonte | Não percorrido no navegador nesta rodada |
| `/cadernos/olhar/` | Inventariado no fonte | Não percorrido no navegador nesta rodada |
| `/cadernos/presenca/` | Inventariado no fonte | Não percorrido no navegador nesta rodada |
| `/cadernos/vestigio/` | Inventariado no fonte | Não percorrido no navegador nesta rodada |
| `/carta/` | Inventariado no fonte | Não percorrido no navegador nesta rodada |
| `/classics/` | Inventariado no fonte | Não percorrido no navegador nesta rodada |
| `/composicoes-autorais/` | Inventariado no fonte | Não percorrido no navegador nesta rodada |
| `/historia-da-arte/` | Inventariado no fonte | Não percorrido no navegador nesta rodada |
| `/ (home)` | Inventariado no fonte | Não percorrido no navegador nesta rodada |
| `/museus/` | Inventariado no fonte | Não percorrido no navegador nesta rodada |
| `/newsletter/` | Inventariado no fonte | Não percorrido no navegador nesta rodada |
| `/noir/` | Inventariado no fonte | Não percorrido no navegador nesta rodada |
| `/outliers/` | Inventariado no fonte | Não percorrido no navegador nesta rodada |
| `/percursos/` | Inventariado no fonte | Não percorrido no navegador nesta rodada |
| `/referencias/` | Inventariado no fonte | Não percorrido no navegador nesta rodada |
| `/referencias/{slug}/ (páginas do atlas)` | Inventariado no fonte | Não percorrido no navegador nesta rodada |
| `/roubar-como-artista/` | Inventariado no fonte | Não percorrido no navegador nesta rodada |
| `/sketchbooks/` | Inventariado no fonte | Não percorrido no navegador nesta rodada |
| `/sobre/` | Inventariado no fonte | Não percorrido no navegador nesta rodada |
| `/temporadas/` | Inventariado no fonte | Não percorrido no navegador nesta rodada |
| `/vault/` | Inventariado no fonte | Não percorrido no navegador nesta rodada |

## Itens que continuam abertos

- Recarregar a página BNDigital publicada e testar os seis controles de cópia, o catálogo Sophia e o botão de direitos.
- Fazer um teste de geração real do Qwen em GPU e CPU/WASM, incluindo aparelho Android com pouca memória. A checagem de código não substitui esse teste de hardware.
- Percorrer visualmente as demais páginas, verificar se capas levam a conteúdo completo e registrar botões externos que não respondam.
- A origem BNDigital pode bloquear acesso automatizado; o destino oficial foi conferido por seu catálogo e pela documentação pública da Fundação Biblioteca Nacional.

## Barra inicial

- BNDigital ao vivo antes da correção: `6/6` alvos genéricos detectados.
- Fichas compartilhadas cobertas pelo código: `13`.
- Templates Astro inventariados: `33`.
- Navegação de visitante após deploy: `pendente de nova publicação`.
