from __future__ import annotations
import hashlib
import json
from typing import Any

def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()

def _work_projection(jev: dict[str, Any]) -> list[dict[str, Any]]:
    rows=[]
    for work in jev.get("open_work",[]) or []:
        if not work.get("work_id"):
            continue
        rows.append({
            "work_id":work.get("work_id"),
            "status":work.get("status"),
            "owner":work.get("owner"),
            "target_role":work.get("target_role"),
            "updated_at":work.get("updated_at"),
        })
    return sorted(rows,key=lambda r:r["work_id"])

def _help_projection(jev: dict[str, Any]) -> list[dict[str, Any]]:
    rows=[]
    for req in jev.get("open_help_requests",[]) or []:
        if not req.get("request_id"):
            continue
        rows.append({
            "request_id":req.get("request_id"),
            "status":req.get("status"),
            "work_id":req.get("work_id"),
            "target_role":req.get("target_role"),
        })
    return sorted(rows,key=lambda r:r["request_id"])

def _registry_projection(registry: dict[str, Any]) -> list[dict[str, Any]]:
    rows=[]
    for role in registry.get("roles",[]) or []:
        if not role.get("role"):
            continue
        rows.append({
            "role":role.get("role"),
            "capabilities":sorted(role.get("capabilities",[]) or []),
            "limits":sorted(role.get("limits",[]) or []),
        })
    return sorted(rows,key=lambda r:r["role"])

def build_state_digest(
    *,
    panel: dict[str, Any],
    jev: dict[str, Any],
    project_tree: dict[str, Any],
    capability_registry: dict[str, Any],
    crdt_state: dict[str, Any] | None = None,
    canonical_commit: str | None = None,
    event_heads: list[str] | None = None,
) -> dict[str, Any]:
    focus=panel.get("current_focus",{}) or {}
    checkpoint=jev.get("checkpoint") or {}
    sections={
        "focus":{
            "project":focus.get("project"),
            "internal_name":focus.get("internal_name"),
            "next_layer":focus.get("next_layer"),
        },
        "checkpoint":{
            "event_id":checkpoint.get("event_id"),
            "occurred_at":checkpoint.get("occurred_at"),
            "payload":checkpoint.get("payload"),
        },
        "open_work":_work_projection(jev),
        "open_help":_help_projection(jev),
        "project_tree":project_tree,
        "capability_registry":_registry_projection(capability_registry),
        "crdt_root":(crdt_state or {}).get("root_sha256"),
        "event_heads":sorted(set(event_heads or [x for x in [jev.get("last_event"),checkpoint.get("event_id")] if x])),
    }
    section_hashes={name:digest(value) for name,value in sections.items()}
    return {
        "schema":"harum.state-digest/v1",
        "canonical_commit":canonical_commit,
        "root_sha256":digest(section_hashes),
        "section_hashes":section_hashes,
        "counts":{
            "open_work":len(sections["open_work"]),
            "open_help":len(sections["open_help"]),
            "capability_roles":len(sections["capability_registry"]),
            "event_heads":len(sections["event_heads"]),
        },
        "checkpoint_event_id":checkpoint.get("event_id"),
        "last_event":jev.get("last_event"),
    }

def validate_state_digest(value: dict[str, Any]) -> bool:
    if value.get("schema")!="harum.state-digest/v1":
        return False
    hashes=value.get("section_hashes")
    if not isinstance(hashes,dict) or not hashes:
        return False
    return value.get("root_sha256")==digest(hashes)

_ACTIONS={
    "focus":"refresh-current-focus",
    "checkpoint":"pull-latest-checkpoint",
    "open_work":"merge-coordination-work-state",
    "open_help":"merge-help-request-state",
    "project_tree":"fetch-canonical-project-tree",
    "capability_registry":"refresh-capability-registry",
    "crdt_root":"exchange-crdt-operations",
    "event_heads":"fetch-missing-event-heads",
}

def compare_state_digests(local: dict[str, Any], remote: dict[str, Any]) -> dict[str, Any]:
    local_ok=validate_state_digest(local)
    remote_ok=validate_state_digest(remote)
    if not local_ok or not remote_ok:
        return {
            "schema":"harum.anti-entropy-report/v1",
            "converged":False,
            "valid":{"local":local_ok,"remote":remote_ok},
            "differences":["invalid-digest"],
            "actions":["reject-and-rebuild-digest"],
        }

    keys=sorted(set(local["section_hashes"])|set(remote["section_hashes"]))
    differences=[k for k in keys if local["section_hashes"].get(k)!=remote["section_hashes"].get(k)]
    commit_equal=local.get("canonical_commit")==remote.get("canonical_commit")
    actions=[_ACTIONS.get(k,"reconcile-section:"+k) for k in differences]
    if not differences and not commit_equal:
        actions.append("commit-different-semantic-state-equal")
    return {
        "schema":"harum.anti-entropy-report/v1",
        "converged":not differences,
        "valid":{"local":True,"remote":True},
        "canonical_commit_equal":commit_equal,
        "differences":differences,
        "actions":actions,
        "local_root":local["root_sha256"],
        "remote_root":remote["root_sha256"],
    }

def build_peer_handshake(*, actor_id: str, state_digest: dict[str, Any], capabilities: list[str] | None = None) -> dict[str, Any]:
    if not actor_id:
        raise ValueError("actor_id required")
    if not validate_state_digest(state_digest):
        raise ValueError("valid state_digest required")
    return {
        "schema":"harum.peer-handshake/v1",
        "actor_id":actor_id,
        "state_digest":state_digest,
        "capabilities":sorted(set(capabilities or [])),
        "rules":{
            "digest_before_bundle":True,
            "leases_not_inherited":True,
            "credentials_never_transferred":True,
            "external_write_requires_local_authorization":True,
        },
    }
