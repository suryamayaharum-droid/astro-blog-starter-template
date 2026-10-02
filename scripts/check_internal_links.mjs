import fs from "node:fs/promises";
import path from "node:path";

const DIST = path.resolve("dist");
const BASE = "/astro-blog-starter-template";

const htmlFiles = [];
async function walk(dir) {
  for (const entry of await fs.readdir(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) await walk(full);
    else if (entry.isFile() && entry.name.endsWith(".html")) htmlFiles.push(full);
  }
}
await walk(DIST);

const missing = [];
const baseEscapes = [];
let checked = 0;

async function exists(file) {
  try { await fs.access(file); return true; } catch { return false; }
}

function stripQueryHash(value) {
  return value.split("#", 1)[0].split("?", 1)[0];
}

function sourceWebPath(file) {
  const rel = path.relative(DIST, file).split(path.sep).join("/");
  return rel === "index.html" ? "/" : "/" + rel.replace(/\/index\.html$/, "/");
}

async function resolveTarget(raw, fromFile) {
  const trimmed = raw.trim();
  if (!trimmed || trimmed.startsWith("#") || trimmed.startsWith("?")) return { skip: true };
  if (/^(?:https?:|mailto:|tel:|data:|blob:|javascript:)/i.test(trimmed) || trimmed.startsWith("//")) return { skip: true };

  let pathname = stripQueryHash(trimmed);
  try { pathname = decodeURI(pathname); } catch {}

  const fromPath = sourceWebPath(fromFile);
  if (pathname.startsWith("/")) {
    if (pathname === BASE || pathname.startsWith(BASE + "/")) {
      pathname = pathname.slice(BASE.length) || "/";
    } else {
      baseEscapes.push({ from: fromPath, value: raw });
      pathname = pathname || "/";
    }
  } else {
    const baseDir = fromPath.endsWith("/") ? fromPath : path.posix.dirname(fromPath) + "/";
    pathname = path.posix.resolve(baseDir, pathname);
  }

  pathname = pathname.replace(/^\/+/, "");
  const candidates = [];

  if (!pathname) candidates.push(path.join(DIST, "index.html"));
  else if (path.posix.extname(pathname)) candidates.push(path.join(DIST, pathname));
  else {
    candidates.push(path.join(DIST, pathname, "index.html"));
    candidates.push(path.join(DIST, pathname + ".html"));
  }

  for (const candidate of candidates) {
    if (await exists(candidate)) return { ok: true };
  }
  return { ok: false, from: fromPath, value: raw, candidates: candidates.map(c => path.relative(DIST, c)) };
}

const attributePattern = /\b(?:href|src)\s*=\s*["']([^"'<>]+)["']/gi;

for (const file of htmlFiles) {
  const html = await fs.readFile(file, "utf8");
  for (const match of html.matchAll(attributePattern)) {
    checked += 1;
    const result = await resolveTarget(match[1], file);
    if (!result.skip && result.ok === false) missing.push(result);
  }
}

const summary = {
  checkedAt: new Date().toISOString(),
  htmlFiles: htmlFiles.length,
  localAttributesChecked: checked,
  missingCount: missing.length,
  baseEscapeCount: baseEscapes.length,
  missing,
  baseEscapes
};

await fs.writeFile("internal-link-health.json", JSON.stringify(summary, null, 2));

console.log(
  `Internal link health: ${summary.htmlFiles} HTML files | ${summary.localAttributesChecked} href/src checked | ${summary.missingCount} missing | ${summary.baseEscapeCount} base escapes`
);

for (const item of missing) console.error("MISSING", item.from, "->", item.value);
for (const item of baseEscapes) console.warn("BASE_ESCAPE", item.from, "->", item.value);

if (missing.length > 0) process.exitCode = 1;
