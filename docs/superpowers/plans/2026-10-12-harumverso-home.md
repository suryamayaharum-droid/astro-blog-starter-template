# HARUM NOIR ecosystem home tour — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (- [ ] ) syntax for tracking.

**Goal:** Turn the public HARUM NOIR home into a memorable, accessible starting tour for its GitHub Pages ecosystem and make image rails easy to browse on touch screens.

**Architecture:** Evolve the existing Astro home at src/pages/index.astro; derive the tour cards from the established src/data/ecosystem.ts hub catalog. Reuse the shared RailEnhancer.astro for rail controls, add it at the shared site header if the audit confirms pages currently omit it, and keep all markup/assets in the existing Astro structure.

**Tech Stack:** Astro 5, TypeScript, HTML/CSS, native horizontal scrolling, Node.js scripts, GitHub Actions and GitHub Pages.

**Spec:** docs/superpowers/specs/2026-10-12-harumverso-home-design.md

## Global Constraints

- The public editorial surface is suryamayaharum-droid/astro-blog-starter-template; the Studio 23 full source remains private in arte-harum-tattoo-site.
- Evolve the existing home; preserve its school intro, free first practice, four learning steps, and current language routes.
- Use only confirmed routes from src/data/ecosystem.ts and the verified /studio23/ subsite.
- Keep the new generated background text-free, locally hosted, credited as editorial/AI-assisted where shown, and distinct from real tattoo work.
- Preserve keyboard focus, native touch scrolling, reduced-motion behavior, and responsive scroll snap.
- Do not overlap open PR #105 sketchbook data work or the open PR #30/#29 gallery/navigation work; do not edit those same files unless the implementation requires it and a ruling is recorded.
- Do not alter hosting, repository visibility, domain, HIVE state, or credentials.

## Review Focus

- Hero text can become unreadable over a bright focal area — test the responsive overlay and ensure the image has useful negative space.
- GitHub Pages uses a base path — test the generated tour image and internal links resolve under /astro-blog-starter-template/.
- A horizontal tour rail can hide cards on phones — test swipe, next/previous controls, keyboard, and focus order.
- A link inside a rail must remain tappable — test clicking/tapping a card after scrolling.
- Reduced-motion mode must avoid animated scrolling — test the shared enhancer with prefers-reduced-motion: reduce.

---

### Task 1: Test the ecosystem tour contract and build the home entry

**Files:**
- Create: scripts/check_home_tour.mjs — focused source contract for the home and its tour hubs.
- Modify: src/pages/index.astro — home hero, tour rail, preserved learning sequence.
- Create: public/noir/page-wallpapers/ecosystem-tour.webp — original optimized hero background.

**Interfaces:**
- CTA: visible link labeled “Começar o tour” with href #tour.
- Tour hubs: escola, atlas, percursos, cadernos, sketchbooks, and biblioteca, resolved from ecosystemHubs.
- Hero asset URL is built with the existing BASE_URL convention.
- The original first-practice link remains escola/#primeira-pratica.

- [ ] **Step 1: Write scripts/check_home_tour.mjs first.** It reads src/pages/index.astro, src/data/ecosystem.ts, and the expected hero asset path; assert the CTA/href, #tour landmark, the exact six hub IDs, data-driven hub links, preserved free-practice route, and that the page credits generated editorial imagery.
- [ ] **Step 2: Run node scripts/check_home_tour.mjs** against current source and confirm it fails because the new tour and asset do not exist yet.
- [ ] **Step 3: Generate and optimize the hero background** as a wide charcoal-and-aged-gold editorial atelier scene with no text and open space for copy; save it at public/noir/page-wallpapers/ecosystem-tour.webp.
- [ ] **Step 4: Update src/pages/index.astro** to import ecosystemHubs, define the six-ID curation in the order above, add the hero CTA and a semantic section id="tour" with a horizontal .rail and informative image alt text, then retain the current study cycle and lesson cards below it.
- [ ] **Step 5: Run node scripts/check_home_tour.mjs** and confirm all assertions pass.
- [ ] **Step 6: Commit** as feat: add curated HARUM NOIR ecosystem tour.

### Task 2: Make shared image rails consistently swipeable and accessible

