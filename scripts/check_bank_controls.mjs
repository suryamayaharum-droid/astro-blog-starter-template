import fs from "node:fs/promises";
import path from "node:path";

const dist = path.resolve("dist");
const banksDir = path.join(dist, "bancos");
const ids = (await fs.readdir(banksDir, { withFileTypes: true }))
  .filter((entry) => entry.isDirectory())
  .map((entry) => entry.name)
  .sort();

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
  } else if (!html.includes("pesquisar nos museus conectados")) {
    const copyButtons = [...html.matchAll(/data-copy-query=/g)].length;
    if (copyButtons < 6) {
      throw new Error(`/bancos/${id}/ should render six copy-term actions; found ${copyButtons}.`);
    }
  }
  checked += 1;
}

const worker = await fs.readFile(path.resolve("src/scripts/lume-ai.worker.js"), "utf8");
for (const token of ["dtype: 'q4f16'", "dtype: 'q8'", "env.useBrowserCache = true", "shader-f16"]) {
  if (!worker.includes(token)) throw new Error(`Quantized local AI fallback contract is missing: ${token}.`);
}

const guide = await fs.readFile(path.resolve("src/components/LumeGuide.astro"), "utf8");
for (const token of ["CPU/WASM", "até 512 MB", "data-lume-ai-enable"]) {
  if (!guide.includes(token)) throw new Error(`Lume UI is missing its local-model guidance: ${token}.`);
}

console.log(`Bank/control contract: ${checked} generated bank routes checked; BNDigital has six themed actions and Sophia target; local Qwen GPU/CPU cache paths present.`);
