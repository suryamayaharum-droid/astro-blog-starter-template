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
const brokenFragments = [];
const invalidImages = [];
const baseEscapes = [];
const idsByFile = new Map();
let checked = 0;
let fragmentsChecked = 0;

async function exists(file) {
  try { await fs.access(file); return true; } catch { return false; }
}

function sourceWebPath(file) {
  const rel = path.relative(DIST, file).split(path.sep).join("/");
  return rel === "index.html" ? "/" : "/" + rel.replace(/\/index\.html$/, "/");
}

function fragmentOf(value) {
  const index = value.indexOf("#");
  if (index < 0) return "";
  try { return decodeURIComponent(value.slice(index + 1)); } catch { return value.slice(index + 1); }
}

function idsFor(htmlFile, html) {
  if (idsByFile.has(htmlFile)) return idsByFile.get(htmlFile);
  const ids = new Set();
  const pattern = /\bid\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>]+))/gi;
  for (const match of html.matchAll(pattern)) ids.add(match[1] ?? match[2] ?? match[3]);
  idsByFile.set(htmlFile, ids);
  return ids;
}

function imageSignatureValid(file, bytes) {
  const ext = path.extname(file).toLowerCase();
  if (ext === ".webp") return bytes.length >= 12 && bytes.toString("ascii", 0, 4) === "RIFF" && bytes.toString("ascii", 8, 12) === "WEBP";
  if (ext === ".png") return bytes.length >= 8 && bytes.subarray(0, 8).equals(Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]));
  if (ext === ".jpg" || ext === ".jpeg") return bytes.length >= 3 && bytes[0] === 255 && bytes[1] === 216 && bytes[2] === 255;
  if (ext === ".gif") return bytes.length >= 6 && ["GIF87a", "GIF89a"].includes(bytes.toString("ascii", 0, 6));
  if (ext === ".avif") return bytes.length >= 12 && bytes.toString("ascii", 4, 8) === "ftyp" && /^(?:avif|avis)$/.test(bytes.toString("ascii", 8, 12));
  return true;
}

async function resolveTarget(raw, fromFile) {
  const trimmed = raw.trim();
  if (!trimmed || /^(?:https?:|mailto:|tel:|data:|blob:|javascript:)/i.test(trimmed) || trimmed.startsWith("//")) return { skip: true };

  const fragment = fragmentOf(trimmed);
  const hashIndex = trimmed.indexOf("#");
  const withoutHash = hashIndex >= 0 ? trimmed.slice(0, hashIndex) : trimmed;
  const queryIndex = withoutHash.indexOf("?");
  let pathname = queryIndex >= 0 ? withoutHash.slice(0, queryIndex) : withoutHash;
  if (!pathname && !fragment) return { skip: true };
  try { pathname = decodeURI(pathname); } catch {}

  const fromPath = sourceWebPath(fromFile);
  let candidates = [];
  if (!pathname) {
    candidates = [fromFile];
  } else {
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
    if (!pathname) candidates.push(path.join(DIST, "index.html"));
    else if (path.posix.extname(pathname)) candidates.push(path.join(DIST, pathname));
    else {
      candidates.push(path.join(DIST, pathname, "index.html"));
      candidates.push(path.join(DIST, pathname + ".html"));
    }
  }

  for (const candidate of candidates) {
    if (await exists(candidate)) {
      const checkFragment = Boolean(fragment && candidate.endsWith(".html"));
      if (checkFragment) {
        const html = await fs.readFile(candidate, "utf8");
        if (!idsFor(candidate, html).has(fragment)) {
          return { ok: true, from: fromPath, value: raw, fragment, target: sourceWebPath(candidate), fragmentMissing: true, isFragment: true };
        }
      }
      return { ok: true, file: candidate, isFragment: checkFragment };
    }
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
    if (result.ok && result.file && /\.(?:webp|png|jpe?g|gif|avif)$/i.test(result.file)) {
      const bytes = await fs.readFile(result.file);
      if (!imageSignatureValid(result.file, bytes)) {
        invalidImages.push({ from: sourceWebPath(file), value: match[1], file: path.relative(DIST, result.file), bytes: bytes.length });
      }
    }
    if (result.isFragment) fragmentsChecked += 1;
    if (result.fragmentMissing) brokenFragments.push(result);
  }
}

const summary = {
  checkedAt: new Date().toISOString(),
  htmlFiles: htmlFiles.length,
  localAttributesChecked: checked,
  fragmentReferencesChecked: fragmentsChecked,
  missingCount: missing.length,
  brokenFragmentCount: brokenFragments.length,
  invalidImageCount: invalidImages.length,
  baseEscapeCount: baseEscapes.length,
  missing,
  brokenFragments,
  invalidImages,
  baseEscapes
};
await fs.writeFile("internal-link-health.json", JSON.stringify(summary, null, 2));
console.log("Internal link health: " + summary.htmlFiles + " HTML files | " + summary.localAttributesChecked + " href/src checked | " + summary.fragmentReferencesChecked + " fragments checked | " + summary.missingCount + " missing | " + summary.brokenFragmentCount + " broken fragments | " + summary.invalidImageCount + " invalid images | " + summary.baseEscapeCount + " base escapes");
for (const item of missing) console.error("MISSING", item.from, "->", item.value);
for (const item of brokenFragments) console.error("BROKEN_FRAGMENT", item.from, "->", item.value, "target", item.target);
for (const item of invalidImages) console.error("INVALID_IMAGE", item.from, "->", item.value, "file", item.file, "bytes", item.bytes);
for (const item of baseEscapes) console.warn("BASE_ESCAPE", item.from, "->", item.value);
if (missing.length > 0 || brokenFragments.length > 0 || invalidImages.length > 0) process.exitCode = 1;
