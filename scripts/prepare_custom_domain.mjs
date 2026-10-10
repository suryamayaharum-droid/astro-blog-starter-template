import fs from "node:fs/promises";
import path from "node:path";

const root = path.resolve("dist");
const requestedSite = process.env.PUBLIC_SITE_URL?.trim();
const oldSitePrefix = "https://suryamayaharum-droid.github.io/astro-blog-starter-template";

if (!requestedSite) {
  console.log("Custom-domain preparation skipped; PUBLIC_SITE_URL is unset.");
  process.exit(0);
}

const site = new URL(requestedSite);
if (site.origin !== "https://arteharum.com.br" || site.pathname !== "/") {
  throw new Error("PUBLIC_SITE_URL must be exactly https://arteharum.com.br");
}

async function walk(dir) {
  const files = [];
  for (const entry of await fs.readdir(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) files.push(...await walk(full));
    else if (entry.isFile()) files.push(full);
  }
  return files;
}

const textExtensions = new Set([".html", ".xml", ".txt", ".json", ".webmanifest", ".js", ".css", ".svg", ".mjs"]);
const files = await walk(root);
let rewritten = 0;

for (const file of files) {
  if (!textExtensions.has(path.extname(file).toLowerCase())) continue;
  const original = await fs.readFile(file, "utf8");
  const updated = original.replaceAll(oldSitePrefix, site.origin);
  if (updated !== original) {
    await fs.writeFile(file, updated);
    rewritten += 1;
  }
}

function escapeAttribute(value) {
  return value.replaceAll("&", "&amp;").replaceAll('"', "&quot;").replaceAll("<", "&lt;");
}

const htmlFiles = files.filter((file) => file.endsWith(".html"));
let redirects = 0;
const legacyRoot = path.join(root, "astro-blog-starter-template");

for (const file of htmlFiles) {
  const relative = path.relative(root, file).split(path.sep).join("/");
  if (relative === "astro-blog-starter-template" || relative.startsWith("astro-blog-starter-template/")) continue;

  const html = await fs.readFile(file, "utf8");
  const canonical = html.match(/<link[^>]*\brel="canonical"[^>]*\bhref="([^"]+)"/i)?.[1];
  const route = relative === "index.html"
    ? "/"
    : relative.endsWith("/index.html")
      ? "/" + relative.slice(0, -"index.html".length)
      : "/" + relative;
  const destination = canonical || new URL(route, site.origin).href;
  const safeDestination = escapeAttribute(destination);
  const alias = path.join(legacyRoot, ...relative.split("/"));

  const redirectPage = [
    "<!doctype html>",
    '<html lang="pt-BR"><head><meta charset="utf-8">',
    '<meta name="robots" content="noindex,follow">',
    '<meta name="viewport" content="width=device-width,initial-scale=1">',
    "<title>Página movida · Arte Harum</title>",
    '<link rel="canonical" href="' + safeDestination + '">',
    '<meta http-equiv="refresh" content="0;url=' + safeDestination + '">',
    "</head><body>",
    '<p>Esta página mudou de endereço. <a href="' + safeDestination + '">Abrir Arte Harum</a></p>',
    "<script>location.replace(" + JSON.stringify(destination) + ");</script>",
    "</body></html>"
  ].join("\n");

  await fs.mkdir(path.dirname(alias), { recursive: true });
  await fs.writeFile(alias, redirectPage);
  redirects += 1;
}

console.log("Custom-domain preparation: " + rewritten + " text files updated; " + redirects + " legacy path redirects created.");
