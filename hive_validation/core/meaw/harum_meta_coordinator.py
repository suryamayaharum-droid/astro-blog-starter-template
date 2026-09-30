from __future__ import annotations
import argparse, datetime, json
from pathlib import Path
from typing import Any

def _load(path:str|Path)->dict[str,Any]:
    p=Path(path)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}

def _walk(node:dict[str,Any],parent:str|None=None):
    yield node,parent
    for child in node.get("children",[]) or []:
        yield from _walk(child,node.get("id"))

def _index(tree:dict[str,Any]):
    nodes={};parents={}
    for node,parent in _walk(tree.get("root",{})):
        if node.get("id"):
            nodes[node["id"]]=node;parents[node["id"]]=parent
    return nodes,parents

def _top_branch(work_id:str,nodes:dict[str,Any],parents:dict[str,str|None])->str|None:
    cur=work_id;last=None
    while cur and cur in nodes:
        parent=parents.get(cur)
        if parent=="HARUM": return cur
        last=cur;cur=parent
    return last if last in nodes else None

def _parse_time(value:Any)->float|None:
    if not value:return None
    try:return datetime.datetime.fromisoformat(str(value).replace("Z","+00:00")).timestamp()
    except (TypeError,ValueError):return None

def _scope_overlap(left:list[str]|None,right:list[str]|None)->bool:
    a=[str(x).rstrip("/") for x in (left or []) if x]
    b=[str(x).rstrip("/") for x in (right or []) if x]
    return any(x==y or x.startswith(y+"/") or y.startswith(x+"/") for x in a for y in b)

def _reverse_dependencies(nodes:dict[str,Any])->dict[str,list[str]]:
    out={}
    for node_id,node in nodes.items():
        for dep in node.get("depends_on",[]) or []:
            out.setdefault(dep,[]).append(node_id)
    return out

def _descendant_unlock_count(work_id:str,reverse:dict[str,list[str]])->int:
    seen=set();stack=list(reverse.get(work_id,[]))
    while stack:
        item=stack.pop()
        if item in seen:continue
        seen.add(item);stack.extend(reverse.get(item,[]))
    return len(seen)

