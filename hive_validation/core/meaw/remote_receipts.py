from __future__ import annotations

import json
from pathlib import Path
from typing import Any


SCHEMA="harum.remote-result-receipt/v1"


def _uniq(values):
    return sorted({str(v).strip() for v in (values or []) if str(v).strip()})


def sanitize_remote_receipt(raw:dict[str,Any])->dict[str,Any]:
    """Whitelist an evidence-only result receipt.

    This record never authorizes execution. It describes work that the remote
    actor says is already complete and leaves acceptance to HARUM Coord.
    """
    if raw.get("schema")!=SCHEMA:
        raise ValueError("invalid remote receipt schema")
    required=["receipt_id","work_id","actor_id","role","summary","submitted_at"]
    for key in required:
        if not str(raw.get(key) or "").strip():
            raise ValueError(f"missing {key}")
    return {
        "schema":SCHEMA,
        "receipt_id":str(raw["receipt_id"]).strip(),
        "work_id":str(raw["work_id"]).strip(),
        "actor_id":str(raw["actor_id"]).strip(),
        "role":str(raw["role"]).strip(),
        "submitted_at":str(raw["submitted_at"]).strip(),
        "summary":str(raw["summary"]).strip(),
        "result_refs":_uniq(raw.get("result_refs")),
        "evidence":_uniq(raw.get("evidence")),
        "routing_evidence":{
            "board_commit":str((raw.get("routing_evidence") or {}).get("board_commit") or "").strip(),
            "actor_was_candidate":bool((raw.get("routing_evidence") or {}).get("actor_was_candidate",False)),
        },
        "external_actions_already_completed":bool(raw.get("external_actions_already_completed",False)),
        "contains_credentials":False,
    }


def load_pending_receipts(directory:Path,index:dict[str,Any])->list[dict[str,Any]]:
    processed=set(index.get("processed",[]) or [])
    rows=[]
    if not directory.exists():
        return rows
    for path in sorted(directory.glob("*.json")):
        try:
            safe=sanitize_remote_receipt(json.loads(path.read_text(encoding="utf-8")))
        except (ValueError,json.JSONDecodeError):
            continue
        if safe["receipt_id"] not in processed:
            safe["_path"]=str(path)
            rows.append(safe)
    return rows


def evaluate_remote_result(
    receipt:dict[str,Any],
    *,
    tree_node:dict[str,Any]|None,
    active_lease:dict[str,Any]|None,
)->dict[str,Any]:
    if not tree_node:
        return {"accepted":False,"reason":"unknown-work"}
    if tree_node.get("state") in {"succeeded","superseded","stable","stable-private"}:
        return {"accepted":False,"reason":"already-final"}
    policy=tree_node.get("remote_result_policy","manual-review")
    if policy!="auto-accept-evidence":
        return {"accepted":False,"reason":"manual-review-required"}
    if active_lease:
        return {"accepted":False,"reason":"active-lease"}
    if not receipt.get("external_actions_already_completed"):
        return {"accepted":False,"reason":"not-a-result-only-receipt"}
    if not receipt.get("evidence"):
        return {"accepted":False,"reason":"evidence-required"}
    routing=receipt.get("routing_evidence") or {}
    if not routing.get("actor_was_candidate") or not routing.get("board_commit"):
        return {"accepted":False,"reason":"routing-evidence-required"}
    target=tree_node.get("target_role")
    if target and receipt.get("role")!=target:
        return {"accepted":False,"reason":"role-mismatch"}
    return {"accepted":True,"reason":"evidence-backed-remote-result"}


def mark_processed(index:dict[str,Any],receipt_id:str)->dict[str,Any]:
    values=set(index.get("processed",[]) or [])
    values.add(receipt_id)
    index["schema"]="harum.remote-receipt-index/v1"
    index["processed"]=sorted(values)
    return index
