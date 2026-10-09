# HARUM NOIR · Painel de execução GitHub · 9 out 2026

**Escopo:** melhoria delimitada no GitHub Pages, sem alterações fora do repositório.
**Marca pública:** HARUM NOIR. “Harumverso” permanece como nome interno do ecossistema.

## Barra de progresso

`██████████ 100% · coleção publicada e auditorias concluídas`

- [x] Confirmar main e verificar sobreposição com PR #78.
- [x] Criar branch independente `feat/colecao-lugares-20261009`.
- [x] Criar rota `/colecoes/lugares/` com quatro estudos ilustrados.
- [x] Ligar a nova rota à oitava coleção em `/colecoes/`.
- [x] Abrir PR #84; CI do PR passou.
- [x] Confirmar rota publicada, quatro imagens carregadas, links do cartão e layout sem overflow.
- [x] Incluir a nova rota na matriz de auditoria móvel pós-deploy.
- [ ] Criar versões localizadas EN/ES após o PR #78 liberar os hubs.

## Diagnóstico e decisão

A Coleção Visual em português já possuía imagens e sete caminhos; faltava uma coleção que desse destino concreto a imagens de espaços e ambientes. A nova trilha transforma ateliê, galeria, jardim botânico e arquivo brasileiro em práticas de observação e liga cada uma a um acervo institucional.

As imagens são artes editoriais locais já versionadas. Elas não são apresentadas como fotografias de museus ou documentos históricos. Cada cartão separa a pergunta visual da pesquisa de fonte e informa que direitos devem ser lidos na ficha institucional.

## Entrega integrada: PR #84 squash-merged em `main` (`d15a5c5`) e publicada no GitHub Pages. Estado dos arquivos

| Arquivo | Mudança | Estado |
|---|---|---|
| `src/pages/colecoes/lugares.astro` | Nova aula visual com quatro ambientes, exercícios de 8 minutos, imagens, links aos guias de banco e acervos oficiais. | Implementado; CI pendente |
| `src/pages/colecoes.astro` | Oitavo cartão de coleção, com imagem pertinente e destino da aula. | Implementado; CI pendente |
| Hubs EN/ES e `InternationalHub.astro` | Não alterados nesta rodada: estão no escopo do PR #78. | Aguardando integração para localização sem conflito |
| `.github/workflows/noir-mobile-visual-audit.yml` | Adiciona a rota nova à matriz de auditoria pós-deploy. | Concluído; run 37990935006 verde, incluindo a nova rota |

## Coordenação e validação

- Base `main`: `40592075c25b9fe060222f0814b2ffb4aa5155e2`.
- PR #78 segue aberto em rascunho e altera os hubs EN/ES e o componente internacional; checks lidos nesta rodada: CI e auditoria responsiva verdes no head consultado.
- Esta branch evita esses arquivos. A validação conclusiva depende dos checks do GitHub; a matriz móvel executa após a publicação.
- Nenhuma imagem foi gerada nesta rodada; os assets locais existentes foram reutilizados.

## Próximo passo

Abrir o PR desta coleção, ler o resultado de todos os checks no head atual e corrigir qualquer erro antes de chamar a entrega de concluída. Depois, integrar as versões EN/ES e a rota à matriz responsiva quando o PR #78 liberar os hubs.