**Files:**
- Modify: src/components/Header.astro — ensure the shared rail enhancer runs on all pages using the site header if it is not already globally mounted.
- Modify: src/components/RailEnhancer.astro — extend selectors only for confirmed image rails, retaining current button, keyboard, resize, and reduced-motion behavior.
- Modify: src/pages/index.astro — style the tour rail for native horizontal touch scrolling and scroll snap.
- Create or modify: scripts/check_home_tour.mjs — assert rail enhancer integration and supported touch/keyboard behavior.
- Generated: Astro dist/ output, created by build.

**Interfaces:**
- Existing .rail and .browse-rail classes remain the shared horizontal-scrolling contract.
- The enhancer continues to add labeled aria-controls previous/next buttons and ArrowLeft/ArrowRight support.
- Native touch panning remains available; no pointer-capture code may suppress link activation.

- [ ] **Step 1: Extend the focused contract test** to assert that the home tour uses the shared .rail contract, the enhancer is mounted once across shared-header routes, it respects prefers-reduced-motion, and it preserves anchor links inside a rail.
- [ ] **Step 2: Run node scripts/check_home_tour.mjs** and confirm it fails for the unmounted/incomplete shared rail integration.
- [ ] **Step 3: Wire the existing RailEnhancer** through the shared Header only if the page audit shows it is not already loaded site-wide; add confirmed gallery selectors when needed and keep native browser panning.
- [ ] **Step 4: Add responsive rail CSS** with overflow-x:auto, overscroll-behavior-inline:contain, scroll-snap-type, and visible focus styles; retain the existing two-column/desktop editorial grids outside the rail.
- [ ] **Step 5: Run the focused contract and Astro build**; verify the generated root page has six working route targets and the enhancer exposes visible controls only when overflow exists.
- [ ] **Step 6: Commit** as feat: unify HARUM NOIR image rail navigation.

### Task 3: Validate, review, and publish through the existing GitHub Pages flow

**Files:**
- Modify: .github/workflows/harumverso-ci.yml only if the new focused check is not already invoked by CI.
- Verify: current check_home_tour.mjs, build/typecheck, check_ecosystem_contract.mjs, check_internal_links.mjs, and responsive/mobile audit.
- Publish: merge the reviewed branch through the existing pull-request flow and verify GitHub Pages.

**Interfaces:**
- Pull request base is main; the implementation stays isolated on codex/harumverso-home-tour-20261012.
- The public URL remains https://suryamayaharum-droid.github.io/astro-blog-starter-template/.
- Report the PR, CI results, and a live URL only after confirming the deployment.

- [ ] **Step 1: Run npm run check** and confirm Astro build and TypeScript checking pass.
- [ ] **Step 2: Run node scripts/check_home_tour.mjs, node scripts/check_ecosystem_contract.mjs, node scripts/check_internal_links.mjs, and node scripts/check_bank_controls.mjs**; confirm all pass and no existing route or subsite bundle is broken.
- [ ] **Step 3: Open a pull request** with a summary of the new home, original image, rail behavior, exact checks, and any remaining limitation; wait for all GitHub Actions checks to finish.
- [ ] **Step 4: Run the responsive/mobile audit** on the PR preview or, if the existing workflow only captures production after Pages deploy, run its equivalent matrix against a build preview and verify 320px, 360px, 390px, 412px, and desktop.
- [ ] **Step 5: Inspect the public release** after merge; verify the hero image and six hub links at the canonical root URL and verify /studio23/ still resolves.
- [ ] **Step 6: Report the verified published URL, PR, and CI outcomes**. Do not claim a live release before the Pages deploy and public page have both been confirmed.

## Self-review

- Spec coverage: the entry hero, local image, six hub destinations, preserved study experience, shared touch/keyboard rail access, motion preferences, route checks, and release verification each have an owning task.
- Step scan: every test step states the command and expected failing condition; each implementation task names its concrete source files and behavior.
- Interface consistency: home cards consume ecosystemHubs; rails continue to use .rail and the existing RailEnhancer contract.
- Review Focus: path prefixes, responsive contrast, hidden rail cards, tappable links, and reduced motion are attached to verification steps.
- Scope: the implementation stays on the public HARUM NOIR home and shared rail behavior; it does not reopen the private migration/cutover or alter existing content PRs.