def build_meta_plan(*,dispatch:dict[str,Any],tree:dict[str,Any],health:dict[str,Any],jev:dict[str,Any],policy:dict[str,Any]|None=None,now:float|None=None)->dict[str,Any]:
    policy=policy or {}
    ts=float(now if now is not None else datetime.datetime.now(datetime.timezone.utc).timestamp())
    nodes,parents=_index(tree);reverse=_reverse_dependencies(nodes)
    focus=set(policy.get("focus_roots",["HARUM-NOIR"]) or [])
    support=set(policy.get("support_roots",["MEAW"]) or [])
    scoring=policy.get("scoring",{}) or {}
    focus_bonus=int(scoring.get("focus_bonus",20) or 20)
    unblock_weight=int(scoring.get("dependency_unblock_weight",8) or 8)
    support_penalty=int(scoring.get("support_penalty_when_healthy",30) or 30)
    stale_per_hour=float(scoring.get("stale_bonus_per_hour",1) or 1)
    max_stale=int(scoring.get("max_stale_bonus",12) or 12)
    healthy=health.get("status")=="healthy"
    assignments=dispatch.get("assignments",[]) or []
    open_work={x.get("work_id"):x for x in jev.get("open_work",[]) or [] if x.get("work_id")}
    rows=[];product_available=False

    for row in assignments:
        work_id=row.get("work_id")
        if not work_id:continue
        node=nodes.get(work_id,{})
        branch=_top_branch(work_id,nodes,parents)
        is_product=branch in focus or work_id.startswith("HN-")
        is_support=branch in support or work_id.startswith("MEAW-") or work_id.startswith("HN-COORD-")
        if row.get("state")=="available" and is_product:product_available=True
        rows.append((row,node,branch,is_product,is_support,open_work.get(work_id,{})))

    recommendations=[];stale=[]
    warn_hours=float((policy.get("stagnation",{}) or {}).get("warn_after_hours",2) or 2)
    urgent_hours=float((policy.get("stagnation",{}) or {}).get("urgent_after_hours",6) or 6)
    for row,node,branch,is_product,is_support,work in rows:
        base=int(row.get("priority",50) or 50)
        unlock=_descendant_unlock_count(row["work_id"],reverse)
        updated=_parse_time(work.get("updated_at") or node.get("updated_at"))
        age_hours=max(0.0,(ts-updated)/3600) if updated is not None else 0.0
        stale_bonus=min(int(age_hours*stale_per_hour),max_stale)
        score=base+(focus_bonus if is_product else 0)+(unlock*unblock_weight)+stale_bonus
        reasons=[f"base={base}"]
        if is_product:reasons.append(f"current-focus+{focus_bonus}")
        if unlock:reasons.append(f"unblocks={unlock}x{unblock_weight}")
        if stale_bonus:reasons.append(f"age+{stale_bonus}")
        if row.get("recovery_candidate"):reasons.append("recovery-candidate")
        if healthy and product_available and is_support and unlock==0:
            score-=support_penalty;reasons.append(f"healthy-support-{support_penalty}")
        item={
            "work_id":row["work_id"],"state":row.get("state"),"branch":branch,
            "role":(row.get("candidate_roles") or [row.get("target_role")])[0] if (row.get("candidate_roles") or row.get("target_role")) else None,
            "priority":base,"meta_score":score,"unlocks":unlock,"age_hours":round(age_hours,2),
            "is_current_focus":is_product,"is_support":is_support,"reason":" · ".join(reasons),
            "recovery_candidate":bool(row.get("recovery_candidate")),
            "dispatch_reason":row.get("reason"),
            "candidate_instances":row.get("candidate_instances",[]) or [],
            "recovery":row.get("recovery"),
            "write_scope":row.get("write_scope",[]) or [],"max_helpers":row.get("max_helpers",0),
        }
        recommendations.append(item)
        if row.get("state") in {"available","blocked","leased"} and age_hours>=warn_hours:
            stale.append({"work_id":row["work_id"],"state":row.get("state"),"age_hours":round(age_hours,2),"severity":"urgent" if age_hours>=urgent_hours else "warning","suggestion":"answer existing help / claim / handoff / supersede; do not open duplicate work"})

    available_ranked=sorted([x for x in recommendations if x["state"]=="available"],key=lambda x:(-x["meta_score"],-x["priority"],x["work_id"]))
    recovery_ranked=sorted([x for x in recommendations if x.get("recovery_candidate")],key=lambda x:(-x["meta_score"],-x["priority"],x["work_id"]))
    primary=available_ranked[0] if available_ranked else None
    primary_recovery=recovery_ranked[0] if recovery_ranked else None

    max_wave=int((policy.get("parallelism",{}) or {}).get("max_primary_wave",3) or 3)
    wave=[];roles=set();scopes=[]
    for item in available_ranked:
        if len(wave)>=max_wave:break
        role=item.get("role")
        if (policy.get("parallelism",{}) or {}).get("require_distinct_roles",True) and role and role in roles:continue
        if (policy.get("parallelism",{}) or {}).get("avoid_write_scope_overlap",True) and any(_scope_overlap(item.get("write_scope"),s) for s in scopes):continue
        wave.append({k:item[k] for k in ("work_id","role","meta_score","reason")})
        if role:roles.add(role)
        scopes.append(item.get("write_scope") or [])

    help_by_work={}
    for req in jev.get("open_help_requests",[]) or []:
        if req.get("work_id"):help_by_work.setdefault(req["work_id"],[]).append(req)
    collaboration=[]
    for item in available_ranked:
        reqs=help_by_work.get(item["work_id"],[])
        if reqs:
            collaboration.append({
                "work_id":item["work_id"],"mode":"existing-help-request",
                "target_roles":sorted({r.get("target_role") for r in reqs if r.get("target_role")}),
                "questions":[r.get("question") for r in reqs if r.get("question")][:3],
                "action":"answer/accept existing request instead of creating parallel work"
            })

    active_states={"available","leased","blocked","waiting-capacity"}
    open_product=sum(1 for x in recommendations if (x["state"] in active_states or x.get("recovery_candidate")) and x["is_current_focus"])
    open_support=sum(1 for x in recommendations if (x["state"] in active_states or x.get("recovery_candidate")) and x["is_support"])
    total=max(1,open_product+open_support);support_ratio=open_support/total
    max_ratio=float((policy.get("anti_overcoordination",{}) or {}).get("max_support_ratio_when_healthy",0.34) or 0.34)
    over=bool(healthy and product_available and support_ratio>max_ratio)
    mode="repair-first" if not healthy else ("product-first" if product_available else "maintenance")
    guard_action=("freeze-new-coordination-work-unless-it-unblocks-a-named-product-item" if healthy and product_available else ("repair-coordination-before-expanding-work" if not healthy else "maintain-smallest-useful-system"))

    return {
        "schema":"harum.meta-coordination-plan/v1",
        "source_last_event":jev.get("last_event"),
        "generated_at":datetime.datetime.fromtimestamp(ts,datetime.timezone.utc).isoformat(),
        "mode":mode,"health":health.get("status"),"primary_move":primary,
        "primary_recovery":primary_recovery,"recovery_queue":recovery_ranked[:5],
        "critical_path":available_ranked[:5],"parallel_wave":wave,
        "collaboration_suggestions":collaboration[:6],"stagnation":stale[:8],
        "coordination_budget":{"open_product":open_product,"open_support":open_support,"support_ratio":round(support_ratio,3),"max_support_ratio_when_healthy":max_ratio,"overcoordination":over,"action":guard_action},
        "rules":{"advisory_only":True,"never_auto_claim":True,"never_expand_permissions":True,"product_focus_when_healthy":True,"prefer_existing_work_and_help":True}
    }

def main():
    p=argparse.ArgumentParser(description="HARUM/JEV second-order coordination advisor")
    p.add_argument("--dispatch",default="state/coordination/dispatch_plan.json")
    p.add_argument("--tree",default="systems/harum_project_tree.json")
    p.add_argument("--health",default="state/coordination/health.json")
    p.add_argument("--jev",default=".harum-assembly/jev_view.json")
    p.add_argument("--policy",default="systems/harum_meta_coordination.json")
    p.add_argument("--out",default="state/coordination/meta_plan.json")
    a=p.parse_args()
    plan=build_meta_plan(dispatch=_load(a.dispatch),tree=_load(a.tree),health=_load(a.health),jev=_load(a.jev),policy=_load(a.policy))
    out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(plan,ensure_ascii=False))

if __name__=="__main__":main()
