from __future__ import annotations
import argparse, datetime, json
from pathlib import Path
from typing import Any
from .portable_crdt import PortableCRDT
from .interop_profiles import build_meaw_interop_profile
from .harum_anti_entropy import build_state_digest
from .capability_federation import sanitize_passport

def load(path:str|Path)->dict[str,Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))

def build_bundle(
    *,
    actor_id:str,
    canonical_commit:str,
    panel:dict[str,Any],
    jev:dict[str,Any],
    project_tree:dict[str,Any],
    capability_registry:dict[str,Any],
    a2a_endpoint:str|None=None,
    documentation_url:str|None=None,
    instance_passport:dict[str,Any]|None=None,
)->dict[str,Any]:
    if not actor_id: raise ValueError("actor_id required")
    if not canonical_commit: raise ValueError("canonical_commit required")
    crdt=PortableCRDT(actor_id)
    focus=panel.get("current_focus",{})
    crdt.set("focus.project",focus.get("project"))
    crdt.set("focus.next_layer",focus.get("next_layer"))
    checkpoint=(jev.get("checkpoint") or {}).get("event_id")
    if checkpoint: crdt.set("checkpoint.event_id",checkpoint)
    for w in jev.get("open_work",[]):
        if w.get("work_id"): crdt.add("open_work",w["work_id"])
    for r in jev.get("open_help_requests",[]):
        if r.get("request_id"): crdt.add("open_help",r["request_id"])
    event_heads=[x for x in [jev.get("last_event"),checkpoint] if x]
    crdt_state=crdt.export()
    state_digest=build_state_digest(
      panel=panel,jev=jev,project_tree=project_tree,capability_registry=capability_registry,
      crdt_state=crdt_state,canonical_commit=canonical_commit,event_heads=event_heads,
    )
    return {
      "schema":"harum.federation-bundle/v1",
      "created_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),
      "actor_id":actor_id,
      "canonical_commit":canonical_commit,
      "jev_view":jev,
      "project_tree":project_tree,
      "capability_registry":capability_registry,
      "crdt_state":crdt_state,
      "state_digest":state_digest,
      "instance_passport":sanitize_passport(instance_passport) if instance_passport else None,
      "interop_profile":build_meaw_interop_profile(
        actor_id=actor_id,current_focus=focus,capability_registry=capability_registry,
        a2a_endpoint=a2a_endpoint,documentation_url=documentation_url,
      ),
      "content_refs":[],
      "event_heads":event_heads,
      "notes":[
        "No credentials or hidden chain-of-thought included.",
        "Invalidate inherited leases before joining.",
        "Reconcile live external state before any write.",
        "Interop descriptors are descriptive-only and do not grant permission."
      ]
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--actor-id",required=True)
    p.add_argument("--canonical-commit",required=True)
    p.add_argument("--panel",default="systems/harum_instance_panel.json")
    p.add_argument("--jev",default=".harum-assembly/jev_view.json")
    p.add_argument("--tree",default="systems/harum_project_tree.json")
    p.add_argument("--registry",default="systems/harum_capability_registry.json")
    p.add_argument("--out",default="state/coordination/federation_bundle.json")
    p.add_argument("--a2a-endpoint")
    p.add_argument("--documentation-url")
    p.add_argument("--passport")
    a=p.parse_args()
    bundle=build_bundle(
      actor_id=a.actor_id,canonical_commit=a.canonical_commit,
      panel=load(a.panel),jev=load(a.jev),
      project_tree=load(a.tree),capability_registry=load(a.registry),
      a2a_endpoint=a.a2a_endpoint,documentation_url=a.documentation_url,
      instance_passport=load(a.passport) if a.passport else None,
    )
    Path(a.out).parent.mkdir(parents=True,exist_ok=True)
    Path(a.out).write_text(json.dumps(bundle,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
      "schema":bundle["schema"],"actor_id":bundle["actor_id"],"event_heads":bundle["event_heads"],
      "a2a_enabled":bundle["interop_profile"]["a2a"] is not None
    },ensure_ascii=False))

if __name__=="__main__":
    main()
