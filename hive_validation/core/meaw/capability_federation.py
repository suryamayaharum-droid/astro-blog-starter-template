from __future__ import annotations

import datetime
from typing import Any, Iterable


_ALLOWED_STATUS={"declared","verified","degraded","unavailable"}


def _uniq(values: Iterable[str] | None) -> list[str]:
    return sorted({str(v).strip() for v in (values or []) if str(v).strip()})


def _connector(row: dict[str,Any]) -> dict[str,Any]:
    status=str(row.get("status") or "declared")
    if status not in _ALLOWED_STATUS:
        raise ValueError(f"invalid connector status: {status}")
    return {
        "id":str(row.get("id") or "").strip(),
        "provider":str(row.get("provider") or row.get("id") or "").strip(),
        "status":status,
        "capabilities":_uniq(row.get("capabilities")),
        "requires_user_auth":bool(row.get("requires_user_auth",True)),
        "evidence":_uniq(row.get("evidence")),
    }


def _skill(row: dict[str,Any]) -> dict[str,Any]:
    return {
        "id":str(row.get("id") or "").strip(),
        "category":(str(row.get("category")).strip() if row.get("category") is not None else None),
        "capabilities":_uniq(row.get("capabilities")),
    }


def build_instance_passport(
    *,
    actor_id:str,
    roles:Iterable[str]|None=None,
    capabilities:Iterable[str]|None=None,
    connectors:Iterable[dict[str,Any]]|None=None,
    skills:Iterable[dict[str,Any]]|None=None,
    surfaces:Iterable[str]|None=None,
    capacity:dict[str,Any]|None=None,
    constraints:Iterable[str]|None=None,
    preferred_work_types:Iterable[str]|None=None,
    reachability:str="manual-resume",
    dispatch_modes:Iterable[str]|None=None,
    updated_at:str|None=None,
    expires_at:str|None=None,
)->dict[str,Any]:
    """Build a non-secret description of what one runtime can do.

    A passport is routing metadata only. It never transports OAuth sessions,
    API keys, cookies, passwords, leases, or external-write authority.
    """
    actor_id=actor_id.strip()
    if reachability not in {"active","endpoint","manual-resume","offline"}:
        raise ValueError("invalid reachability")
    if not actor_id:
        raise ValueError("actor_id required")
    connector_rows=[_connector(dict(x)) for x in (connectors or [])]
    if any(not x["id"] or not x["provider"] for x in connector_rows):
        raise ValueError("connector id/provider required")
    skill_rows=[_skill(dict(x)) for x in (skills or [])]
    if any(not x["id"] for x in skill_rows):
        raise ValueError("skill id required")
    return {
        "schema":"harum.instance-capability-passport/v1",
        "actor_id":actor_id,
        "updated_at":updated_at or datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "expires_at":expires_at,
        "roles":_uniq(roles),
        "capabilities":_uniq(capabilities),
        "connectors":sorted(connector_rows,key=lambda x:(x["provider"],x["id"])),
        "skills":sorted(skill_rows,key=lambda x:x["id"]),
        "surfaces":_uniq(surfaces),
        "capacity":dict(capacity or {}),
        "constraints":_uniq(constraints),
        "preferred_work_types":_uniq(preferred_work_types),
        "reachability":reachability,
        "dispatch_modes":_uniq(dispatch_modes),
        "security":{
            "contains_credentials":False,
            "grants_permissions":False,
            "auth_boundary":"connector authorization remains local to the instance/runtime",
        },
    }


def sanitize_passport(raw:dict[str,Any])->dict[str,Any]:
    """Whitelist only non-secret passport fields from an untrusted descriptor."""
    return build_instance_passport(
        actor_id=str(raw.get("actor_id") or ""),
        roles=raw.get("roles") or [],
        capabilities=raw.get("capabilities") or [],
        connectors=raw.get("connectors") or [],
        skills=raw.get("skills") or [],
        surfaces=raw.get("surfaces") or [],
        capacity=raw.get("capacity") or {},
        constraints=raw.get("constraints") or [],
        preferred_work_types=raw.get("preferred_work_types") or [],
        reachability=str(raw.get("reachability") or "manual-resume"),
        dispatch_modes=raw.get("dispatch_modes") or [],
        updated_at=raw.get("updated_at"),
        expires_at=raw.get("expires_at"),
    )


def _fresh(passport:dict[str,Any], now:datetime.datetime|None=None)->bool:
    value=passport.get("expires_at")
    if not value:
        return True
    try:
        expiry=datetime.datetime.fromisoformat(str(value).replace("Z","+00:00"))
    except ValueError:
        return False
    current=now or datetime.datetime.now(datetime.timezone.utc)
    if expiry.tzinfo is None:
        expiry=expiry.replace(tzinfo=datetime.timezone.utc)
    return expiry>current


