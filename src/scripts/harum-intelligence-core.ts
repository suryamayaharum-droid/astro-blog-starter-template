export type HarumCapability =
  | 'research' | 'content' | 'ui' | 'code' | 'qa' | 'seo' | 'deploy' | 'coordination';

export type HarumStatus =
  | 'BACKLOG' | 'READY' | 'CLAIMED' | 'DOING' | 'VERIFY' | 'VERIFIED' | 'INTEGRATE' | 'DONE'
  | 'BLOCKED_PERMISSION' | 'BLOCKED_DEPENDENCY' | 'BLOCKED_EVIDENCE' | 'FAILED';

export interface HarumTask {
  id: string;
  objective: string;
  priority: 0 | 1 | 2 | 3;
  status: HarumStatus;
  capability: HarumCapability;
  dependsOn?: string[];
  files?: string[];
  evidence?: string[];
  acceptance?: string[];
  reversible?: boolean;
  requiresApproval?: boolean;
}

export interface HarumContext {
  completed: ReadonlySet<string>;
  availableCapabilities: ReadonlySet<HarumCapability>;
  claimedFiles?: ReadonlySet<string>;
}

const blocked: ReadonlySet<HarumStatus> = new Set([
  'BLOCKED_PERMISSION', 'BLOCKED_DEPENDENCY', 'BLOCKED_EVIDENCE', 'FAILED',
]);

export function isReady(task: HarumTask, context: HarumContext): boolean {
  if (task.status !== 'READY' || blocked.has(task.status)) return false;
  if (!context.availableCapabilities.has(task.capability)) return false;
  if (task.requiresApproval) return false;
  if ((task.dependsOn ?? []).some((id) => !context.completed.has(id))) return false;
  if ((task.files ?? []).some((file) => context.claimedFiles?.has(file))) return false;
  return true;
}

export function pullNext(tasks: HarumTask[], context: HarumContext): HarumTask | undefined {
  return tasks
    .filter((task) => isReady(task, context))
    .sort((a, b) => a.priority - b.priority || a.id.localeCompare(b.id))[0];
}

export function pullParallel(tasks: HarumTask[], context: HarumContext, limit = 4): HarumTask[] {
  const selected: HarumTask[] = [];
  const files = new Set(context.claimedFiles ?? []);
  for (const task of tasks.filter((item) => isReady(item, context)).sort((a, b) => a.priority - b.priority)) {
    if (selected.length >= limit) break;
    const taskFiles = task.files ?? [];
    if (taskFiles.some((file) => files.has(file))) continue;
    selected.push(task);
    taskFiles.forEach((file) => files.add(file));
  }
  return selected;
}

export function nextStatus(task: HarumTask, hasEvidence: boolean): HarumStatus {
  if (task.requiresApproval) return 'BLOCKED_PERMISSION';
  if (task.status === 'DOING') return hasEvidence ? 'VERIFY' : 'BLOCKED_EVIDENCE';
  if (task.status === 'VERIFY') return hasEvidence ? 'VERIFIED' : 'FAILED';
  if (task.status === 'VERIFIED') return 'INTEGRATE';
  return task.status;
}

/**
 * This module decides what work is safe to pull next. It deliberately does not
 * call external services, elevate permissions, modify GitHub Actions or publish.
 * Tool invocation remains with the execution environment and its native controls.
 */
