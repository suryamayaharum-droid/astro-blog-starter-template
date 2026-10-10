// @ts-check
import { defineConfig } from "astro/config";
import mdx from "@astrojs/mdx";
import sitemap from "@astrojs/sitemap";

const defaultSite = "https://suryamayaharum-droid.github.io";
const defaultBase = "/astro-blog-starter-template";
const customSite = process.env.PUBLIC_SITE_URL?.trim();

if (customSite) {
  const parsed = new URL(customSite);
  if (parsed.protocol !== "https:" || parsed.origin !== "https://arteharum.com.br" || parsed.pathname !== "/") {
    throw new Error("PUBLIC_SITE_URL must be exactly https://arteharum.com.br/");
  }
}

export default defineConfig({
  site: customSite || defaultSite,
  base: customSite ? "/" : defaultBase,
  output: "static",
  prefetch: { prefetchAll: false, defaultStrategy: "hover" },
  integrations: [mdx(), sitemap()],
});
