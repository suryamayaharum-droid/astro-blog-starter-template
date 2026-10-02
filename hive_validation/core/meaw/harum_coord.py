from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import json
import os
from pathlib import Path
from typing import Any, Iterable

from core.meaw.harum_coordination_fabric import CoordinationFabric
from core.meaw.harum_projection_refresh import refresh as refresh_projections
from core.meaw.jev_instance_bridge import build_view
from runtime import harum_assembly_bus as bus
from core.meaw.capability_federation import sanitize_passport
from core.meaw.remote_receipts import load_pending_receipts, evaluate_remote_result, mark_processed
from core.meaw.harum_prewrite_guard import evaluate_prewrite
from core.meaw.harum_projection_freshness import assess_projection_freshness

FINAL_STATES={"succeeded","superseded","stable","stable-private"}

def _load(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))

def _write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def _utc_iso_from_ts(value: float) -> str:
    return dt.datetime.fromtimestamp(float(value), dt.timezone.utc).isoformat()

def _uniq(values: Iterable[str] | None) -> list[str]:
    return sorted({str(v).strip() for v in (values or []) if str(v).strip()})

def _walk(node: dict[str,Any]):
    yield node
    for child in node.get("children",[]) or []:
        yield from _walk(child)

@contextlib.contextmanager
def _local_lock(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    fh=path.open("a+", encoding="utf-8")
    try:
        try:
            import fcntl
            fcntl.flock(fh.fileno(), fcntl.LOCK_EX)
        except (ImportError, OSError):
            pass
        yield
    finally:
        try:
            import fcntl
            fcntl.flock(fh.fileno(), fcntl.LOCK_UN)
        except (ImportError, OSError):
            pass
        fh.close()

class CoordinationError(RuntimeError):
    pass

class HarumCoord:
    def __init__(self, root: str | Path="."):
        self.root=Path(root).resolve()
        self.paths={
            "events":self.root/".harum-assembly/events.jsonl",
            "state":self.root/".harum-assembly/state.json",
            "jev":self.root/".harum-assembly/jev_view.json",
            "tree":self.root/"systems/harum_project_tree.json",
            "registry":self.root/"systems/harum_capability_registry.json",
            "leases":self.root/"state/coordination/work_leases.json",
            "policy":self.root/"systems/harum_dispatch_policy.json",
            "panel":self.root/"systems/harum_instance_panel.json",
            "bootstrap":self.root/"systems/harum_bootstrap_manifest.json",
            "validation":self.root/"state/coordination/validation.json",
            "dispatch":self.root/"state/coordination/dispatch_plan.json",
            "health":self.root/"state/coordination/health.json",
            "capsule":self.root/"state/coordination/context_capsule.json",
            "meta":self.root/"state/coordination/meta_plan.json",
            "meta_policy":self.root/"systems/harum_meta_coordination.json",
            "passports":self.root/"state/coordination/instance_passports.json",
            "capability_board":self.root/"state/coordination/capability_board.json",
            "remote_receipts":self.root/"state/coordination/remote_receipts",
            "remote_receipt_index":self.root/"state/coordination/remote_receipt_index.json",
            "lock":self.root/".harum-assembly/coord.lock",
        }

    def _configure_bus(self) -> None:
        bus.ROOT=self.root/".harum-assembly"
        bus.LOG=self.paths["events"]
        bus.STATE=self.paths["state"]

    def _mutation_paths(self) -> list[Path]:
        return [
            self.paths["events"],self.paths["state"],self.paths["jev"],
            self.paths["tree"],self.paths["leases"],self.paths["dispatch"],
            self.paths["health"],self.paths["meta"],self.paths["capsule"],self.paths["capability_board"],self.paths["remote_receipt_index"],
        ]

    @contextlib.contextmanager
    def transaction(self):
        snapshots={}
        with _local_lock(self.paths["lock"]):
            for path in self._mutation_paths():
                snapshots[path]=path.read_bytes() if path.exists() else None
            try:
                yield
            except Exception:
                for path,data in snapshots.items():
                    if data is None:
                        if path.exists():
                            path.unlink()
                    else:
                        path.parent.mkdir(parents=True, exist_ok=True)
                        path.write_bytes(data)
                raise

    def _tree_index(self) -> dict[str,dict[str,Any]]:
        tree=_load(self.paths["tree"],{})
        return {str(node.get("id")):node for node in _walk(tree.get("root",{})) if node.get("id")}

    def _update_tree_node(self, work_id: str, **changes: Any) -> None:
        tree=_load(self.paths["tree"],{})
        found=False
        for node in _walk(tree.get("root",{})):
            if node.get("id")==work_id:
                node.update(changes)
                found=True
                break
        if not found:
            raise CoordinationError(f"work_id not found in project tree: {work_id}")
        tree["updated_at"]=dt.datetime.now(dt.timezone.utc).isoformat()
        _write(self.paths["tree"],tree)

    def _merge_jev_rules(self, fresh: dict[str,Any]) -> dict[str,Any]:
        current=_load(self.paths["jev"],{})
        rules={}
        rules.update(current.get("rules",{}) or {})
        rules.update(fresh.get("rules",{}) or {})
        fresh["rules"]=rules

        current_completed={
            str(row.get("work_id")):row
            for row in (current.get("completed_work",[]) or [])
            if row.get("work_id")
        }
        merged_completed=[]
        for row in (fresh.get("completed_work",[]) or []):
            work_id=str(row.get("work_id") or "")
            merged={**(current_completed.get(work_id,{}) or {}),**row}
            merged_completed.append(merged)
        fresh["completed_work"]=merged_completed

        for key,value in current.items():
            if key not in fresh and key not in {"open_work","completed_work","open_help_requests","open_decisions","conflicts","role_inboxes"}:
                fresh[key]=value
        return fresh

    def _reconcile_remote_receipts(self) -> list[dict[str,Any]]:
        index=_load(self.paths["remote_receipt_index"],{"schema":"harum.remote-receipt-index/v1","processed":[]})
        receipts=load_pending_receipts(self.paths["remote_receipts"],index)
        if not receipts:
            return []
        tree_index=self._tree_index()
        leases=_load(self.paths["leases"],{"leases":{}})
        active=leases.get("leases",{}) or {}
        results=[]
        self._configure_bus()
        for receipt in receipts:
            decision=evaluate_remote_result(
                receipt,
                tree_node=tree_index.get(receipt["work_id"]),
                active_lease=active.get(receipt["work_id"]),
            )
            row={"receipt_id":receipt["receipt_id"],"work_id":receipt["work_id"],**decision}
            if not decision.get("accepted"):
                results.append(row)
                continue
            event=bus.emit(
                "work.completed",receipt["role"],receipt["work_id"],
                {
                    "summary":"PRONTO: "+receipt["summary"],
                    "result_refs":receipt.get("result_refs",[]),
                    "remote_receipt_id":receipt["receipt_id"],
                },
                producer=receipt["actor_id"],work_id=receipt["work_id"],
                evidence=receipt.get("evidence",[]),
                idempotency_key="remote-result:"+receipt["receipt_id"],
            )
            self._update_tree_node(
                receipt["work_id"],state="succeeded",owner=receipt["actor_id"],
                completed_at=dt.datetime.now(dt.timezone.utc).isoformat(),
                evidence=receipt.get("evidence",[]),result_refs=receipt.get("result_refs",[]),
            )
            mark_processed(index,receipt["receipt_id"])
            row["event_id"]=event.get("event_id")
            results.append(row)
        _write(self.paths["remote_receipt_index"],index)
        return results

    def sync(self) -> dict[str,Any]:
        self._configure_bus()
        remote_receipts=self._reconcile_remote_receipts()
        state=bus.load()
        fresh=self._merge_jev_rules(build_view(state))
        _write(self.paths["jev"],fresh)

        leases=_load(self.paths["leases"],{"schema":"harum.work-leases/v2","leases":{}})
        fabric=CoordinationFabric(leases,default_ttl_seconds=int(leases.get("default_ttl_seconds",900) or 900))
        reclaimed=fabric.reclaim_expired()
        if reclaimed:
            _write(self.paths["leases"],leases)

        result=refresh_projections(
            jev=fresh,
            tree=_load(self.paths["tree"],{}),
            registry=_load(self.paths["registry"],{}),
            leases=leases,
            policy=_load(self.paths["policy"],{}),
            panel=_load(self.paths["panel"],{}),
            bootstrap=_load(self.paths["bootstrap"],{}),
            assembly_state=state,
            validation=_load(self.paths["validation"],{}),
            meta_policy=_load(self.paths["meta_policy"],{}),
            persisted_passports=(_load(self.paths["passports"],{}).get("passports",[]) or []),
        )
        _write(self.paths["dispatch"],result["dispatch"])
        _write(self.paths["health"],result["health"])
        _write(self.paths["meta"],result["meta"])
        _write(self.paths["capsule"],result["capsule"])
        _write(self.paths["capability_board"],result["capability_board"])
        return {
            "health":result["health"].get("status"),
            "dispatch_summary":result["dispatch"].get("summary",{}),
            "reclaimed_leases":reclaimed,
            "capsule_generated_at":result["capsule"].get("generated_at"),
            "primary_move":(result["meta"].get("primary_move") or {}).get("work_id"),
            "remote_receipts":remote_receipts,
            "capability_board":result["capability_board"].get("summary",{}),
        }

    def projection_freshness(self) -> dict[str,Any]:
        return assess_projection_freshness(
            jev=_load(self.paths["jev"],{}),
            projections={
                "dispatch":_load(self.paths["dispatch"],{}),
                "health":_load(self.paths["health"],{}),
                "meta":_load(self.paths["meta"],{}),
                "capsule":_load(self.paths["capsule"],{}),
                "capability_board":_load(self.paths["capability_board"],{}),
            },
        )

    def status(self, role: str|None=None) -> dict[str,Any]:
        capsule=_load(self.paths["capsule"],{})
        jev=_load(self.paths["jev"],{})
        dispatch=_load(self.paths["dispatch"],{})
        freshness=self.projection_freshness()
        assignments=dispatch.get("assignments",[]) or []
        if role:
            assignments=[
                row for row in assignments
                if role in (row.get("candidate_roles") or []) or row.get("target_role")==role or row.get("role")==role
            ]
        meta=_load(self.paths["meta"],{})
        trusted_assignments=assignments if freshness.get("fresh") else []
        return {
            "focus":capsule.get("focus",{}),
            "health":capsule.get("health",{}),
            "checkpoint":capsule.get("checkpoint",{}),
            "projection_freshness":freshness,
            "available_work":[x for x in trusted_assignments if x.get("state")=="available"],
            "leased_work":[x for x in trusted_assignments if x.get("state")=="leased"],
            "open_help":[x for x in jev.get("open_help_requests",[]) if not role or x.get("target_role")==role],
            "inbox":(jev.get("role_inboxes",{}) or {}).get(role,[]) if role else jev.get("role_inboxes",{}),
            "advice":meta if freshness.get("fresh") else {
                "stale":True,
                "action":"run-harum-coord-sync",
                "source_last_event":meta.get("source_last_event"),
                "current_jev_event":freshness.get("current_jev_event"),
            },
        }

    def capabilities(self) -> dict[str,Any]:
        return _load(self.paths["capability_board"],{})

    def guard_write(self, actor: str, scopes: list[str]) -> dict[str,Any]:
        freshness=self.projection_freshness()
        if not freshness.get("fresh"):
            return {
                "schema":"harum.prewrite-guard/v1",
                "actor_id":actor,
                "requested_scopes":sorted(set(scopes)),
                "allowed":False,
                "mode":"sync-required",
                "blockers":[{
                    "kind":"stale-coordination-projection",
                    "current_jev_event":freshness.get("current_jev_event"),
                    "stale":freshness.get("stale",[]),
                    "missing_watermark":freshness.get("missing_watermark",[]),
                }],
                "projection_freshness":freshness,
                "rule":"Derived coordination state must match JEV.last_event before connector mutation; run HARUM Coord sync first.",
            }
        result=evaluate_prewrite(
            actor_id=actor,
            requested_scopes=scopes,
            tree=_load(self.paths["tree"],{}),
            jev=_load(self.paths["jev"],{}),
            leases=_load(self.paths["leases"],{"leases":{}}),
        )
        result["projection_freshness"]=freshness
        return result

    def next_work(self, role: str|None=None, actor: str|None=None) -> dict[str,Any]|None:
        freshness=self.projection_freshness()
        if not freshness.get("fresh"):
            raise CoordinationError(
                "coordination projections are stale; run 'harum_coord sync' before selecting next work"
            )
        plan=_load(self.paths["dispatch"],{})
        candidates=[]
        for row in plan.get("assignments",[]) or []:
            if row.get("state")!="available":
                continue
            if role and row.get("candidate_roles") and role not in row.get("candidate_roles",[]):
                continue
            if actor and row.get("candidate_instances") and actor not in row.get("candidate_instances",[]):
                continue
            candidates.append(row)
        return candidates[0] if candidates else None

    def _assignment(self, work_id: str) -> dict[str,Any]:
        plan=_load(self.paths["dispatch"],{})
        for row in plan.get("assignments",[]) or []:
            if row.get("work_id")==work_id:
                return row
        raise CoordinationError(f"work_id not present in dispatch plan: {work_id}")

    def _lease_state(self):
        value=_load(self.paths["leases"],{"schema":"harum.work-leases/v2","default_ttl_seconds":900,"leases":{}})
        value.setdefault("leases",{})
        return value

    def claim(self, work_id: str, actor: str, role: str, ttl_seconds: int|None=None) -> dict[str,Any]:
        with self.transaction():
            self.sync()
            health=_load(self.paths["health"],{})
            if health.get("status")=="attention":
                raise CoordinationError("coordination health=attention; resolve issues before new claim")

            assignment=self._assignment(work_id)
            if assignment.get("state")!="available":
                raise CoordinationError(f"work is not available: {assignment.get('state')} / {assignment.get('reason')}")
            if assignment.get("candidate_roles") and role not in assignment.get("candidate_roles",[]):
                raise CoordinationError(f"role {role} is not eligible for {work_id}")
            if assignment.get("candidate_instances") and actor not in assignment.get("candidate_instances",[]):
                raise CoordinationError(f"actor {actor} is not a routed candidate for {work_id}")

            leases=self._lease_state()
            fabric=CoordinationFabric(leases,default_ttl_seconds=int(leases.get("default_ttl_seconds",900) or 900))
            result=fabric.claim(
                work_id,actor,role=role,
                write_scope=assignment.get("write_scope") or [],
                max_helpers=int(assignment.get("max_helpers",0) or 0),
                ttl_seconds=ttl_seconds,
            )
            if not result.get("ok"):
                raise CoordinationError(f"lease rejected: {result.get('reason')}")
            lease=result["lease"]
            _write(self.paths["leases"],leases)

            node=self._tree_index().get(work_id,{})
            self._update_tree_node(
                work_id,state="executing",owner=actor,owner_role=role,
                lease_id=lease["lease_id"],updated_at=dt.datetime.now(dt.timezone.utc).isoformat()
            )
            self._configure_bus()
            event=bus.emit(
                "work.claimed",role,work_id,
                {
                    "summary":f"FAZENDO: {work_id}",
                    "lease_id":lease["lease_id"],
                    "expires_at":_utc_iso_from_ts(lease["expires_at"]),
                    "intent_key":node.get("intent_key"),
                },
                producer=actor,work_id=work_id,
                idempotency_key=f"{work_id}:claim:{lease['lease_id']}",
            )
            sync=self.sync()
            return {"ok":True,"event":event,"lease":lease,"sync":sync}

    def take_next(self, actor: str, role: str, ttl_seconds: int|None=None) -> dict[str,Any]:
        with _local_lock(self.paths["lock"]):
            self.sync()
            nxt=self.next_work(role=role,actor=actor)
        if not nxt:
            raise CoordinationError(f"no available work for role={role}")
        return self.claim(nxt["work_id"],actor,role,ttl_seconds=ttl_seconds)

    def _owned_lease(self, work_id: str, actor: str) -> tuple[dict[str,Any],CoordinationFabric,dict[str,Any]]:
        leases=self._lease_state()
        fabric=CoordinationFabric(leases,default_ttl_seconds=int(leases.get("default_ttl_seconds",900) or 900))
        fabric.reclaim_expired()
        row=leases.get("leases",{}).get(work_id)
        if not row:
            raise CoordinationError(f"no active lease for {work_id}")
        if row.get("owner")!=actor:
            raise CoordinationError(f"lease owned by {row.get('owner')}, not {actor}")
        return leases,fabric,row

    def progress(self, work_id: str, actor: str, role: str, summary: str, ttl_seconds: int|None=None) -> dict[str,Any]:
        with self.transaction():
            leases,fabric,row=self._owned_lease(work_id,actor)
            result=fabric.heartbeat(work_id,actor,row["lease_id"],ttl_seconds=ttl_seconds)
            if not result.get("ok"):
                raise CoordinationError(f"heartbeat rejected: {result.get('reason')}")
            _write(self.paths["leases"],leases)
            self._update_tree_node(work_id,state="executing",owner=actor,updated_at=dt.datetime.now(dt.timezone.utc).isoformat())
            self._configure_bus()
            event=bus.emit(
                "work.progressed",role,work_id,
                {"summary":"FAZENDO: "+summary,"lease_id":row["lease_id"],"expires_at":_utc_iso_from_ts(result["lease"]["expires_at"])},
                producer=actor,work_id=work_id,
            )
            sync=self.sync()
            return {"ok":True,"event":event,"lease":result["lease"],"sync":sync}

    def complete(self, work_id: str, actor: str, role: str, summary: str, evidence: Iterable[str]|None=None, result_refs: Iterable[str]|None=None) -> dict[str,Any]:
        with self.transaction():
            leases,fabric,row=self._owned_lease(work_id,actor)
            self._configure_bus()
            event=bus.emit(
                "work.completed",role,work_id,
                {"summary":"PRONTO: "+summary,"result_refs":_uniq(result_refs)},
                producer=actor,work_id=work_id,evidence=_uniq(evidence),
                idempotency_key=f"{work_id}:complete:{row['lease_id']}",
            )
            if not fabric.release(work_id,actor,row["lease_id"]):
                raise CoordinationError("lease release failed")
            _write(self.paths["leases"],leases)
            self._update_tree_node(
                work_id,state="succeeded",owner=actor,completed_at=dt.datetime.now(dt.timezone.utc).isoformat(),
                evidence=_uniq(evidence),result_refs=_uniq(result_refs)
            )
            sync=self.sync()
            return {"ok":True,"event":event,"sync":sync}

    def block(self, work_id: str, actor: str, role: str, reason: str, evidence: Iterable[str]|None=None) -> dict[str,Any]:
        with self.transaction():
            leases,fabric,row=self._owned_lease(work_id,actor)
            self._configure_bus()
            event=bus.emit(
                "work.blocked",role,work_id,
                {"summary":"BLOQUEIO: "+reason,"reason":reason},
                producer=actor,work_id=work_id,evidence=_uniq(evidence),
                idempotency_key=f"{work_id}:blocked:{row['lease_id']}",
            )
            if not fabric.release(work_id,actor,row["lease_id"]):
                raise CoordinationError("lease release failed")
            _write(self.paths["leases"],leases)
            self._update_tree_node(work_id,state="blocked",owner=actor,blocker=reason,updated_at=dt.datetime.now(dt.timezone.utc).isoformat())
            sync=self.sync()
            return {"ok":True,"event":event,"sync":sync}

    def handoff(self, work_id: str, actor: str, role: str, target_role: str, summary: str, evidence: Iterable[str]|None=None) -> dict[str,Any]:
        with self.transaction():
            leases,fabric,row=self._owned_lease(work_id,actor)
            self._configure_bus()
            event=bus.emit(
                "handoff.created",role,work_id,
                {"summary":"PASSO: "+summary,"from_actor":actor,"target_role":target_role},
                producer=actor,target_role=target_role,work_id=work_id,evidence=_uniq(evidence),
                idempotency_key=f"{work_id}:handoff:{row['lease_id']}:{target_role}",
            )
            if not fabric.release(work_id,actor,row["lease_id"]):
                raise CoordinationError("lease release failed")
            _write(self.paths["leases"],leases)
            self._update_tree_node(
                work_id,state="open",owner=None,target_role=target_role,
                updated_at=dt.datetime.now(dt.timezone.utc).isoformat()
            )
            sync=self.sync()
            return {"ok":True,"event":event,"sync":sync}

    def help(self, source_role: str, target_role: str, work_id: str, question: str, context: str="", actor: str|None=None, evidence: Iterable[str]|None=None) -> dict[str,Any]:
        with self.transaction():
            self._configure_bus()
            request_id=f"{work_id}-help"
            event=bus.emit(
                "help.requested",source_role,work_id,
                {"request_id":request_id,"question":question,"context":context},
                producer=actor,target_role=target_role,work_id=work_id,evidence=_uniq(evidence),
                idempotency_key=f"{work_id}:help:{target_role}:{abs(hash(question))}",
            )
            sync=self.sync()
            return {"ok":True,"event":event,"sync":sync}

    def hello(
        self, actor: str, role: str, capabilities: Iterable[str]|None=None,
        skills: Iterable[str]|None=None, reachability: str="manual-resume",
        dispatch_modes: Iterable[str]|None=None, ttl_minutes: int=60,
        passport: dict[str,Any]|None=None,
    ) -> dict[str,Any]:
        with self.transaction():
            expires=(dt.datetime.now(dt.timezone.utc)+dt.timedelta(minutes=max(5,ttl_minutes))).isoformat()
            if passport:
                safe=sanitize_passport({**passport,"actor_id":actor})
                payload={
                    "roles":safe.get("roles") or [role],
                    "capabilities":safe.get("capabilities",[]),
                    "skills":safe.get("skills",[]),
                    "connectors":safe.get("connectors",[]),
                    "capacity":safe.get("capacity",{}),
                    "constraints":safe.get("constraints",[]),
                    "preferred_work_types":safe.get("preferred_work_types",[]),
                    "reachability":safe.get("reachability") or reachability,
                    "dispatch_modes":safe.get("dispatch_modes") or _uniq(dispatch_modes) or ["jev-resume"],
                    "expires_at":safe.get("expires_at") or expires,
                    "current_focus":(_load(self.paths["capsule"],{}).get("focus") or {}).get("project"),
                }
            else:
                payload={
                "roles":[role],
                "capabilities":_uniq(capabilities),
                "skills":[{"id":skill,"category":None,"capabilities":[]} for skill in _uniq(skills)],
                "reachability":reachability,
                "dispatch_modes":_uniq(dispatch_modes) or ["jev-resume"],
                "expires_at":expires,
                "current_focus":(_load(self.paths["capsule"],{}).get("focus") or {}).get("project"),
                }
            self._configure_bus()
            event=bus.emit("instance.hello",role,actor,payload,producer=actor)
            sync=self.sync()
            return {"ok":True,"event":event,"sync":sync}

def _print_lite(status: dict[str,Any]) -> None:
    focus=(status.get("focus") or {}).get("project") or "HARUM"
    health=(status.get("health") or {}).get("status") or "unknown"
    print(f"TENHO: foco={focus} · saúde={health}")
    freshness=status.get("projection_freshness",{}) or {}
    if freshness and not freshness.get("fresh",True):
        print(
            "PRECISO: SYNC REQUIRED · projeções antigas="
            + ",".join(freshness.get("stale",[]) or freshness.get("missing_watermark",[]))
        )
        print("PASSO: python -m core.meaw.harum_coord sync")
        return
    advice=status.get("advice",{}) or {}
    primary=advice.get("primary_move") or {}
    available=status.get("available_work",[]) or []
    if primary:
        print(f"PASSO: {primary.get('work_id')} · meta={primary.get('meta_score')} · {primary.get('reason')}")
    elif available:
        top=available[0]
        print(f"PASSO: {top.get('work_id')} · prioridade={top.get('priority')} · papel={','.join(top.get('candidate_roles') or [])}")
    else:
        print("PASSO: nenhum trabalho disponível para este filtro")
    for row in (status.get("open_help",[]) or [])[:4]:
        print(f"PRECISO: {row.get('work_id')} · {row.get('question')}")
    for row in (status.get("leased_work",[]) or [])[:4]:
        print(f"FAZENDO: {row.get('work_id')} · dono={row.get('owner')}")

def build_parser() -> argparse.ArgumentParser:
    p=argparse.ArgumentParser(description="HARUM Coord — single operational doorway for JEV coordination")
    p.add_argument("--root",default=".")
    p.add_argument("--json",action="store_true")
    sub=p.add_subparsers(dest="command",required=True)

    s=sub.add_parser("status");s.add_argument("--role")
    sub.add_parser("advice")
    sub.add_parser("capabilities")
    s=sub.add_parser("guard-write");s.add_argument("--actor",required=True);s.add_argument("--scope",action="append",required=True)
    s=sub.add_parser("sync")
    s=sub.add_parser("next");s.add_argument("--role");s.add_argument("--actor")

    s=sub.add_parser("claim");s.add_argument("work_id");s.add_argument("--actor",required=True);s.add_argument("--role",required=True);s.add_argument("--ttl",type=int)
    s=sub.add_parser("take");s.add_argument("--actor",required=True);s.add_argument("--role",required=True);s.add_argument("--ttl",type=int)

    s=sub.add_parser("progress");s.add_argument("work_id");s.add_argument("--actor",required=True);s.add_argument("--role",required=True);s.add_argument("--summary",required=True);s.add_argument("--ttl",type=int)
    s=sub.add_parser("complete");s.add_argument("work_id");s.add_argument("--actor",required=True);s.add_argument("--role",required=True);s.add_argument("--summary",required=True);s.add_argument("--evidence",action="append",default=[]);s.add_argument("--result-ref",action="append",default=[])
    s=sub.add_parser("block");s.add_argument("work_id");s.add_argument("--actor",required=True);s.add_argument("--role",required=True);s.add_argument("--reason",required=True);s.add_argument("--evidence",action="append",default=[])
    s=sub.add_parser("handoff");s.add_argument("work_id");s.add_argument("--actor",required=True);s.add_argument("--role",required=True);s.add_argument("--target-role",required=True);s.add_argument("--summary",required=True);s.add_argument("--evidence",action="append",default=[])

    s=sub.add_parser("help");s.add_argument("work_id");s.add_argument("--source-role",required=True);s.add_argument("--target-role",required=True);s.add_argument("--question",required=True);s.add_argument("--context",default="");s.add_argument("--actor");s.add_argument("--evidence",action="append",default=[])

    s=sub.add_parser("hello");s.add_argument("--actor",required=True);s.add_argument("--role",required=True);s.add_argument("--capability",action="append",default=[]);s.add_argument("--skill",action="append",default=[]);s.add_argument("--reachability",default="manual-resume",choices=["active","endpoint","manual-resume","offline"]);s.add_argument("--dispatch-mode",action="append",default=[]);s.add_argument("--ttl-minutes",type=int,default=60);s.add_argument("--passport")
    return p

def main() -> None:
    args=build_parser().parse_args()
    coord=HarumCoord(args.root)
    try:
        if args.command=="status":
            result=coord.status(role=args.role)
            if args.json: print(json.dumps(result,ensure_ascii=False,indent=2))
            else: _print_lite(result)
            return
        if args.command=="advice":
            result=_load(coord.paths["meta"],{})
            print(json.dumps(result,ensure_ascii=False,indent=2) if args.json else json.dumps(result,ensure_ascii=False))
            return
        if args.command=="guard-write":
            result=coord.guard_write(args.actor,args.scope)
            print(json.dumps(result,ensure_ascii=False,indent=2) if args.json else ("WRITE OK" if result.get("allowed") else "BLOCK · support-only"))
            if not result.get("allowed"):
                raise SystemExit(2)
            return
        if args.command=="capabilities":
            result=coord.capabilities()
            if args.json:
                print(json.dumps(result,ensure_ascii=False,indent=2))
            else:
                summary=result.get("summary",{})
                print(f"TENHO: instances={summary.get('instances_fresh_dispatchable',0)}/{summary.get('instances_total',0)} · connectors={summary.get('connectors_known',0)} · skills={summary.get('skills_known',0)}")
                for row in result.get("instances",[])[:8]:
                    print(f"TENHO: {row.get('actor_id')} · {row.get('reachability')} · connectors={len(row.get('connectors',[]))} · skills={row.get('skill_count',0)}")
                for gap in result.get("gaps",[])[:8]:
                    print(f"PRECISO: {gap.get('work_id')} · {gap.get('reason')}")
            return
        if args.command=="sync":
            result=coord.sync()
        elif args.command=="next":
            result=coord.next_work(role=args.role,actor=args.actor) or {}
        elif args.command=="claim":
            result=coord.claim(args.work_id,args.actor,args.role,args.ttl)
        elif args.command=="take":
            result=coord.take_next(args.actor,args.role,args.ttl)
        elif args.command=="progress":
            result=coord.progress(args.work_id,args.actor,args.role,args.summary,args.ttl)
        elif args.command=="complete":
            result=coord.complete(args.work_id,args.actor,args.role,args.summary,args.evidence,args.result_ref)
        elif args.command=="block":
            result=coord.block(args.work_id,args.actor,args.role,args.reason,args.evidence)
        elif args.command=="handoff":
            result=coord.handoff(args.work_id,args.actor,args.role,args.target_role,args.summary,args.evidence)
        elif args.command=="help":
            result=coord.help(args.source_role,args.target_role,args.work_id,args.question,args.context,args.actor,args.evidence)
        elif args.command=="hello":
            passport=_load(Path(args.passport),{}) if args.passport else None
            result=coord.hello(args.actor,args.role,args.capability,args.skill,args.reachability,args.dispatch_mode,args.ttl_minutes,passport)
        else:
            raise CoordinationError("unknown command")
        print(json.dumps(result,ensure_ascii=False,indent=2) if args.json else json.dumps(result,ensure_ascii=False))
    except CoordinationError as exc:
        raise SystemExit(f"CONFLITO/BLOQUEIO: {exc}")

if __name__=="__main__":
    main()
