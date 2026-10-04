import fs from "node:fs/promises";
import vm from "node:vm";
import path from "node:path";

const EXPECTED = {
  STUDIO_SITE: "https://tattoostudio23.suryamaya-harum.chatgpt.site/",
  STUDIO_NOIR: "https://tattoostudio23.suryamaya-harum.chatgpt.site/harum-noir/",
};

const constsPath = path.resolve("src/consts.ts");
const headerPath = path.resolve("src/components/Header.astro");
const footerPath = path.resolve("src/components/Footer.astro");
const ecosystemPath = path.resolve("src/data/ecosystem.ts");
const atlasPath = path.resolve("src/pages/atlas.astro");
const lumePath = path.resolve("src/components/LumeGuide.astro");
const galleriesPath = path.resolve("src/data/sketchbookGalleries.ts");
const galleriesPagePath = path.resolve("src/pages/sketchbooks.astro");

const [consts, header, footer, ecosystem, atlas, lume, galleries, galleriesPage] = await Promise.all([
  fs.readFile(constsPath, "utf8"),
  fs.readFile(headerPath, "utf8"),
  fs.readFile(footerPath, "utf8"),
  fs.readFile(ecosystemPath, "utf8"),
  fs.readFile(atlasPath, "utf8"),
  fs.readFile(lumePath, "utf8"),
  fs.readFile(galleriesPath, "utf8"),
  fs.readFile(galleriesPagePath, "utf8"),
]);

const failures = [];

for (const [name, expected] of Object.entries(EXPECTED)) {
  const pattern = new RegExp(`export\\s+const\\s+${name}\\s*=\\s*["']([^"']+)["']`);
  const match = consts.match(pattern);
  if (!match) {
    failures.push(`${name} is not exported from src/consts.ts`);
    continue;
  }
  if (match[1] !== expected) {
    failures.push(`${name} must be ${expected}, found ${match[1]}`);
  }
}

if (!/import\s*\{[^}]*STUDIO_SITE[^}]*\}\s*from\s*['"]\.\.\/consts['"]/.test(header)) {
  failures.push("Header must import STUDIO_SITE from src/consts.ts");
}
if (!header.includes("href={STUDIO_SITE}")) {
  failures.push("Header must link back to Studio 23 through STUDIO_SITE");
}
if (!/import\s*\{[^}]*STUDIO_SITE[^}]*STUDIO_NOIR[^}]*\}\s*from\s*['"]\.\.\/consts['"]/.test(footer) &&
    !/import\s*\{[^}]*STUDIO_NOIR[^}]*STUDIO_SITE[^}]*\}\s*from\s*['"]\.\.\/consts['"]/.test(footer)) {
  failures.push("Footer must import STUDIO_SITE and STUDIO_NOIR from src/consts.ts");
}
if (!footer.includes("href={STUDIO_SITE}")) {
  failures.push("Footer must expose the canonical Studio 23 site link");
}
if (!footer.includes("href={STUDIO_NOIR}")) {
  failures.push("Footer must expose the canonical Studio 23 Harum Noir bridge");
}

const requiredHubs = ["bancos", "sketchbooks", "composicoes-autorais"];
for (const slug of requiredHubs) {
  const hubLine = ecosystem.split("\n").find((line) => line.includes('id:"' + slug + '"'));
  if (!hubLine || !hubLine.includes('href:"' + slug + '"')) failures.push("ecosystem hub missing or misrouted: " + slug);
  if (!atlas.includes('"' + slug + '"')) failures.push("Atlas door missing: " + slug);
}
if (!/bndigital\s*:\s*\{\s*href\s*:\s*base\s*\+\s*['"]bancos\/bndigital\/['"]/.test(lume)) failures.push("Lume must link directly to the BNDigital detail page");
if (!/banks\s*:\s*\{\s*href\s*:\s*base\s*\+\s*['"]bancos\/['"]/.test(lume)) failures.push("Lume must expose the image banks catalog");
const localeRuntime = lume.match(/const supportedLocales=new Set\(\[[^\]]+\]\);\s*const browserLocale=\(\)=>\{[\s\S]*?\n\s*};\s*const detectLocale=\(raw\)=>\{[\s\S]*?\n\s*};/);
if (!localeRuntime) {
  failures.push("Lume locale detector could not be extracted for runtime checks");
} else {
  const localeCases = [
    { query: "Biblioteca Nacional", browser: "pt-BR", expected: "pt" },
    { query: "biblioteca nacional", browser: "es-MX", expected: "es" },
    { query: "bancos de imágenes", browser: "pt-BR", expected: "es" },
    { query: "bancos de imagenes", browser: "pt-BR", expected: "es" },
    { query: "BNDigital", browser: "en-US", expected: "pt" },
  ];
  for (const test of localeCases) {
    const context = {
      navigator: { languages: [test.browser], language: test.browser },
      document: { documentElement: { lang: test.browser } },
    };
    vm.runInNewContext(localeRuntime[0] + "\nglobalThis.__detectLocale = detectLocale;", context);
    const actual = context.__detectLocale(test.query);
    if (actual !== test.expected) {
      failures.push("Lume locale mismatch for \"" + test.query + "\": expected " + test.expected + ", received " + actual);
    }
  }
}
if (galleries.includes("images: []")) failures.push("Every indexed sketchbook must have at least one reviewed gallery image");
if (!galleriesPage.includes("gallery-image-fallback")) failures.push("Sketchbook image tiles must degrade to a source-linked fallback");

const directUrlFiles = [];
async function walk(dir) {
  for (const entry of await fs.readdir(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) await walk(full);
    else if (entry.isFile()) {
      let text;
      try { text = await fs.readFile(full, "utf8"); } catch { continue; }
      if (text.includes("tattoostudio23.suryamaya-harum.chatgpt.site") && path.resolve(full) !== constsPath) {
        directUrlFiles.push(path.relative(process.cwd(), full));
      }
    }
  }
}
await walk(path.resolve("src"));

if (directUrlFiles.length) {
  failures.push(
    "Studio 23 canonical URL must stay centralized in src/consts.ts; duplicated in: " +
    directUrlFiles.join(", ")
  );
}

const summary = {
  studioSite: EXPECTED.STUDIO_SITE,
  studioNoir: EXPECTED.STUDIO_NOIR,
  headerBridge: header.includes("href={STUDIO_SITE}"),
  footerSiteBridge: footer.includes("href={STUDIO_SITE}"),
  footerNoirBridge: footer.includes("href={STUDIO_NOIR}"),
  duplicatedCanonicalUrlFiles: directUrlFiles,
  requiredHubs,
  emptySketchbookGallery: galleries.includes("images: []"),
  galleryImageFallback: galleriesPage.includes("gallery-image-fallback"),
  failures,
};

await fs.writeFile("ecosystem-contract-health.json", JSON.stringify(summary, null, 2));

if (failures.length) {
  for (const failure of failures) console.error("ECOSYSTEM CONTRACT:", failure);
  process.exit(1);
}

console.log("Ecosystem contract passed: Studio bridges, image galleries, Atlas doors, and Lume routes are intact.");
