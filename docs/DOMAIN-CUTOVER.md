# Configuração do domínio Arte Harum

Este projeto continua hospedado como site estático no GitHub Pages. A mudança para domínio próprio fica desativada enquanto a variável PUBLIC_SITE_URL não estiver definida.

## Quando o domínio estiver registrado

1. Verifique a propriedade do domínio na conta GitHub que publica este site.
2. Em Settings → Pages, cadastre arteharum.com.br antes de apontar o DNS.
3. No provedor DNS, configure os registros A do domínio raiz para 185.199.108.153, 185.199.109.153, 185.199.110.153 e 185.199.111.153. Para www, configure CNAME para suryamayaharum-droid.github.io.
4. Em Settings → Secrets and variables → Actions → Variables, crie PUBLIC_SITE_URL com o valor https://arteharum.com.br.
5. Rode o workflow de publicação. Ele constrói as páginas com base na raiz, atualiza sitemaps e URLs públicas e cria páginas de redirecionamento para o antigo caminho /astro-blog-starter-template/.
6. Confirme HTTPS nas configurações do Pages e valide as rotas principais, sitemaps, canonical e alternates.

## Enquanto o domínio não estiver registrado

Deixe PUBLIC_SITE_URL vazia. O build continuará em https://suryamayaharum-droid.github.io/astro-blog-starter-template/ sem alterar o site publicado.

O teste de CI também constrói a variante customizada sem publicá-la. O domínio e a hospedagem são cobranças distintas: o GitHub Pages pode permanecer no plano gratuito; o registro do domínio é pago e renovável.
