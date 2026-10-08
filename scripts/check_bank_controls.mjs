import fs from "node:fs/promises";
import path from "node:path";

const dist = path.resolve("dist");
const banksDir = path.join(dist, "bancos");
const ids = (await fs.readdir(banksDir, { withFileTypes: true }))
  .filter((entry) => entry.isDirectory())
  .map((entry) => entry.name)
  .sort();
const expectedFederatedLenses = { aic: 7, cma: 6, met: 6 };

if (ids.length < 13) {
  throw new Error(`Expected at least 13 generated image-bank routes, found ${ids.length}.`);
}

let checked = 0;
for (const id of ids) {
  const html = await fs.readFile(path.join(banksDir, id, "index.html"), "utf8");
  if (html.includes("abrir banco e pesquisar")) {
    throw new Error(`The obsolete generic search link remains on /bancos/${id}/.`);
  }

  if (id === "bndigital") {
    const copyButtons = [...html.matchAll(/data-copy-query=/g)].length;
    if (copyButtons !== 6) {
      throw new Error(`BNDigital should render six copy-term actions; found ${copyButtons}.`);
    }
    if (!html.includes('href="https://acervobndigital.bn.gov.br/sophia/index.asp"')) {
      throw new Error("BNDigital does not link to the official Sophia search catalog.");
    }
    if (!html.includes("Busca rápida") || !html.includes("Busca combinada")) {
      throw new Error("BNDigital search instructions are missing quick/combined catalog guidance.");
    }
  } else if (Object.hasOwn(expectedFederatedLenses, id)) {
    const targets = [...html.matchAll(/<a href="([^"]*\/museus\?q=[^"]*)"/g)].map((match) => match[1]);
    const expected = expectedFederatedLenses[id];
    if (targets.length !== expected || new Set(targets).size !== expected) {
      throw new Error(`/bancos/${id}/ should render ${expected} distinct query-filled museum links; found ${targets.length}.`);
    }
  } else if (!html.includes("pesquisar nos museus conectados")) {
    const copyButtons = [...html.matchAll(/data-copy-query=/g)].length;
    const terms = [...html.matchAll(/data-copy-query="([^"]+)"/g)].map((match) => match[1]);
    if (copyButtons !== 6 || new Set(terms).size !== 6) {
      throw new Error(`/bancos/${id}/ should render six distinct copy-term actions; found ${copyButtons}.`);
    }
  }
  checked += 1;
}

const worker = await fs.readFile(path.resolve("src/scripts/lume-ai.worker.js"), "utf8");
for (const token of ["dtype: 'q4f16'", "dtype: 'q8'", "env.useBrowserCache = true", "shader-f16", "SITE_MAP", "routeContext", "verifiedAnswer"]) {
  if (!worker.includes(token)) throw new Error(`Quantized local AI fallback contract is missing: ${token}.`);
}

const guide = await fs.readFile(path.resolve("src/components/LumeGuide.astro"), "utf8");
for (const token of ["CPU/WASM", "até 512 MB", "data-lume-ai-enable", "answerStaysOnRoute", "routeKeys", "verifiedAnswer"]){
  if (!guide.includes(token)) throw new Error(`Lume UI is missing its local-model guidance: ${token}.`);
}

const progressStart = guide.indexOf("if (message.type === 'progress')");
const progressEnd = guide.indexOf("if (message.type === 'unsupported')", progressStart);
const progressHandler = guide.slice(progressStart, progressEnd);
for (const token of [
  "message.status === 'progress_total'",
  "message.status === 'progress'",
  "aria-valuetext",
  "O valor acompanha este arquivo",
  "aiProgress.removeAttribute('value')",
  "scheduleAiLoadHint()"
]) {
  if (!progressHandler.includes(token)) {
    throw new Error(`Lume loading progress is missing phase-aware feedback: ${token}.`);
  }
}
if (!guide.includes('O carregamento continua sem novas atualizações')) {
  throw new Error("Lume loading progress is missing its stalled-load hint.");
}

console.log(`Bank/control contract: ${checked} bank routes checked; BNDigital has six distinct terms and Sophia target; federated routes keep distinct queries; local Qwen GPU/CPU cache, relevance guard and truthful phase-aware loading feedback present.`);
