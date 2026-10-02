import fs from "node:fs/promises";
import path from "node:path";

const EXPECTED = {
  STUDIO_SITE: "https://tattoostudio23.suryamaya-harum.chatgpt.site/",
  STUDIO_NOIR: "https://tattoostudio23.suryamaya-harum.chatgpt.site/harum-noir/",
};

const constsPath = path.resolve("src/consts.ts");
const headerPath = path.resolve("src/components/Header.astro");
const footerPath = path.resolve("src/components/Footer.astro");

const [consts, header, footer] = await Promise.all([
  fs.readFile(constsPath, "utf8"),
  fs.readFile(headerPath, "utf8"),
  fs.readFile(footerPath, "utf8"),
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
  failures,
};

await fs.writeFile("ecosystem-contract-health.json", JSON.stringify(summary, null, 2));

if (failures.length) {
  for (const failure of failures) console.error("ECOSYSTEM CONTRACT:", failure);
  process.exit(1);
}

console.log("Ecosystem contract passed: Harum Noir ↔ Studio 23 canonical bridges are centralized and intact.");
