import type { HarumCapability, HarumStatus, HarumTask } from './harum-intelligence-core';

/** Compact deterministic mirror of project state.
 * It is a projection/index, never the source of truth.
 */
export interface ProjectVector {
  version: 1;
  taskCount: number;
  status: number[];
  capability: number[];
  priority: number[];
  dependencyDensity: number;
  fileConflictDensity: number;
  evidenceCoverage: number;
  readiness: number;
  blocked: number;
  completion: number;
  signature: string;
}

const statuses: HarumStatus[] = [
  'BACKLOG','READY','CLAIMED','DOING','VERIFY','VERIFIED','INTEGRATE','DONE',
  'BLOCKED_PERMISSION','BLOCKED_DEPENDENCY','BLOCKED_EVIDENCE','FAILED',
];
const capabilities: HarumCapability[] = [
  'research','content','ui','code','qa','seo','deploy','coordination',
];

const ratio = (n: number, d: number) => d ? Number((n / d).toFixed(4)) : 0;

function fnv1a(input: string): string {
  let h = 0x811c9dc5;
  for (let i = 0; i < input.length; i++) {
    h ^= input.charCodeAt(i);
    h = Math.imul(h, 0x01000193);
  }
  return (h >>> 0).toString(16).padStart(8, '0');
}

export function vectorizeProject(tasks: HarumTask[]): ProjectVector {
  const n = tasks.length;
  const status = statuses.map(s => ratio(tasks.filter(t => t.status === s).length, n));
  const capability = capabilities.map(c => ratio(tasks.filter(t => t.capability === c).length, n));
  const priority = [0,1,2,3].map(p => ratio(tasks.filter(t => t.priority === p).length, n));
  const deps = tasks.reduce((sum,t) => sum + (t.dependsOn?.length ?? 0), 0);
  const fileRefs = tasks.flatMap(t => t.files ?? []);
  const uniqueFiles = new Set(fileRefs).size;
  const evidenced = tasks.filter(t => (t.evidence?.length ?? 0) > 0).length;
  const ready = tasks.filter(t => t.status === 'READY').length;
  const blockedCount = tasks.filter(t => t.status.startsWith('BLOCKED_') || t.status === 'FAILED').length;
  const done = tasks.filter(t => t.status === 'DONE').length;

  const canonical = tasks
    .map(t => [t.id,t.status,t.priority,t.capability,(t.dependsOn ?? []).sort(),(t.files ?? []).sort(),(t.evidence ?? []).sort()])
    .sort((a,b) => String(a[0]).localeCompare(String(b[0])));

  return {
    version: 1,
    taskCount: n,
    status,
    capability,
    priority,
    dependencyDensity: ratio(deps, Math.max(n,1)),
    fileConflictDensity: ratio(Math.max(fileRefs.length - uniqueFiles, 0), Math.max(fileRefs.length,1)),
    evidenceCoverage: ratio(evidenced,n),
    readiness: ratio(ready,n),
    blocked: ratio(blockedCount,n),
    completion: ratio(done,n),
    signature: fnv1a(JSON.stringify(canonical)),
  };
}

export function projectHealth(v: ProjectVector): number {
  // 0..1 operational score; weights are explicit and versionable.
  return Number(Math.max(0, Math.min(1,
    0.30 * v.evidenceCoverage +
    0.25 * v.completion +
    0.20 * v.readiness +
    0.15 * (1 - v.blocked) +
    0.10 * (1 - v.fileConflictDensity)
  )).toFixed(4));
}

export const VECTOR_SCHEMA = {
  status: statuses,
  capability: capabilities,
  priority: ['P0','P1','P2','P3'],
} as const;
