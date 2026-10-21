# Nova ↔ HARUM NOIR — contrato inicial de integração

Estado: **interface criada; runtime não conectado; não é uma implantação de agente**.

## Objetivo
Substituir a dependência de qualquer assistente legado por uma ponte explícita entre o site HARUM NOIR e o núcleo Nova/MEAW, sem misturar interface pública, memória privada e execução privilegiada.

## Descoberta realizada
- O repositório astro-blog-starter-template tem saída Astro estática (output: static).
- A página inicial examinada e a navegação principal não continham referências diretas a Lumi ou Lume.
- Portanto, a localização do componente legado não foi confirmada; não declarar remoção completa.
- A interface foi adicionada numa branch isolada e não altera main.

## Contrato proposto
A futura ponte de servidor deve:
1. aceitar apenas operações explicitamente permitidas;
2. validar método, origem, esquema e tamanho do corpo;
3. autenticar chamadas de servidor para servidor;
4. impor timeout, limite de resposta, rate limit e limites de custo;
5. nunca encaminhar segredos ao navegador nem registrar credenciais;
6. devolver estado explícito (connected, degraded, offline) com checked_at, runtime_version e capabilities;
7. falhar fechado: endpoint ausente ou erro não equivale a conectado;
8. não permitir execução arbitrária de código, acesso irrestrito à rede, elevação de privilégios ou auto-deploy.

## Hospedagem
O site atual é estático e usa @astrojs/cloudflare como dependência, mas astro.config.mjs declara output: static. Antes de adicionar API dinâmica, escolher e validar um runtime autorizado compatível com a hospedagem atual. Não habilitar GitHub Actions nem alterar configuração de publicação nesta etapa.

## Próximas etapas
1. Identificar o componente real da Lumi/Lume ou confirmar que reside noutro repositório/serviço.
2. Selecionar runtime de servidor e definir variáveis secretas no painel do provedor.
3. Implementar endpoint de status e adaptador de chat mínimo, somente após aprovar o provedor.
4. Testar desconexão, timeout, autenticação, rate limit e conteúdo inválido.
5. Atualizar estado para conectado somente após uma verificação real.
6. Revisar acessibilidade, privacidade, custo e conteúdo antes de promover a branch.

## Evidência
A página pública src/pages/nova.astro é uma interface de status/documentação. Não faz chamadas de rede e não inicia processos Nova.
