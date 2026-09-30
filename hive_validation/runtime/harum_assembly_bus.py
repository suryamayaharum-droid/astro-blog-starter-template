#!/usr/bin/env python3
from __future__ import annotations
import argparse
import datetime
import json
import pathlib
import uuid
from typing import Any

ROOT = pathlib.Path(".harum-assembly")
LOG = ROOT / "events.jsonl"
STATE = ROOT / "state.json"

COORDINATION_TYPES = {
    "instance.hello",
    "checkpoint.published",
    "work.claimed",
    "work.progressed",
    "work.completed",
    "work.blocked",
    "handoff.created",
    "handoff.accepted",
    "help.requested",
    "help.answered",
    "evidence.observed",
    "decision.proposed",
    "decision.resolved",
    "conflict.detected",
    "jev.synthesis",
}

def now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def _uniq(values):
    return sorted({str(v).strip() for v in (values or []) if str(v).strip()})

def _sanitize_hello_payload(payload: dict[str, Any]) -> dict[str, Any]:
    connectors=[]
    for row in payload.get("connectors",[]) or []:
        if not isinstance(row,dict) or not row.get("id"):
            continue
        connectors.append({
            "id":str(row.get("id")),
            "provider":str(row.get("provider") or row.get("id")),
            "status":str(row.get("status") or "declared"),
            "capabilities":_uniq(row.get("capabilities")),
            "requires_user_auth":bool(row.get("requires_user_auth",True)),
            "evidence":_uniq(row.get("evidence")),
        })
    skills=[]
    for row in payload.get("skills",[]) or []:
        if not isinstance(row,dict) or not row.get("id"):
            continue
        skills.append({
            "id":str(row.get("id")),
            "category":str(row.get("category")) if row.get("category") is not None else None,
            "capabilities":_uniq(row.get("capabilities")),
        })
    return {
        "capabilities":_uniq(payload.get("capabilities")),
        "current_focus":payload.get("current_focus"),
        "roles":_uniq(payload.get("roles")),
        "connectors":connectors,
        "skills":skills,
        "capacity":dict(payload.get("capacity") or {}),
        "constraints":_uniq(payload.get("constraints")),
        "preferred_work_types":_uniq(payload.get("preferred_work_types")),
        "reachability":str(payload.get("reachability") or "manual-resume"),
        "dispatch_modes":_uniq(payload.get("dispatch_modes")),
        "expires_at":payload.get("expires_at"),
        "security":{
            "contains_credentials":False,
            "grants_permissions":False,
            "auth_boundary":"local-runtime",
        },
    }

def default_state() -> dict[str, Any]:
    return {
        "schema": "harum.assembly-state/v2",
        "version": 2,
        "last_event": None,
        "assets": {},
        "incidents": [],
        "instances": {},
        "work_items": {},
        "help_requests": {},
        "decisions": {},
        "conflicts": [],
        "inboxes": {},
        "idempotency": {},
        "actor_clocks": {},
        "current_checkpoint": None,
    }

def load() -> dict[str, Any]:
    if not STATE.exists():
        return default_state()
    data = json.loads(STATE.read_text(encoding="utf-8"))
    base = default_state()
    base.update(data)
    for key in ("assets","instances","work_items","help_requests","decisions","inboxes","idempotency"):
        base.setdefault(key,{})
    base.setdefault("incidents",[])
    base.setdefault("conflicts",[])
    return base

def save(state: dict[str, Any]) -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def _append_inbox(state: dict[str, Any], role: str | None, event: dict[str, Any]) -> None:
    if not role:
        return
    inbox = state["inboxes"].setdefault(role, [])
    if event["event_id"] not in inbox:
        inbox.append(event["event_id"])

def _work(state: dict[str, Any], event: dict[str, Any]) -> dict[str, Any] | None:
    work_id = event.get("work_id")
    if not work_id:
        return None
    item = state["work_items"].setdefault(work_id, {"work_id": work_id, "events": []})
    item["events"].append(event["event_id"])
    item["updated_at"] = event["occurred_at"]
    return item

