from __future__ import annotations
import argparse, datetime, json
from pathlib import Path
from typing import Any
from .harum_work_intent import detect_intent_collisions

FINAL={"succeeded","superseded","stable","stable-private"}
ACTIVE={"claimed","executing"}

def _load(path: str|Path)->dict[str,Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))

def _parse_time(value: str|None):
    if not value:return None
    try:return datetime.datetime.fromisoformat(value.replace("Z","+00:00"))
    except (ValueError,TypeError):return None

def _index(root: dict[str,Any]):
    nodes={};parents={}
    def visit(node,parent=None):
        node_id=node.get("id")
        if node_id:
            nodes[node_id]=node;parents[node_id]=parent
            for child in node.get("children",[]) or []:visit(child,node_id)
    visit(root)
    return nodes,parents

def _dependency_cycles(nodes: dict[str,Any]) -> list[list[str]]:
    color={};stack=[];cycles=[]
    def visit(node_id):
        state=color.get(node_id,0)
        if state==1:
            if node_id in stack:
                i=stack.index(node_id);cycles.append(stack[i:]+[node_id])
            return
        if state==2:return
        color[node_id]=1;stack.append(node_id)
        for dep in nodes.get(node_id,{}).get("depends_on",[]) or []:
            if dep in nodes:visit(dep)
        stack.pop();color[node_id]=2
    for node_id in nodes:visit(node_id)
    unique=[];seen=set()
    for cycle in cycles:
        key=tuple(cycle)
        if key not in seen:seen.add(key);unique.append(cycle)
    return unique

def _wait_for_cycles(open_work: dict[str,Any]) -> list[list[str]]:
    graph={}
    for work_id,row in open_work.items():
        waits=row.get("waits_for") or row.get("waiting_for") or []
        if isinstance(waits,str): waits=[waits]
        graph[work_id]=[w for w in waits if w in open_work]
    color={};stack=[];cycles=[]
    def visit(node_id):
        state=color.get(node_id,0)
        if state==1:
            if node_id in stack:
                i=stack.index(node_id);cycles.append(stack[i:]+[node_id])
            return
        if state==2:return
        color[node_id]=1;stack.append(node_id)
        for nxt in graph.get(node_id,[]):visit(nxt)
        stack.pop();color[node_id]=2
    for node_id in graph:visit(node_id)
    unique=[];seen=set()
    for cycle in cycles:
        key=tuple(cycle)
        if key not in seen:seen.add(key);unique.append(cycle)
    return unique

def _scope_overlap(left,right):
    a=[str(x).rstrip("/") for x in (left or []) if x]
    b=[str(x).rstrip("/") for x in (right or []) if x]
    return any(x==y or x.startswith(y+"/") or y.startswith(x+"/") for x in a for y in b)

