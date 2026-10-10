// @ts-check
import { defineConfig } from "astro/config";
import mdx from "@astrojs/mdx";
import sitemap from "@astrojs/sitemap";

const defaultSite = "https://suryamayaharum-droid.github.io";
const defaultBase = "/astro-blog-starter-template";
const customSiteInput = process.env.PUBLIC_SITE_URL?.trim();
const customSite = customSiteInput ? new URL(customSiteInput) : null;

if (customSite && (customSite.protocol !== "https:" || customSite.origin !== "https://arteharum.com.br" || customSite.pathname !== "/")) {
  throw new Error("PUBLIC_SITE_URL must be exactly https://arteharum.com.br");
}

export default defineConfig({
  site: customSite?.origin || defaultSite,
  base: customSite ? "/" : defaultBase,
  output: "static",
  prefetch: { prefetchAll: false, defaultStrategy: "hover" },
  integrations: [mdx(), sitemap()],
});
