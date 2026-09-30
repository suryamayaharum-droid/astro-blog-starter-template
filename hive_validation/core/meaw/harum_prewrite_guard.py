from __future__ import annotations

import datetime
from typing import Any, Iterable

FINAL={"succeeded","superseded","stable","stable-private"}


def _norm(scope:str)->str:
    return str(scope or "").strip().rstrip("/")


def _overlap(left:str,right:str)->bool:
    a=_norm(left);b=_norm(right)
    if not a or not b:
        return False
    return a==b or a.startswith(b+"/") or b.startswith(a+"/")


def _walk(node:dict[str,Any]):
    yield node
    for child in node.get("children",[]) or []:
        yield from _walk(child)


def _jev_index(jev:dict[str,Any])->dict[str,dict[str,Any]]:
    return {
        str(row.get("work_id")):row
        for row in (jev.get("open_work",[]) or [])
        if row.get("work_id")
    }


def evaluate_prewrite(
    *,
    actor_id:str,
    requested_scopes:Iterable[str],
    tree:dict[str,Any],
    jev:dict[str,Any],
    leases:dict[str,Any]|None=None,
    now:float|None=None,
)->dict[str,Any]:
    """Check whether an actor may mutate requested HARUM write scopes.

    This is a coordination guard, not external authorization. It prevents an
    instance from writing through a connector into files currently owned by
    another claimed work item.
    """
    actor=str(actor_id or "").strip()
    if not actor:
        raise ValueError("actor_id required")
    requested=sorted({_norm(x) for x in requested_scopes if _norm(x)})
    if not requested:
        raise ValueError("at least one requested scope required")

    ts=float(now if now is not None else datetime.datetime.now(datetime.timezone.utc).timestamp())
    open_work=_jev_index(jev)
    blockers=[]

    for node in _walk(tree.get("root",{})):
        scopes=[_norm(x) for x in (node.get("write_scope",[]) or []) if _norm(x)]
        if not scopes:
            continue
        work_id=str(node.get("id") or "")
        state=str(node.get("state") or "")
        work=open_work.get(work_id,{})
        status=str(work.get("status") or state)
        owner=str(work.get("owner") or node.get("owner") or "").strip()
        collaborators=set(node.get("collaborators",[]) or [])
        overlap=sorted({
            req for req in requested
            if any(_overlap(req,declared) for declared in scopes)
        })
        if not overlap or status in FINAL:
            continue
        if status=="claimed" and owner and actor!=owner and actor not in collaborators:
            blockers.append({
                "kind":"claimed-work-owner",
                "work_id":work_id,
                "owner":owner,
                "status":status,
                "declared_write_scope":scopes,
                "requested_overlap":overlap,
            })

    lease_rows=((leases or {}).get("leases",{}) or {})
    for work_id,row in lease_rows.items():
        expiry=float(row.get("expires_at",0) or 0)
        if expiry<=ts:
            continue
        owner=str(row.get("owner") or "").strip()
        scopes=[_norm(x) for x in (row.get("write_scope",[]) or []) if _norm(x)]
        overlap=sorted({
            req for req in requested
            if any(_overlap(req,declared) for declared in scopes)
        })
        if overlap and owner and actor!=owner:
            blockers.append({
                "kind":"active-lease-owner",
                "work_id":work_id,
                "owner":owner,
                "lease_id":row.get("lease_id"),
                "declared_write_scope":scopes,
                "requested_overlap":overlap,
            })

    dedup={}
    for row in blockers:
        key=(row.get("kind"),row.get("work_id"),row.get("owner"),tuple(row.get("requested_overlap",[])))
        dedup[key]=row
    blockers=list(dedup.values())

    allowed=not blockers
    return {
        "schema":"harum.prewrite-guard/v1",
        "actor_id":actor,
        "requested_scopes":requested,
        "allowed":allowed,
        "mode":"write" if allowed else "support-only",
        "blockers":blockers,
        "rule":"A connector can execute a write only after coordination ownership is clear; this guard does not grant external permission.",
    }
