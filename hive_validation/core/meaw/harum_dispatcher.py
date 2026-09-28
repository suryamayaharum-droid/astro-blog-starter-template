from __future__ import annotations
import argparse
import datetime
import json
from pathlib import Path
from typing import Any

from .harum_coordination_fabric import CoordinationFabric
from .capability_federation import build_instance_passport, route_task_to_instances
from .harum_work_intent import canonical_duplicate_map

FINAL={"succeeded","superseded","stable","stable-private"}

def _load(path: str|Path) -> dict[str,Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))

def _walk(node: dict[str,Any]):
    yield node
    for child in node.get("children",[]) or []:
        yield from _walk(child)

def _index(root: dict[str,Any]):
    nodes={}
    parents={}
    def visit(node: dict[str,Any], parent: str|None=None):
        node_id=node.get("id")
        if node_id:
            nodes[node_id]=node
            parents[node_id]=parent
            for child in node.get("children",[]) or []:
                visit(child,node_id)
    visit(root)
    return nodes,parents

def _scope_overlap(left: list[str]|None, right: list[str]|None) -> bool:
    a=[str(x).rstrip("/") for x in (left or []) if x]
    b=[str(x).rstrip("/") for x in (right or []) if x]
    for x in a:
        for y in b:
            if x==y or x.startswith(y+"/") or y.startswith(x+"/"):
                return True
    return False

def _active_leases(rows: dict[str,Any], ts: float) -> dict[str,dict[str,Any]]:
    return {
        work_id:row for work_id,row in rows.items()
        if float(row.get("expires_at",0) or 0)>ts
    }

def _role_of_lease(row: dict[str,Any], role_names: set[str]) -> str|None:
    role=row.get("role") or row.get("owner_role")
    if role:
        return role
    owner=row.get("owner")
    return owner if owner in role_names else None

def _ancestor_branch(work_id: str, parents: dict[str,str|None], policy: dict[str,Any]) -> str|None:
    branch_limits=(policy.get("capacity",{}) or {}).get("per_branch_max_active",{}) or {}
    current=work_id
    while current:
        if current in branch_limits:
            return current
        current=parents.get(current)
    return None

def _parse_time(value: str|None) -> float|None:
    if not value:
        return None
    try:
        return datetime.datetime.fromisoformat(value.replace("Z","+00:00")).timestamp()
    except (ValueError,TypeError):
        return None

def _effective_priority(node: dict[str,Any], work: dict[str,Any], reverse_dependencies: dict[str,list[str]], policy: dict[str,Any], ts: float):
    cfg=policy.get("priority",{}) or {}
    base=int(node.get("priority",50) or 50)
    unblock_count=len(reverse_dependencies.get(node.get("id"),[]))
    unblock_bonus=min(unblock_count,int(cfg.get("max_unblock_count",3) or 3))*int(cfg.get("dependency_unblock_bonus",5) or 5)
    urgent_bonus=int(cfg.get("urgent_bonus",15) or 15) if node.get("urgent") else 0
    risk=float(node.get("risk",0) or 0)
    risk_penalty=round(risk*float(cfg.get("risk_penalty_scale",20) or 20))
    updated=_parse_time(work.get("updated_at") or node.get("updated_at"))
    age_bonus=0
    if updated is not None and ts>updated:
        hours=(ts-updated)/3600
        age_bonus=min(
            int(hours*float(cfg.get("age_bonus_per_hour",0.5) or 0.5)),
            int(cfg.get("max_age_bonus",15) or 15)
        )
    score=base+unblock_bonus+urgent_bonus+age_bonus-risk_penalty
    return score,{
        "base":base,
        "dependency_unblock_bonus":unblock_bonus,
        "urgent_bonus":urgent_bonus,
        "age_bonus":age_bonus,
        "risk_penalty":risk_penalty,
    }

