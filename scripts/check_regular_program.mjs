import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

// The curriculum must remain reachable, complete, and usable without JavaScript.
const root = 'dist/escola/programa-regular';
assert.ok(fs.existsSync(path.join(root, 'index.html')), 'A escola precisa publicar o programa regular');
const home = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const lessons = [...home.matchAll(/data-lesson-id="([^"]+)"/g)].map(m => m[1]);
assert.equal(new Set(lessons).size, 33, 'O programa precisa oferecer 33 aulas distintas');
for (const slug of lessons) {
  const file = path.join(root, slug, 'index.html');
  assert.ok(fs.existsSync(file), `Aula ausente: ${slug}`);
  const html = fs.readFileSync(file, 'utf8');
  for (const id of ['materiais', 'passo-a-passo', 'revisao', 'referencia']) {
    assert.ok(html.includes(`id="${id}"`), `${slug}: falta ${id}`);
  }
  assert.ok(html.includes('data-program-complete'), `${slug}: sem registro de prática`);
}
const school = fs.readFileSync('dist/escola/index.html', 'utf8');
assert.ok(school.includes('escola/programa-regular/'), 'A escola precisa dar acesso direto ao programa');
assert.ok(home.includes('96 horas') && home.includes('24 semanas'), 'Carga e duração precisam estar visíveis');
assert.ok(home.includes('seleção independente'), 'A origem independente precisa estar explícita');
console.log('PASS: 33 aulas completas, entrada pela escola, sequência e origem editorial.');
