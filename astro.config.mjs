// @ts-check
import { defineConfig } from "astro/config";
import mdx from "@astrojs/mdx";
import sitemap from "@astrojs/sitemap";

export default defineConfig({
  site: "https://suryamayaharum-droid.github.io",
  base: "/astro-blog-starter-template",
  output: "static",
  redirects: { "/busca": "/buscar" },
  prefetch: { prefetchAll: false, defaultStrategy: "hover" },
  integrations: [mdx(), sitemap()],
});
