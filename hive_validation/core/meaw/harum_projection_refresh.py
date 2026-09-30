from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any

from core.meaw.harum_dispatcher import build_dispatch_plan
from core.meaw.harum_coordination_doctor import diagnose
from core.meaw.harum_context_capsule import build_capsule
from core.meaw.harum_meta_coordinator import build_meta_plan
from core.meaw.capability_board import build_capability_board
from core.meaw.harum_projection_freshness import projection_generator_fingerprint

def load(path: str) -> dict[str,Any]:
    p=Path(path)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}

def write(path: str, value: dict[str,Any]) -> None:
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

def refresh(
    *,
    jev:dict[str,Any],tree:dict[str,Any],registry:dict[str,Any],leases:dict[str,Any],
    policy:dict[str,Any],panel:dict[str,Any],bootstrap:dict[str,Any],
    assembly_state:dict[str,Any],validation:dict[str,Any],meta_policy:dict[str,Any]|None=None,
    persisted_passports:list[dict[str,Any]]|None=None,
)->dict[str,Any]:
    generator_fingerprint=projection_generator_fingerprint()
    dispatch=build_dispatch_plan(
        jev=jev,tree=tree,registry=registry,leases=leases,policy=policy,
        instance_state=assembly_state or None,
    )
    health=diagnose(
        panel=panel,jev=jev,tree=tree,registry=registry,leases=leases,bootstrap=bootstrap,
        assembly_state=assembly_state or None,dispatch_plan=dispatch,dispatch_policy=policy,
    )
    meta=build_meta_plan(dispatch=dispatch,tree=tree,health=health,jev=jev,policy=meta_policy or {})
    board=build_capability_board(
        assembly_state=assembly_state or {},dispatch=dispatch,registry=registry,
        persisted_passports=persisted_passports or [],
    )
    capsule=build_capsule(
        panel=panel,jev=jev,dispatch=dispatch,health=health,validation=validation,
        meta=meta,generator_fingerprint=generator_fingerprint,
    )
    source_last_event=jev.get("last_event")
    for projection in (dispatch,health,meta,board):
        projection["source_last_event"]=source_last_event
        projection["source_generator_fingerprint"]=generator_fingerprint
    return {"dispatch":dispatch,"health":health,"meta":meta,"capsule":capsule,"capability_board":board}

def main():
    p=argparse.ArgumentParser(description="Refresh all derived HARUM coordination projections atomically.")
    p.add_argument("--jev",default=".harum-assembly/jev_view.json")
    p.add_argument("--state",default=".harum-assembly/state.json")
    p.add_argument("--tree",default="systems/harum_project_tree.json")
    p.add_argument("--registry",default="systems/harum_capability_registry.json")
    p.add_argument("--leases",default="state/coordination/work_leases.json")
    p.add_argument("--policy",default="systems/harum_dispatch_policy.json")
    p.add_argument("--panel",default="systems/harum_instance_panel.json")
    p.add_argument("--bootstrap",default="systems/harum_bootstrap_manifest.json")
    p.add_argument("--validation",default="state/coordination/validation.json")
    p.add_argument("--dispatch-out",default="state/coordination/dispatch_plan.json")
    p.add_argument("--health-out",default="state/coordination/health.json")
    p.add_argument("--capsule-out",default="state/coordination/context_capsule.json")
    p.add_argument("--meta-policy",default="systems/harum_meta_coordination.json")
    p.add_argument("--meta-out",default="state/coordination/meta_plan.json")
    p.add_argument("--passports",default="state/coordination/instance_passports.json")
    p.add_argument("--capability-board-out",default="state/coordination/capability_board.json")
    a=p.parse_args()
    result=refresh(
        jev=load(a.jev),tree=load(a.tree),registry=load(a.registry),leases=load(a.leases),
        policy=load(a.policy),panel=load(a.panel),bootstrap=load(a.bootstrap),
        assembly_state=load(a.state),validation=load(a.validation),meta_policy=load(a.meta_policy),
        persisted_passports=(load(a.passports).get("passports",[]) if Path(a.passports).exists() else []),
    )
    write(a.dispatch_out,result["dispatch"])
    write(a.health_out,result["health"])
    write(a.meta_out,result["meta"])
    write(a.capsule_out,result["capsule"])
    write(a.capability_board_out,result["capability_board"])
    print(json.dumps({
      "dispatch_summary":result["dispatch"].get("summary",{}),
      "health":result["health"].get("status"),
      "primary_move":(result["meta"].get("primary_move") or {}).get("work_id"),
      "capsule_sha256":result["capsule"].get("content_sha256"),
      "capability_board":result["capability_board"].get("summary",{}),
      "generator_fingerprint":result["dispatch"].get("source_generator_fingerprint"),
    },ensure_ascii=False))

if __name__=="__main__":
    main()
