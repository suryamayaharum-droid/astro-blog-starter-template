import fs from "node:fs/promises";
import path from "node:path";

const EXPECTED = {
  STUDIO_SITE: "/astro-blog-starter-template/studio23/",
  STUDIO_NOIR: "/astro-blog-starter-template/studio23/harum-noir/",
};

const constsPath = path.resolve("src/consts.ts");
const headerPath = path.resolve("src/components/Header.astro");
const footerPath = path.resolve("src/components/Footer.astro");
const ecosystemPath = path.resolve("src/data/ecosystem.ts");
const atlasPath = path.resolve("src/pages/atlas.astro");
const lumePath = path.resolve("src/components/LumeGuide.astro");

const [consts, header, footer, ecosystem, atlas, lume] = await Promise.all([
  fs.readFile(constsPath, "utf8"),
  fs.readFile(headerPath, "utf8"),
  fs.readFile(footerPath, "utf8"),
  fs.readFile(ecosystemPath, "utf8"),
  fs.readFile(atlasPath, "utf8"),
  fs.readFile(lumePath, "utf8"),
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


const requiredAtlasHubs = ["bancos", "sketchbooks", "composicoes-autorais"];
for (const slug of requiredAtlasHubs) {
  const hubLine = ecosystem.split("\\n").find((line) => line.includes('id:"' + slug + '"'));
  if (!hubLine || !hubLine.includes('href:"' + slug + '/"')) failures.push("ecosystem hub missing or misrouted: " + slug);
  if (!atlas.includes('"' + slug + '/"')) failures.push("Atlas door missing or misrouted: " + slug);
}
if (!lume.includes("banks:{href:base+'bancos/'")) failures.push("Lume must route image-bank queries to the bank catalog");
if (!lume.includes("bndigital:{href:base+'bancos/bndigital/'")) failures.push("Lume must route BNDigital queries to its detail page");

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


const STUDIO_BUNDLE_FILES = 637;
const STUDIO_IMAGE_FILES = 613;
const STUDIO_ROUTE_FILES = [
  "index.html", "agendar/index.html", "biblioteca/index.html", "contato/index.html",
  "cuidados/index.html", "faq/index.html", "harum-noir/index.html", "localizacao/index.html",
  "portfolio/index.html", "privacidade/index.html", "servicos/index.html", "sobre/index.html",
];
const GPT_HOST = "tattoostudio23.suryamaya-harum.chatgpt.site";

async function inspectStudioBundle(root) {
  const files = [];
  async function walkBundle(dir) {
    for (const entry of await fs.readdir(dir, { withFileTypes: true })) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) await walkBundle(full);
      else if (entry.isFile()) files.push(path.relative(root, full).split(path.sep).join("/"));
    }
  }
  try {
    await fs.access(root);
    await walkBundle(root);
  } catch {
    return { exists: false, files: [], missingRoutes: STUDIO_ROUTE_FILES, imageFiles: 0, staleHostFiles: [] };
  }
  const fileSet = new Set(files);
  const missingRoutes = STUDIO_ROUTE_FILES.filter((route) => !fileSet.has(route));
  const imageFiles = files.filter((file) => /\.(?:avif|gif|jpe?g|png|svg|webp)$/i.test(file));
  const staleHostFiles = [];
  for (const file of files.filter((value) => /\.(?:html|css|js|json|xml|txt|webmanifest)$/i.test(value))) {
    const text = await fs.readFile(path.join(root, file), "utf8");
    if (text.includes(GPT_HOST)) staleHostFiles.push(file);
  }
  return { exists: true, files, missingRoutes, imageFiles: imageFiles.length, staleHostFiles };
}

const sourceBundle = await inspectStudioBundle(path.resolve("public/studio23"));
const builtBundle = await inspectStudioBundle(path.resolve("dist/studio23"));
for (const [label, bundle] of [["public/studio23", sourceBundle], ["dist/studio23", builtBundle]]) {
  if (!bundle.exists) failures.push(`${label} is missing`);
  if (bundle.files.length !== STUDIO_BUNDLE_FILES) failures.push(`${label} must contain ${STUDIO_BUNDLE_FILES} files, found ${bundle.files.length}`);
  if (bundle.imageFiles !== STUDIO_IMAGE_FILES) failures.push(`${label} must contain ${STUDIO_IMAGE_FILES} images, found ${bundle.imageFiles}`);
  if (bundle.missingRoutes.length) failures.push(`${label} is missing routes: ${bundle.missingRoutes.join(", ")}`);
  if (bundle.staleHostFiles.length) failures.push(`${label} still references the GPT host in: ${bundle.staleHostFiles.join(", ")}`);
}

const summary = {
  studioSite: EXPECTED.STUDIO_SITE,
  studioNoir: EXPECTED.STUDIO_NOIR,
  headerBridge: header.includes("href={STUDIO_SITE}"),
  footerSiteBridge: footer.includes("href={STUDIO_SITE}"),
  footerNoirBridge: footer.includes("href={STUDIO_NOIR}"),
  duplicatedCanonicalUrlFiles: directUrlFiles,
  requiredAtlasHubs,
  studioBundleFiles: sourceBundle.files.length,
  studioImageFiles: sourceBundle.imageFiles,
  studioBundleRoutes: STUDIO_ROUTE_FILES.length,
  failures,
};

await fs.writeFile("ecosystem-contract-health.json", JSON.stringify(summary, null, 2));

if (failures.length) {
  for (const failure of failures) console.error("ECOSYSTEM CONTRACT:", failure);
  process.exit(1);
}

console.log("Ecosystem contract passed: Studio bridges and native Atlas routes are intact.");