def _passports_from_instance_state(state: dict[str,Any]|None) -> list[dict[str,Any]]:
    rows=[]
    for actor,row in ((state or {}).get("instances",{}) or {}).items():
        roles=list(row.get("roles") or [])
        if row.get("role") and row.get("role") not in roles:
            roles.append(row.get("role"))
        try:
            rows.append(build_instance_passport(
                actor_id=actor,
                roles=roles,
                capabilities=row.get("capabilities") or [],
                connectors=row.get("connectors") or [],
                skills=row.get("skills") or [],
                surfaces=row.get("surfaces") or [],
                capacity=row.get("capacity") or {},
                constraints=row.get("constraints") or [],
                preferred_work_types=row.get("preferred_work_types") or [],
                reachability=str(row.get("reachability") or "manual-resume"),
                dispatch_modes=row.get("dispatch_modes") or ["jev-resume"],
                updated_at=row.get("last_seen"),
                expires_at=row.get("expires_at"),
            ))
        except ValueError:
            continue
    return rows


def build_dispatch_plan(
    *,
    jev: dict[str,Any],
    tree: dict[str,Any],
    registry: dict[str,Any],
    leases: dict[str,Any],
    policy: dict[str,Any]|None=None,
    instance_state: dict[str,Any]|None=None,
    now: float|None=None,
) -> dict[str,Any]:
    policy=policy or {}
    ts=(datetime.datetime.now(datetime.timezone.utc).timestamp() if now is None else float(now))
    nodes,parents=_index(tree.get("root",{}))
    role_names={r.get("role") for r in registry.get("roles",[]) if r.get("role")}
    lease_rows=leases.get("leases",{}) or {}
    active=_active_leases(lease_rows,ts)
    fabric=CoordinationFabric({"leases":dict(lease_rows)})

    role_load={role:0 for role in role_names}
    branch_load={}
    for work_id,row in active.items():
        role=_role_of_lease(row,role_names)
        if role:
            role_load[role]=role_load.get(role,0)+1
        branch=_ancestor_branch(work_id,parents,policy)
        if branch:
            branch_load[branch]=branch_load.get(branch,0)+1

    capacity=policy.get("capacity",{}) or {}
    global_limit=int(capacity.get("global_max_active_leases",999999) or 999999)
    default_role_limit=int(capacity.get("default_per_role_max_active",1) or 1)
    role_limits=capacity.get("per_role_max_active",{}) or {}
    branch_limits=capacity.get("per_branch_max_active",{}) or {}

    open_ids={w.get("work_id") for w in jev.get("open_work",[]) or [] if w.get("work_id") and w.get("status") not in FINAL}
    duplicate_map=canonical_duplicate_map(nodes,open_ids=open_ids)

    reverse_dependencies={}
    for node_id,node in nodes.items():
        for dep in node.get("depends_on",[]) or []:
            reverse_dependencies.setdefault(dep,[]).append(node_id)

    assignments=[]
    for work in jev.get("open_work",[]) or []:
        work_id=work.get("work_id")
        if not work_id or work.get("status") in FINAL:
            continue
        node=nodes.get(work_id,{})
        priority,breakdown=_effective_priority(node,work,reverse_dependencies,policy,ts)
        if work_id in duplicate_map:
            assignments.append({
                "work_id":work_id,
                "state":"blocked",
                "candidate_roles":[],
                "reason":"duplicate-work-intent",
                "canonical_work_id":duplicate_map[work_id],
                "priority":priority,
                "score_breakdown":breakdown,
            })
            continue
        lease=active.get(work_id)
        if lease:
            assignments.append({
                "work_id":work_id,
                "state":"leased",
                "owner":lease.get("owner"),
                "role":_role_of_lease(lease,role_names),
                "lease_id":lease.get("lease_id"),
                "helpers":sorted((lease.get("helpers") or {}).keys()),
                "candidate_roles":[],
                "reason":"active-lease",
                "priority":priority,
                "score_breakdown":breakdown,
            })
            continue

        lease_row=lease_rows.get(work_id)
        recovery_candidate=bool(
            work.get("status") in {"claimed","executing"}
            and lease_row
            and float(lease_row.get("expires_at",0) or 0)<=ts
        )

        deps=node.get("depends_on",[]) or []
        missing=[dep for dep in deps if dep not in nodes]
        pending=[dep for dep in deps if dep in nodes and nodes[dep].get("state") not in FINAL]
        if missing:
            assignments.append({
                "work_id":work_id,"state":"blocked","candidate_roles":[],
                "reason":"missing-dependency","missing_dependencies":sorted(missing),
                "priority":priority,"score_breakdown":breakdown,
            })
            continue
        if pending:
            assignments.append({
                "work_id":work_id,"state":"blocked","candidate_roles":[],
                "reason":"dependency-not-satisfied","pending_dependencies":sorted(pending),
                "priority":priority,"score_breakdown":breakdown,
            })
            continue

        write_scope=node.get("write_scope",[]) or []
        collision=None
        if write_scope:
            for other_id,row in active.items():
                if _scope_overlap(write_scope,row.get("write_scope",[]) or []):
                    collision={
                        "work_id":other_id,
                        "owner":row.get("owner"),
                        "write_scope":row.get("write_scope",[]) or [],
                    }
                    break
        if collision:
            assignments.append({
                "work_id":work_id,"state":"blocked","candidate_roles":[],
                "reason":"write-scope-collision","collision":collision,
                "write_scope":write_scope,"priority":priority,"score_breakdown":breakdown,
            })
            continue

        branch=_ancestor_branch(work_id,parents,policy)
        if len(active)>=global_limit:
            assignments.append({
                "work_id":work_id,"state":"waiting-capacity","candidate_roles":[],
                "reason":"global-capacity","priority":priority,"score_breakdown":breakdown,
            })
            continue
        if branch and branch_load.get(branch,0)>=int(branch_limits.get(branch,999999) or 999999):
            assignments.append({
                "work_id":work_id,"state":"waiting-capacity","candidate_roles":[],
                "reason":"branch-capacity","branch":branch,"priority":priority,"score_breakdown":breakdown,
            })
            continue

        target=node.get("target_role") or work.get("target_role")
        required=set(node.get("required_capabilities",[]) or [])
        required_connectors=set(node.get("required_connectors",[]) or [])
        required_skills=set(node.get("required_skills",[]) or [])
        required_surfaces=set(node.get("required_surfaces",[]) or [])
        require_verified_connectors=bool(node.get("require_verified_connectors",False))
        if target and target in role_names:
            raw_candidates=[target]
            route_reason="explicit-target-role"
        elif required:
            raw_candidates=fabric.route(required,registry,busy_roles=set())
            route_reason="capability-match"
        else:
            raw_candidates=[]
            route_reason="needs-target-or-required-capabilities"

        candidates=[]
        full_roles=[]
        for role in raw_candidates:
            limit=int(role_limits.get(role,default_role_limit) or default_role_limit)
            if role_load.get(role,0)>=limit:
                full_roles.append(role)
            else:
                candidates.append(role)

        if raw_candidates and not candidates:
            assignments.append({
                "work_id":work_id,"state":"waiting-capacity","candidate_roles":[],
                "target_role":target,"required_capabilities":sorted(required),
                "reason":"role-capacity","full_roles":sorted(full_roles),
                "branch":branch,"write_scope":write_scope,
                "priority":priority,"score_breakdown":breakdown,
            })
            continue

        candidate_instances=[]
        if instance_state is not None and (required or required_connectors or required_skills or candidates):
            passports=_passports_from_instance_state(instance_state)
            routed=route_task_to_instances(
                passports,
                required_capabilities=required,
                required_connectors=required_connectors,
                required_skills=required_skills,
                required_surfaces=required_surfaces,
                required_roles=candidates or ([target] if target else []),
                require_verified_connectors=require_verified_connectors,
                now=datetime.datetime.fromtimestamp(ts,datetime.timezone.utc),
            )
            candidate_instances=[row["actor_id"] for row in routed]

        role_routable=bool(candidates)
        instance_routable=(instance_state is None or bool(candidate_instances))
        state="available" if role_routable and instance_routable else "unroutable"
        final_reason=route_reason
        if role_routable and instance_state is not None and not candidate_instances:
            final_reason="no-live-instance-with-required-connectors-skills"
        assignment={
            "work_id":work_id,
            "state":state,
            "candidate_roles":candidates,
            "candidate_instances":candidate_instances,
            "target_role":target,
            "required_capabilities":sorted(required),
            "required_connectors":sorted(required_connectors),
            "required_skills":sorted(required_skills),
            "required_surfaces":sorted(required_surfaces),
            "require_verified_connectors":require_verified_connectors,
            "priority":priority,
            "score_breakdown":breakdown,
            "reason":"expired-lease-recovery" if recovery_candidate else final_reason,
            "recovery_candidate":recovery_candidate,
            "claim_required":True,
            "branch":branch,
            "write_scope":write_scope,
            "max_helpers":int(node.get("max_helpers",(policy.get("collaboration",{}) or {}).get("default_max_helpers",2)) or 0),
        }
        if recovery_candidate:
            assignment["recovery"]={
                "previous_owner":work.get("owner") or lease_row.get("owner"),
                "previous_lease_id":lease_row.get("lease_id"),
                "previous_fencing_token":lease_row.get("fencing_token"),
            }
        assignments.append(assignment)

    order={"available":0,"leased":1,"waiting-capacity":2,"blocked":3,"unroutable":4}
    assignments.sort(key=lambda x:(order.get(x.get("state"),9),-x.get("priority",50),x["work_id"]))
    return {
        "schema":"harum.dispatch-plan/v2",
        "source_last_event":jev.get("last_event"),
        "generated_at":datetime.datetime.fromtimestamp(ts,datetime.timezone.utc).isoformat(),
        "assignments":assignments,
        "summary":{
            "available":sum(1 for x in assignments if x["state"]=="available"),
            "leased":sum(1 for x in assignments if x["state"]=="leased"),
            "waiting_capacity":sum(1 for x in assignments if x["state"]=="waiting-capacity"),
            "blocked":sum(1 for x in assignments if x["state"]=="blocked"),
            "unroutable":sum(1 for x in assignments if x["state"]=="unroutable"),
            "active_leases":len(active),
            "global_capacity":global_limit,
        },
        "load":{"roles":role_load,"branches":branch_load},
        "rules":{
            "advisory_only":True,
            "claim_before_execution":True,
            "one_owner_per_work_item":True,
            "dependencies_before_execution":True,
            "capacity_backpressure":True,
            "write_scope_collision_prevention":True,
            "helpers_require_explicit_helper_lease":True,
            "lease_is_not_external_write_permission":True,
        },
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jev",default=".harum-assembly/jev_view.json")
    p.add_argument("--tree",default="systems/harum_project_tree.json")
    p.add_argument("--registry",default="systems/harum_capability_registry.json")
    p.add_argument("--leases",default="state/coordination/work_leases.json")
    p.add_argument("--policy",default="systems/harum_dispatch_policy.json")
    p.add_argument("--assembly-state",default=".harum-assembly/state.json")
    p.add_argument("--out",default="state/coordination/dispatch_plan.json")
    a=p.parse_args()
    plan=build_dispatch_plan(
        jev=_load(a.jev),tree=_load(a.tree),registry=_load(a.registry),
        leases=_load(a.leases),policy=_load(a.policy),
        instance_state=_load(a.assembly_state) if Path(a.assembly_state).exists() else None,
    )
    path=Path(a.out);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(plan,ensure_ascii=False))

if __name__=="__main__":
    main()