def project(event: dict[str, Any]) -> dict[str, Any]:
    state = load()
    state["last_event"] = event["event_id"]
    causal=event.get("causal") or {}
    actor=causal.get("actor")
    seq=causal.get("seq")
    if actor and isinstance(seq,int):
        state["actor_clocks"][actor]=max(int(state["actor_clocks"].get(actor,0) or 0),seq)
    key = event.get("idempotency_key")
    if key:
        state["idempotency"][key] = event["event_id"]

    asset = event.get("asset_code")
    if asset:
        item = state["assets"].setdefault(asset, {"events": []})
        item["events"].append(event["event_id"])
        item["last_type"] = event["type"]
        item["updated_at"] = event["occurred_at"]
        if event["type"] == "publish.succeeded":
            item.setdefault("publications", []).append(event["payload"])
        if event["type"] == "metrics.observed":
            item["latest_metrics"] = event["payload"]

    et = event["type"]
    producer = event.get("producer") or event.get("source_role")
    target = event.get("target_role")
    work = _work(state, event)

    if et == "instance.hello":
        state["instances"][producer] = {
            "role": event.get("source_role"),
            "roles": event["payload"].get("roles", []),
            "last_seen": event["occurred_at"],
            "expires_at": event["payload"].get("expires_at"),
            "capabilities": event["payload"].get("capabilities", []),
            "connectors": event["payload"].get("connectors", []),
            "skills": event["payload"].get("skills", []),
            "capacity": event["payload"].get("capacity", {}),
            "constraints": event["payload"].get("constraints", []),
            "preferred_work_types": event["payload"].get("preferred_work_types", []),
            "reachability": event["payload"].get("reachability", "manual-resume"),
            "dispatch_modes": event["payload"].get("dispatch_modes", []),
            "current_focus": event["payload"].get("current_focus"),
            "security": event["payload"].get("security", {}),
        }
    elif et == "checkpoint.published":
        state["current_checkpoint"] = {
            "event_id": event["event_id"],
            "occurred_at": event["occurred_at"],
            "payload": event["payload"],
            "evidence": event.get("evidence", []),
        }
    elif et == "handoff.created":
        if work is not None:
            work.update({"status": "proposed", "target_role": target, "owner": None, "payload": event["payload"]})
        _append_inbox(state, target, event)
    elif et in {"work.claimed", "handoff.accepted"}:
        if work is not None:
            work.update({"status": "claimed", "owner": producer, "target_role": target or work.get("target_role"), "payload": event["payload"]})
    elif et == "work.progressed":
        if work is not None:
            work.update({"status": "executing", "owner": producer, "progress": event["payload"]})
    elif et == "work.completed":
        if work is not None:
            work.update({"status": "succeeded", "owner": producer, "result": event["payload"], "evidence": event.get("evidence", [])})
    elif et == "work.blocked":
        if work is not None:
            work.update({"status": "blocked", "owner": producer, "blocker": event["payload"], "evidence": event.get("evidence", [])})
    elif et == "help.requested":
        request_id = event["payload"].get("request_id") or event["correlation_id"]
        state["help_requests"][request_id] = {
            "status": "open",
            "event_id": event["event_id"],
            "source_role": event.get("source_role"),
            "target_role": target,
            "work_id": event.get("work_id"),
            "question": event["payload"].get("question"),
            "context": event["payload"].get("context"),
            "created_at": event["occurred_at"],
        }
        _append_inbox(state, target, event)
    elif et == "help.answered":
        request_id = event["payload"].get("request_id") or event["correlation_id"]
        req = state["help_requests"].setdefault(request_id, {})
        req.update({
            "status": "answered",
            "answer_event_id": event["event_id"],
            "answered_by": producer,
            "answer": event["payload"].get("answer"),
            "evidence": event.get("evidence", []),
            "updated_at": event["occurred_at"],
        })
    elif et == "decision.proposed":
        decision_id = event["payload"].get("decision_id") or event["correlation_id"]
        decision = state["decisions"].setdefault(decision_id, {"status": "open", "proposals": []})
        decision["proposals"].append({
            "event_id": event["event_id"],
            "producer": producer,
            "option": event["payload"].get("option"),
            "summary": event["payload"].get("summary"),
            "confidence": event.get("confidence"),
            "risk": event.get("risk"),
            "evidence": event.get("evidence", []),
        })
    elif et == "decision.resolved":
        decision_id = event["payload"].get("decision_id") or event["correlation_id"]
        decision = state["decisions"].setdefault(decision_id, {"proposals": []})
        decision.update({
            "status": "resolved",
            "resolution": event["payload"],
            "resolved_by": producer,
            "resolved_at": event["occurred_at"],
        })
    elif et == "jev.synthesis":
        decision_id = event["payload"].get("decision_id") or event["correlation_id"]
        decision = state["decisions"].setdefault(decision_id, {"proposals": []})
        decision["jev_synthesis"] = event["payload"]
        decision["jev_event_id"] = event["event_id"]
    elif et == "conflict.detected":
        state["conflicts"].append({
            "event_id": event["event_id"],
            "correlation_id": event["correlation_id"],
            "work_id": event.get("work_id"),
            "payload": event["payload"],
            "evidence": event.get("evidence", []),
            "created_at": event["occurred_at"],
        })
    elif et == "incident.opened":
        state["incidents"].append(event["payload"])

    save(state)
    return state

