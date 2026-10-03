# Auditoria funcional de rotas — 2026-10-03

## Escopo

Inventário do tree Astro no commit `5ccdae2`: 33 arquivos de rota, incluindo duas famílias dinâmicas. A página pública `/bancos/bndigital/` foi aberta antes da correção: seus seis temas mandavam para a mesma página genérica do acervo. As 13 fichas de bancos compartilham `src/pages/bancos/[id].astro`.

## Resultado da rodada

- Naveguei pelas 13 URLs de banco no Pages publicado. Todas carregaram, nenhuma manteve o rótulo antigo “abrir banco e pesquisar”.
- As 10 fichas não federadas exibem seis termos e seis ações distintas de cópia; as três federadas mantêm seus links de pesquisa interna com a consulta de cada tema (MET 6, AIC 7, CMA 6).
- Na BNDigital, os seis cliques exibiram a confirmação do termo escolhido. O catálogo oficial Sophia, o Acervo Digital e os direitos aparecem como portas separadas. O navegador de teste não disponibilizou uma leitura independente do clipboard; o retorno visível da página confirmou a ação.
- CI e Pages passaram no commit `5ccdae2`: Astro/TypeScript, contrato de controles, dry run, links internos e deploy.
- Qwen 0.5B quantizado Q8/CPU-WASM carregou e gerou texto no navegador de teste. A primeira resposta saiu do assunto; a versão seguinte inclui mapa explícito do site e substitui saída sem relação com a rota pela orientação verificada. A geração ainda precisa ser repetida após o deploy dessa proteção.
- A alternativa CPU usa mais memória e pode responder mais devagar. O teste em telefone Android real continua aberto.

## Inventário de rotas

| Rota ou família | Estado do inventário | Navegação manual |
|---|---|---|
| `/about/` | Mapeada | Pendente |
| `/arquivo/` | Mapeada | Pendente |
| `/artists/` | Mapeada | Pendente |
| `/atelier/` | Mapeada | Pendente |
| `/atlas/` | Mapeada | Pendente |
| `/bancos/` | Mapeada | Pendente |
| `/bancos/{id}/` (13 fichas) | Mapeada e navegada | 13/13 carregaram; 13/13 sem link genérico |
| `/biblioteca/` | Mapeada | Pendente |
| `/busca/` | Mapeada | Pendente |
| `/buscar/` | Mapeada | Pendente |
| `/cadernos/` | Mapeada | Pendente |
| `/cadernos/gesto/` | Mapeada | Pendente |
| `/cadernos/memoria/` | Mapeada | Pendente |
| `/cadernos/olhar/` | Mapeada | Pendente |
| `/cadernos/presenca/` | Mapeada | Pendente |
| `/cadernos/vestigio/` | Mapeada | Pendente |
| `/carta/` | Mapeada | Pendente |
| `/classics/` | Mapeada | Pendente |
| `/composicoes-autorais/` | Mapeada | Pendente |
| `/historia-da-arte/` | Mapeada | Pendente |
| `/` (home) | Mapeada | Pendente |
| `/museus/` | Mapeada | Pendente |
| `/newsletter/` | Mapeada | Pendente |
| `/noir/` | Mapeada | Pendente |
| `/outliers/` | Mapeada | Pendente |
| `/percursos/` | Mapeada | Pendente |
| `/referencias/` | Mapeada | Pendente |
| `/referencias/{slug}/` | Mapeada | Pendente |
| `/roubar-como-artista/` | Mapeada | Pendente |
| `/sketchbooks/` | Mapeada | Pendente |
| `/sobre/` | Mapeada | Pendente |
| `/temporadas/` | Mapeada | Pendente |
| `/vault/` | Mapeada | Pendente |

## Próximas verificações

- Repetir a geração da Lume após o deploy e confirmar que a resposta segue o mapa do site.
- Percorrer os outros 32 templates Astro, abrindo capas, páginas de detalhe e botões externos; registrar os destinos que não respondem ou não combinam com o conteúdo.
- Fazer teste específico em Android com memória limitada. Build/CI não substitui verificação de hardware.
- A Fundação Biblioteca Nacional pode restringir automação no portal; os destinos Sophia, Acervo Digital e direitos foram comparados com fontes oficiais indexadas.

## Progresso

- Fichas de bancos navegadas: `13/13`.
- Ações temáticas: `60/60` nas 10 fichas não federadas; `19/19` links federados preservam consulta temática.
- Templates Astro inventariados: `33/33`.
- Templates fora da família de bancos com navegação manual: `0/32`.
- IA local: download/carregamento Q8 e geração observados; qualidade de resposta e aparelho Android ainda em verificação.