def _connector_map(passport:dict[str,Any])->dict[str,dict[str,Any]]:
    return {str(x.get("id")):x for x in passport.get("connectors",[]) if x.get("id")}


def score_passport(
    passport:dict[str,Any],
    *,
    required_capabilities:Iterable[str]|None=None,
    required_connectors:Iterable[str]|None=None,
    required_skills:Iterable[str]|None=None,
    required_surfaces:Iterable[str]|None=None,
    require_verified_connectors:bool=False,
    now:datetime.datetime|None=None,
)->dict[str,Any]:
    required_caps=set(_uniq(required_capabilities))
    required_conns=set(_uniq(required_connectors))
    required_skill_ids=set(_uniq(required_skills))
    required_surface_ids=set(_uniq(required_surfaces))

    connector_map=_connector_map(passport)
    usable_status={"verified"} if require_verified_connectors else {"verified","declared"}
    usable_connectors={
        cid for cid,row in connector_map.items()
        if row.get("status") in usable_status
    }
    available_skills={str(x.get("id")) for x in passport.get("skills",[]) if x.get("id")}
    capability_pool=set(passport.get("capabilities",[]))
    for row in connector_map.values():
        if row.get("status") in {"verified","declared"}:
            capability_pool.update(row.get("capabilities",[]) or [])
    for row in passport.get("skills",[]) or []:
        capability_pool.update(row.get("capabilities",[]) or [])

    missing_caps=sorted(required_caps-capability_pool)
    missing_connectors=sorted(required_conns-usable_connectors)
    available_surfaces=set(passport.get("surfaces",[]) or [])
    missing_skills=sorted(required_skill_ids-available_skills)
    missing_surfaces=sorted(required_surface_ids-available_surfaces)
    fresh=_fresh(passport,now=now)
    reachability=str(passport.get("reachability") or "manual-resume")
    dispatchable=reachability!="offline" and bool(passport.get("dispatch_modes") or [])
    eligible=fresh and dispatchable and not (missing_caps or missing_connectors or missing_skills or missing_surfaces)

    verified_required=sum(
        1 for cid in required_conns
        if connector_map.get(cid,{}).get("status")=="verified"
    )
    reachability_bonus={"endpoint":5,"active":4,"manual-resume":1,"offline":0}.get(reachability,0)
    score=(len(required_caps&capability_pool)*3)+(verified_required*4)+(len(required_skill_ids&available_skills)*2)+reachability_bonus
    return {
        "actor_id":passport.get("actor_id"),
        "eligible":eligible,
        "score":score if eligible else -1,
        "fresh":fresh,
        "dispatchable":dispatchable,
        "reachability":reachability,
        "dispatch_modes":list(passport.get("dispatch_modes") or []),
        "missing_capabilities":missing_caps,
        "missing_connectors":missing_connectors,
        "missing_skills":missing_skills,
        "missing_surfaces":missing_surfaces,
        "verified_required_connectors":verified_required,
    }


def route_task_to_instances(
    passports:Iterable[dict[str,Any]],
    *,
    required_capabilities:Iterable[str]|None=None,
    required_connectors:Iterable[str]|None=None,
    required_skills:Iterable[str]|None=None,
    required_roles:Iterable[str]|None=None,
    required_surfaces:Iterable[str]|None=None,
    require_verified_connectors:bool=False,
    now:datetime.datetime|None=None,
)->list[dict[str,Any]]:
    role_set=set(_uniq(required_roles))
    filtered=[
        p for p in passports
        if not role_set or role_set.intersection(set(p.get("roles",[]) or []))
    ]
    scored=[
        score_passport(
            p,
            required_capabilities=required_capabilities,
            required_connectors=required_connectors,
            required_skills=required_skills,
            required_surfaces=required_surfaces,
            require_verified_connectors=require_verified_connectors,
            now=now,
        )
        for p in filtered
    ]
    return sorted(
        [row for row in scored if row["eligible"]],
        key=lambda row:(-row["score"],str(row.get("actor_id") or "")),
    )


def task_requirement(
    *,
    work_id:str,
    required_capabilities:Iterable[str]|None=None,
    required_connectors:Iterable[str]|None=None,
    required_skills:Iterable[str]|None=None,
    required_surfaces:Iterable[str]|None=None,
    require_verified_connectors:bool=False,
    evidence_required:bool=True,
)->dict[str,Any]:
    if not work_id.strip():
        raise ValueError("work_id required")
    return {
        "schema":"harum.task-requirement/v1",
        "work_id":work_id.strip(),
        "required_capabilities":_uniq(required_capabilities),
        "required_connectors":_uniq(required_connectors),
        "required_skills":_uniq(required_skills),
        "required_surfaces":_uniq(required_surfaces),
        "require_verified_connectors":bool(require_verified_connectors),
        "evidence_required":bool(evidence_required),
        "execution_rule":"execute on the instance that owns the authorized connector; return only bounded result/evidence",
    }
