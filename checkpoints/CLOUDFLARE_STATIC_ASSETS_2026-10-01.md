# CHECKPOINT — CLOUDFLARE STATIC ASSETS 2026-10-01

## Diagnóstico
- Astro está configurado com `output: "static"`.
- GitHub Pages compila/publica o main com sucesso.
- `wrangler.json` apontava `main` para `./dist/_worker.js/index.js`.
- Esse Worker só é gerado quando o adapter Cloudflare/SSR é usado.
- O projeto atual não usa o adapter no `astro.config.mjs`.

## Correção
`wrangler.json` reduzido para Workers Static Assets:
- name
- compatibility_date
- assets.directory = ./dist
- sem `main`
- sem binding `ASSETS`

## Fonte técnica
Cloudflare documenta que `main` é opcional para assets-only Workers e que sites Astro estáticos podem ser publicados apenas com os assets gerados.

## Gate
Abrir PR e exigir preview Cloudflare verde antes de aplicar a correção a main.
