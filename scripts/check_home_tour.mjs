import fs from "node:fs/promises";

const homePath = "src/pages/index.astro";
const ecosystemPath = "src/data/ecosystem.ts";
const heroPath = "public/noir/page-wallpapers/ecosystem-tour.webp";
const failures = [];

const [home, ecosystem] = await Promise.all([
  fs.readFile(homePath, "utf8"),
  fs.readFile(ecosystemPath, "utf8"),
]);

const tourHubs = ["escola", "atlas", "percursos", "cadernos", "sketchbooks", "biblioteca"];

if (!home.includes("Começar o tour")) failures.push("home needs a visible Começar o tour CTA");
if (!home.includes('href="#tour"')) failures.push("tour CTA must point to #tour");
if (!home.includes('id="tour"')) failures.push("home needs the #tour landmark");
if (!home.includes("tourHubs.map")) failures.push("tour cards must be rendered from the curated ecosystem hub list");
if (!home.includes("ecosystemHubs.filter")) failures.push("tour cards must reuse the existing ecosystemHubs catalog");
if (!home.includes("noir/page-wallpapers/ecosystem-tour.webp")) failures.push("hero must use the local ecosystem-tour background");
if (!home.includes("escola/#primeira-pratica")) failures.push("free first-practice route must remain available");

for (const slug of tourHubs) {
  const row = ecosystem.split("\n").find((line) => line.includes('id:"' + slug + '"'));
  if (!row || !row.includes('href:"' + slug + '/"')) {
    failures.push("tour hub must resolve to a confirmed ecosystem route: " + slug);
  }
}

try {
  await fs.access(heroPath);
} catch {
  failures.push("the local ecosystem-tour hero asset is missing");
}

if (failures.length) {
  for (const failure of failures) console.error("HOME TOUR CONTRACT:", failure);
  process.exit(1);
}

console.log("Home tour contract passed: CTA, six confirmed hubs, local hero, and study entry are present.");
