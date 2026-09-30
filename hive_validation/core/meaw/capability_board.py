from __future__ import annotations

import datetime
from typing import Any, Iterable

from .capability_federation import build_instance_passport, score_passport


def _passports_from_state(state:dict[str,Any])->list[dict[str,Any]]:
    rows=[]
    for actor,row in (state.get("instances",{}) or {}).items():
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


def _merge_passports(*groups:Iterable[dict[str,Any]])->list[dict[str,Any]]:
    merged={}
    for group in groups:
        for row in group or []:
            actor=str(row.get("actor_id") or "").strip()
            if actor:
                merged[actor]=row
    return [merged[k] for k in sorted(merged)]


def build_capability_board(
    *,
    assembly_state:dict[str,Any],
    dispatch:dict[str,Any],
    registry:dict[str,Any],
    persisted_passports:Iterable[dict[str,Any]]|None=None,
    now:datetime.datetime|None=None,
)->dict[str,Any]:
    current=now or datetime.datetime.now(datetime.timezone.utc)
    passports=_merge_passports(_passports_from_state(assembly_state),persisted_passports or [])

    instance_rows=[]
    connector_index:dict[str,dict[str,Any]]={}
    skill_index:dict[str,set[str]]={}
    role_index:dict[str,set[str]]={}
    fresh_actor_ids=set()

    for passport in passports:
        score=score_passport(passport,now=current)
        actor=str(passport.get("actor_id"))
        if score.get("fresh") and score.get("dispatchable"):
            fresh_actor_ids.add(actor)
        connectors=[]
        for connector in passport.get("connectors",[]) or []:
            cid=str(connector.get("id"))
            status=str(connector.get("status") or "declared")
            connectors.append({"id":cid,"provider":connector.get("provider"),"status":status})
            idx=connector_index.setdefault(cid,{"id":cid,"verified":[],"declared":[],"degraded":[],"unavailable":[]})
            idx.setdefault(status,[]).append(actor)
        skill_ids=[]
        for skill in passport.get("skills",[]) or []:
            sid=str(skill.get("id"))
            if not sid:
                continue
            skill_ids.append(sid)
            skill_index.setdefault(sid,set()).add(actor)
        roles=passport.get("roles",[]) or []
        for role in roles:
            role_index.setdefault(str(role),set()).add(actor)
        instance_rows.append({
            "actor_id":actor,
            "roles":roles,
            "reachability":passport.get("reachability"),
            "dispatch_modes":passport.get("dispatch_modes",[]),
            "fresh":bool(score.get("fresh")),
            "dispatchable":bool(score.get("dispatchable")),
            "expires_at":passport.get("expires_at"),
            "connectors":connectors,
            "skill_count":len(skill_ids),
            "surfaces":passport.get("surfaces",[]) or [],
            "capability_count":len(passport.get("capabilities",[]) or []),
        })

    work=[]
    gaps=[]
    for item in dispatch.get("assignments",[]) or []:
        state=item.get("state")
        if state not in {"available","unroutable","waiting-capacity"}:
            continue
        candidates=item.get("candidate_instances",[]) or []
        required={
            "roles":item.get("candidate_roles",[]) or ([item.get("target_role")] if item.get("target_role") else []),
            "capabilities":item.get("required_capabilities",[]) or [],
            "connectors":item.get("required_connectors",[]) or [],
            "skills":item.get("required_skills",[]) or [],
            "surfaces":item.get("required_surfaces",[]) or [],
            "verified_connectors":bool(item.get("require_verified_connectors",False)),
        }
        row={
            "work_id":item.get("work_id"),
            "state":state,
            "priority":item.get("priority"),
            "candidate_instances":candidates,
            "requirements":required,
            "reason":item.get("reason"),
        }
        work.append(row)
        if not candidates:
            gap_reason="no-announced-reachable-instance" if not fresh_actor_ids else "no-eligible-instance"
            gaps.append({"work_id":item.get("work_id"),"reason":gap_reason,"requirements":required})

    known_roles={str(r.get("role")) for r in registry.get("roles",[]) if r.get("role")}
    open_roles={
        role for row in work for role in row["requirements"]["roles"] if role
    }
    role_gaps=[
        role for role in sorted(open_roles)
        if not any(actor in fresh_actor_ids for actor in role_index.get(role,set()))
    ]

    connectors=[]
    for cid in sorted(connector_index):
        row=connector_index[cid]
        connectors.append({
            "id":cid,
            "verified":sorted(set(row.get("verified",[]))),
            "declared":sorted(set(row.get("declared",[]))),
            "degraded":sorted(set(row.get("degraded",[]))),
            "unavailable":sorted(set(row.get("unavailable",[]))),
        })

    return {
        "schema":"harum.capability-board/v1",
        "generated_at":current.isoformat(),
        "summary":{
            "instances_total":len(instance_rows),
            "instances_fresh_dispatchable":len(fresh_actor_ids),
            "connectors_known":len(connectors),
            "skills_known":len(skill_index),
            "open_routable_work":sum(1 for row in work if row.get("candidate_instances")),
            "open_work_without_instance":sum(1 for row in work if not row.get("candidate_instances")),
            "role_gaps":role_gaps,
        },
        "instances":sorted(instance_rows,key=lambda r:(not r["dispatchable"],r["actor_id"])),
        "connectors":connectors,
        "skills":{
            "count":len(skill_index),
            "actors_by_skill":{k:sorted(v) for k,v in sorted(skill_index.items())},
        },
        "work":work,
        "gaps":gaps,
        "rules":{
            "metadata_only":True,
            "credentials_forbidden":True,
            "verified_is_stronger_than_declared":True,
            "expired_or_offline_not_routable":True,
            "claim_and_lease_still_required":True,
        },
    }