def diagnose(
    *,
    panel: dict[str,Any],
    jev: dict[str,Any],
    tree: dict[str,Any],
    registry: dict[str,Any],
    leases: dict[str,Any],
    bootstrap: dict[str,Any],
    assembly_state: dict[str,Any]|None=None,
    dispatch_plan: dict[str,Any]|None=None,
    dispatch_policy: dict[str,Any]|None=None,
    now: datetime.datetime|None=None,
    instance_stale_seconds: int=3600,
)->dict[str,Any]:
    now=now or datetime.datetime.now(datetime.timezone.utc)
    issues=[];warnings=[];repairs=[]

    roles={r.get("role") for r in registry.get("roles",[]) if r.get("role")}
    nodes,parents=_index(tree.get("root",{}))
    open_work={w.get("work_id"):w for w in jev.get("open_work",[]) if w.get("work_id")}

    wait_cycles=_wait_for_cycles(open_work)
    for cycle in wait_cycles:
        issues.append({"code":"wait-for-cycle","cycle":cycle})
        repairs.append({"action":"break-wait-for-cycle-via-handoff-or-scope-split","cycle":cycle})

    collisions=detect_intent_collisions(nodes,open_ids=set(open_work))
    for row in collisions["hard"]:
        issues.append({"code":"duplicate-work-intent","intent_key":row["intent_key"],"work_ids":row["work_ids"]})
        repairs.append({"action":"merge-handoff-or-supersede-duplicate-work","intent_key":row["intent_key"],"work_ids":row["work_ids"]})
    for row in collisions["probable"]:
        warnings.append({"code":"possible-duplicate-work-intent","work_ids":row["work_ids"],"similarity":row["similarity"]})
        repairs.append({"action":"compare-intent-before-claim","work_ids":row["work_ids"]})

    cycles=_dependency_cycles(nodes)
    for cycle in cycles:
        issues.append({"code":"dependency-cycle","cycle":cycle})
        repairs.append({"action":"break-dependency-cycle","cycle":cycle})

    for node_id,node in nodes.items():
        for dep in node.get("depends_on",[]) or []:
            if dep not in nodes:
                issues.append({"code":"unknown-dependency","work_id":node_id,"dependency":dep})
                repairs.append({"action":"fix-or-remove-dependency","work_id":node_id,"dependency":dep})

    for work_id,work in open_work.items():
        node=nodes.get(work_id)
        if node is None:
            warnings.append({"code":"orphan-open-work","work_id":work_id})
            repairs.append({"action":"add-project-tree-node-or-supersede","work_id":work_id})
            continue
        if node.get("state") in FINAL:
            issues.append({"code":"closed-node-opened-as-work","work_id":work_id,"node_state":node.get("state")})
        if work.get("status")=="blocked" and not work.get("blocker"):
            issues.append({"code":"blocked-without-blocker","work_id":work_id})
        if not work.get("owner") and not node.get("target_role") and not node.get("required_capabilities"):
            warnings.append({"code":"unroutable-open-work","work_id":work_id})
            repairs.append({"action":"add-target-role-or-required-capabilities","work_id":work_id})

    for node_id,node in nodes.items():
        if node.get("state")=="open" and node_id not in open_work:
            warnings.append({"code":"tree-open-without-jev","work_id":node_id})
            repairs.append({"action":"emit-help-or-work-event-or-close-tree-node","work_id":node_id})

    for req in jev.get("open_help_requests",[]):
        role=req.get("target_role")
        if role and role not in roles:
            issues.append({"code":"unknown-help-target-role","request_id":req.get("request_id"),"target_role":role})
        created=_parse_time(req.get("created_at"))
        if created and (now-created).total_seconds()>172800:
            warnings.append({"code":"stale-help-request","request_id":req.get("request_id"),"age_hours":round((now-created).total_seconds()/3600,1)})
            repairs.append({"action":"answer-reroute-or-close-help","request_id":req.get("request_id")})

    lease_rows=leases.get("leases",{}) or {}
    active={}
    for work_id,row in lease_rows.items():
        expires=row.get("expires_at")
        if isinstance(expires,(int,float)) and expires<=now.timestamp():
            warnings.append({"code":"expired-work-lease","work_id":work_id,"owner":row.get("owner")})
            repairs.append({"action":"reclaim-expired-lease","work_id":work_id})
        else:
            active[work_id]=row
        token=row.get("fencing_token")
        if token is not None and int(token or 0)<=0:
            issues.append({"code":"invalid-fencing-token","work_id":work_id,"fencing_token":token})
            repairs.append({"action":"reclaim-lease-with-new-fencing-token","work_id":work_id})
        if work_id not in open_work:
            warnings.append({"code":"lease-without-open-work","work_id":work_id})
            repairs.append({"action":"release-or-reconcile-lease","work_id":work_id})
        for helper,helper_row in (row.get("helpers",{}) or {}).items():
            if float(helper_row.get("expires_at",0) or 0)<=now.timestamp():
                warnings.append({"code":"expired-helper-lease","work_id":work_id,"helper":helper})
                repairs.append({"action":"remove-expired-helper-lease","work_id":work_id,"helper":helper})

    active_items=list(active.items())
    for i,(left_id,left) in enumerate(active_items):
        for right_id,right in active_items[i+1:]:
            if _scope_overlap(left.get("write_scope",[]),right.get("write_scope",[])):
                issues.append({
                    "code":"active-write-scope-collision",
                    "left_work_id":left_id,"right_work_id":right_id,
                    "left_owner":left.get("owner"),"right_owner":right.get("owner"),
                })
                repairs.append({"action":"handoff-or-split-write-scope","work_ids":[left_id,right_id]})

    recovery_candidates=[]
    for work_id,work in open_work.items():
        if work.get("status") not in ACTIVE or work_id in active:
            continue
        lease_row=lease_rows.get(work_id)
        if lease_row:
            candidate={
                "work_id":work_id,
                "owner":work.get("owner") or lease_row.get("owner"),
                "lease_id":lease_row.get("lease_id"),
                "fencing_token":lease_row.get("fencing_token"),
                "reason":"expired-primary-lease",
            }
            recovery_candidates.append(candidate)
            warnings.append({
                "code":"orphaned-active-work-expired-lease",
                **candidate,
            })
            repairs.append({
                "action":"recovery-claim-with-new-fencing-token-or-owner-complete",
                "work_id":work_id,
                "previous_lease_id":lease_row.get("lease_id"),
                "previous_fencing_token":lease_row.get("fencing_token"),
            })
        else:
            warnings.append({"code":"active-work-without-lease","work_id":work_id,"owner":work.get("owner")})
            repairs.append({"action":"claim-lease-or-return-work-to-available","work_id":work_id})

    if assembly_state:
        for instance_id,row in (assembly_state.get("instances",{}) or {}).items():
            last=_parse_time(row.get("last_seen"))
            if last and (now-last).total_seconds()>instance_stale_seconds:
                warnings.append({"code":"stale-instance-heartbeat","instance":instance_id,"age_seconds":int((now-last).total_seconds())})
                repairs.append({"action":"expire-instance-and-release-owned-leases-after-verification","instance":instance_id})

    if dispatch_plan:
        if dispatch_plan.get("source_last_event") not in {None,jev.get("last_event")}:
            warnings.append({"code":"stale-dispatch-projection","projection_event":dispatch_plan.get("source_last_event"),"jev_event":jev.get("last_event")})
            repairs.append({"action":"run-projection-refresh-before-claim"})
        summary=dispatch_plan.get("summary",{}) or {}
        if int(summary.get("unroutable",0) or 0)>0:
            warnings.append({"code":"dispatcher-has-unroutable-work","count":int(summary.get("unroutable",0) or 0)})
            repairs.append({"action":"add-capability-or-target-role-to-unroutable-work"})

    if dispatch_policy:
        capacity=dispatch_policy.get("capacity",{}) or {}
        global_limit=int(capacity.get("global_max_active_leases",999999) or 999999)
        if len(active)>global_limit:
            issues.append({"code":"global-capacity-exceeded","active":len(active),"limit":global_limit})
        role_limits=capacity.get("per_role_max_active",{}) or {}
        default_limit=int(capacity.get("default_per_role_max_active",1) or 1)
        loads={}
        for row in active.values():
            role=row.get("role") or row.get("owner_role")
            if role:loads[role]=loads.get(role,0)+1
        for role,count in loads.items():
            limit=int(role_limits.get(role,default_limit) or default_limit)
            if count>limit:
                issues.append({"code":"role-capacity-exceeded","role":role,"active":count,"limit":limit})

    required=[
      "JEV.md","docs/GLOBAL_CONTINUITY_INSTRUCTION.md","START_HERE.md",
      "systems/harum_instance_panel.json",".harum-assembly/jev_view.json",
      "systems/harum_project_tree.json","systems/harum_capability_registry.json"
    ]
    order=bootstrap.get("startup_order",[])
    for item in required:
        if item not in order and item!="docs/GLOBAL_CONTINUITY_INSTRUCTION.md":
            warnings.append({"code":"bootstrap-missing-entry","entry":item})
    if bootstrap.get("global_continuity")!="docs/GLOBAL_CONTINUITY_INSTRUCTION.md":
        issues.append({"code":"bootstrap-global-continuity-missing"})

    checkpoint=jev.get("checkpoint") or {}
    public=panel.get("public_web",{})
    if not checkpoint:issues.append({"code":"missing-current-checkpoint"})
    if not public.get("github_pages") or not public.get("vercel"):
        warnings.append({"code":"public-redundancy-incomplete"})

    status="healthy" if not issues and not warnings else ("degraded" if not issues else "attention")
    return {
      "schema":"harum.coordination-health/v3",
      "source_last_event":jev.get("last_event"),
      "checked_at":now.isoformat(),
      "status":status,
      "counts":{
        "issues":len(issues),"warnings":len(warnings),"open_work":len(open_work),
        "open_help":len(jev.get("open_help_requests",[])),"active_leases":len(active),
        "known_instances":len((assembly_state or {}).get("instances",{}) or {}),
      },
      "issues":issues,"warnings":warnings,"suggested_repairs":repairs,
      "recovery_candidates":recovery_candidates,
      "next_safe_action":(
        "resolve issues before new mutation" if issues else
        "repair warnings before expanding scope" if warnings else
        "claim one bounded highest-priority dependency-ready compatible work item"
      )
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--panel",default="systems/harum_instance_panel.json")
    p.add_argument("--jev",default=".harum-assembly/jev_view.json")
    p.add_argument("--tree",default="systems/harum_project_tree.json")
    p.add_argument("--registry",default="systems/harum_capability_registry.json")
    p.add_argument("--leases",default="state/coordination/work_leases.json")
    p.add_argument("--bootstrap",default="systems/harum_bootstrap_manifest.json")
    p.add_argument("--assembly-state",default=".harum-assembly/state.json")
    p.add_argument("--dispatch-plan",default="state/coordination/dispatch_plan.json")
    p.add_argument("--dispatch-policy",default="systems/harum_dispatch_policy.json")
    p.add_argument("--out",default="state/coordination/health.json")
    a=p.parse_args()
    report=diagnose(
      panel=_load(a.panel),jev=_load(a.jev),tree=_load(a.tree),
      registry=_load(a.registry),leases=_load(a.leases),bootstrap=_load(a.bootstrap),
      assembly_state=_load(a.assembly_state),dispatch_plan=_load(a.dispatch_plan),
      dispatch_policy=_load(a.dispatch_policy)
    )
    Path(a.out).parent.mkdir(parents=True,exist_ok=True)
    Path(a.out).write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False))

if __name__=="__main__":
    main()