def emit(
    event_type: str,
    role: str,
    correlation: str,
    payload: dict[str, Any],
    asset: str | None = None,
    evidence: list[Any] | None = None,
    producer: str | None = None,
    target_role: str | None = None,
    work_id: str | None = None,
    confidence: float | None = None,
    risk: float | None = None,
    idempotency_key: str | None = None,
) -> dict[str, Any]:
    state = load()
    if idempotency_key and idempotency_key in state.get("idempotency", {}):
        return {
            "deduplicated": True,
            "idempotency_key": idempotency_key,
            "existing_event_id": state["idempotency"][idempotency_key],
        }

    if event_type == "instance.hello":
        payload = _sanitize_hello_payload(payload)

    actor_id=producer or role
    next_seq=int(state.get("actor_clocks",{}).get(actor_id,0) or 0)+1
    event = {
        "event_id": str(uuid.uuid4()),
        "type": event_type,
        "occurred_at": now(),
        "producer": producer or None,
        "source_role": role,
        "target_role": target_role or None,
        "work_id": work_id or None,
        "asset_code": asset or None,
        "correlation_id": correlation,
        "idempotency_key": idempotency_key or None,
        "confidence": confidence,
        "risk": risk,
        "causal": {"actor": actor_id, "seq": next_seq, "parent_event_id": state.get("last_event")},
        "payload": payload,
        "evidence": evidence or [],
    }
    ROOT.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event, ensure_ascii=False) + "\n")
    project(event)
    return event

def _json_arg(value: str, fallback: Any) -> Any:
    if not value:
        return fallback
    return json.loads(value)

def main() -> None:
    parser = argparse.ArgumentParser(description="HARUM durable cross-instance assembly bus")
    parser.add_argument("type")
    parser.add_argument("--role", required=True)
    parser.add_argument("--correlation", required=True)
    parser.add_argument("--producer")
    parser.add_argument("--target-role")
    parser.add_argument("--work-id")
    parser.add_argument("--asset")
    parser.add_argument("--idempotency-key")
    parser.add_argument("--confidence", type=float)
    parser.add_argument("--risk", type=float)
    parser.add_argument("--payload", default="{}")
    parser.add_argument("--evidence", default="[]")
    args = parser.parse_args()
    result = emit(
        args.type,
        args.role,
        args.correlation,
        _json_arg(args.payload, {}),
        asset=args.asset,
        evidence=_json_arg(args.evidence, []),
        producer=args.producer,
        target_role=args.target_role,
        work_id=args.work_id,
        confidence=args.confidence,
        risk=args.risk,
        idempotency_key=args.idempotency_key,
    )
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()
