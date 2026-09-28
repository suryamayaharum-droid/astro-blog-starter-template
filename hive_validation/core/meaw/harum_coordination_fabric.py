from __future__ import annotations
import hashlib, json, time, uuid
from dataclasses import dataclass
from typing import Any

def canonical(value: Any) -> str:
    return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"))

def stable_id(*parts: Any) -> str:
    return hashlib.sha256(canonical(parts).encode("utf-8")).hexdigest()

@dataclass(frozen=True)
class WorkLease:
    work_id: str
    owner: str
    lease_id: str
    acquired_at: float
    expires_at: float

    def active(self, now: float | None = None) -> bool:
        return self.expires_at > (time.time() if now is None else now)

class CoordinationFabric:
    def __init__(self, state: dict[str, Any], *, default_ttl_seconds: int = 900):
        self.state=state
        self.default_ttl_seconds=max(30,int(default_ttl_seconds))
        self.state.setdefault("leases",{})
        self.state.setdefault("lease_epochs",{})

    def reclaim_expired(self, *, now: float | None = None) -> list[str]:
        ts=time.time() if now is None else float(now)
        reclaimed=[]
        for work_id,row in list(self.state["leases"].items()):
            helpers=row.setdefault("helpers",{})
            for helper_id,helper in list(helpers.items()):
                if float(helper.get("expires_at",0) or 0)<=ts:
                    del helpers[helper_id]
            if float(row.get("expires_at",0) or 0)<=ts:
                reclaimed.append(work_id)
                del self.state["leases"][work_id]
        return sorted(reclaimed)

    def claim(
        self, work_id: str, owner: str, *,
        role: str|None=None,
        write_scope: list[str]|None=None,
        max_helpers: int=0,
        ttl_seconds: int | None = None,
        now: float | None = None,
    ) -> dict[str, Any]:
        if not work_id or not owner:
            raise ValueError("work_id and owner required")
        ts=time.time() if now is None else float(now)
        self.reclaim_expired(now=ts)
        current=self.state["leases"].get(work_id)
        if current:
            return {"ok":False,"reason":"already-leased","current":current}
        ttl=max(30,int(ttl_seconds or self.default_ttl_seconds))
        epoch=int(self.state["lease_epochs"].get(work_id,0) or 0)+1
        self.state["lease_epochs"][work_id]=epoch
        lease={
            "work_id":work_id,"owner":owner,"role":role,
            "lease_id":uuid.uuid4().hex,"fencing_token":epoch,
            "acquired_at":ts,"expires_at":ts+ttl,
            "write_scope":sorted(set(write_scope or [])),
            "max_helpers":max(0,int(max_helpers or 0)),
            "helpers":{},
        }
        self.state["leases"][work_id]=lease
        return {"ok":True,"lease":lease}

    def heartbeat(self, work_id: str, owner: str, lease_id: str, *, fencing_token: int|None=None, ttl_seconds: int | None = None, now: float | None = None) -> dict[str, Any]:
        ts=time.time() if now is None else float(now)
        row=self.state["leases"].get(work_id)
        if not row or row.get("owner")!=owner or row.get("lease_id")!=lease_id:
            return {"ok":False,"reason":"invalid-lease"}
        if fencing_token is not None and int(row.get("fencing_token",0) or 0)!=int(fencing_token):
            return {"ok":False,"reason":"stale-fencing-token","current_fencing_token":row.get("fencing_token")}
        ttl=max(30,int(ttl_seconds or self.default_ttl_seconds))
        row["expires_at"]=ts+ttl
        return {"ok":True,"lease":row}

    def join_helper(
        self, work_id: str, helper: str, *,
        role: str|None=None,
        ttl_seconds: int|None=None,
        now: float|None=None,
    ) -> dict[str,Any]:
        if not helper:
            raise ValueError("helper required")
        ts=time.time() if now is None else float(now)
        self.reclaim_expired(now=ts)
        row=self.state["leases"].get(work_id)
        if not row:
            return {"ok":False,"reason":"work-not-leased"}
        if helper==row.get("owner"):
            return {"ok":False,"reason":"owner-is-not-helper"}
        helpers=row.setdefault("helpers",{})
        if helper in helpers and float(helpers[helper].get("expires_at",0) or 0)>ts:
            return {"ok":False,"reason":"helper-already-joined","current":helpers[helper]}
        max_helpers=max(0,int(row.get("max_helpers",0) or 0))
        if max_helpers<=0:
            return {"ok":False,"reason":"helpers-disabled"}
        if len(helpers)>=max_helpers:
            return {"ok":False,"reason":"helper-capacity"}
        ttl=max(30,int(ttl_seconds or self.default_ttl_seconds))
        helper_lease={
            "helper":helper,"role":role,"helper_lease_id":uuid.uuid4().hex,
            "acquired_at":ts,"expires_at":min(ts+ttl,float(row.get("expires_at",ts+ttl))),
        }
        helpers[helper]=helper_lease
        return {"ok":True,"helper_lease":helper_lease}

    def heartbeat_helper(
        self, work_id: str, helper: str, helper_lease_id: str, *,
        ttl_seconds: int|None=None, now: float|None=None,
    ) -> dict[str,Any]:
        ts=time.time() if now is None else float(now)
        row=self.state["leases"].get(work_id)
        helper_row=(row or {}).get("helpers",{}).get(helper)
        if not row or not helper_row or helper_row.get("helper_lease_id")!=helper_lease_id:
            return {"ok":False,"reason":"invalid-helper-lease"}
        ttl=max(30,int(ttl_seconds or self.default_ttl_seconds))
        helper_row["expires_at"]=min(ts+ttl,float(row.get("expires_at",ts+ttl)))
        return {"ok":True,"helper_lease":helper_row}

    def leave_helper(self, work_id: str, helper: str, helper_lease_id: str) -> bool:
        row=self.state["leases"].get(work_id)
        helpers=(row or {}).get("helpers",{})
        helper_row=helpers.get(helper)
        if not helper_row or helper_row.get("helper_lease_id")!=helper_lease_id:
            return False
        del helpers[helper]
        return True

    def release(self, work_id: str, owner: str, lease_id: str, *, fencing_token: int|None=None) -> bool:
        row=self.state["leases"].get(work_id)
        if not row or row.get("owner")!=owner or row.get("lease_id")!=lease_id:
            return False
        if fencing_token is not None and int(row.get("fencing_token",0) or 0)!=int(fencing_token):
            return False
        del self.state["leases"][work_id]
        return True

    def route(self, required: set[str], registry: dict[str, Any], *, busy_roles: set[str] | None = None) -> list[str]:
        busy=busy_roles or set()
        candidates=[]
        for row in registry.get("roles",[]):
            role=row.get("role")
            caps=set(row.get("capabilities",[]))
            if role and role not in busy and required <= caps:
                candidates.append((len(caps-required),role))
        return [role for _,role in sorted(candidates)]
