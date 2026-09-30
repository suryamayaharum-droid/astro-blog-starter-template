#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
import pathlib
from typing import Any

def clamp(value: Any, default: float) -> float:
    try:
        return max(0.0, min(1.0, float(value)))
    except (TypeError, ValueError):
        return default

def synthesize_decision(decision_id: str, decision: dict[str, Any]) -> dict[str, Any]:
    proposals = [p for p in decision.get("proposals", []) if p.get("option")]
    support: dict[str, float] = {}
    for proposal in proposals:
        confidence = clamp(proposal.get("confidence"), 0.5)
        risk = clamp(proposal.get("risk"), 0.5)
        weight = confidence * (1.0 - risk)
        support[proposal["option"]] = support.get(proposal["option"], 0.0) + weight
    total = sum(support.values())
    normalized = {k: (v / total if total else 0.0) for k, v in support.items()}
    leader = max(normalized, key=normalized.get) if normalized else None
    leader_score = normalized.get(leader, 0.0) if leader else 0.0
    return {
        "decision_id": decision_id,
        "status": decision.get("status", "open"),
        "proposal_count": len(proposals),
        "support": normalized,
        "leading_option": leader,
        "agreement": round(leader_score, 4),
        "disagreement": round(1.0 - leader_score, 4) if normalized else 1.0,
        "needs_human_or_fresh_evidence": bool(len(normalized) > 1 and leader_score < 0.67),
        "authority": "advisory_only",
    }

def build_view(state: dict[str, Any]) -> dict[str, Any]:
    open_work = [
        item for item in state.get("work_items", {}).values()
        if item.get("status") not in {"succeeded", "superseded"}
    ]
    open_help = [
        {"request_id": rid, **req}
        for rid, req in state.get("help_requests", {}).items()
        if req.get("status") == "open"
    ]
    decisions = {
        decision_id: synthesize_decision(decision_id, decision)
        for decision_id, decision in state.get("decisions", {}).items()
        if decision.get("status") != "resolved"
    }
    return {
        "schema": "harum.jev-coordination-view/v1",
        "source_state_schema": state.get("schema"),
        "last_event": state.get("last_event"),
        "checkpoint": state.get("current_checkpoint"),
        "open_work": open_work,
        "open_help_requests": open_help,
        "open_decisions": decisions,
        "conflicts": state.get("conflicts", []),
        "role_inboxes": {
            role: event_ids
            for role, event_ids in state.get("inboxes", {}).items()
            if event_ids
        },
        "rules": {
            "authority": "advisory_only",
            "no_hidden_chain_of_thought": True,
            "no_permission_expansion": True,
            "live_external_state_overrides_repo": True,
            "secrets_forbidden": True,
        },
    }

def main() -> None:
    parser = argparse.ArgumentParser(description="Build JEV advisory coordination view")
    parser.add_argument("--state", default=".harum-assembly/state.json")
    parser.add_argument("--out", default=".harum-assembly/jev_view.json")
    args = parser.parse_args()
    state_path = pathlib.Path(args.state)
    out_path = pathlib.Path(args.out)
    state = json.loads(state_path.read_text(encoding="utf-8"))
    view = build_view(state)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(view, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(view, ensure_ascii=False))

if __name__ == "__main__":
    main()
