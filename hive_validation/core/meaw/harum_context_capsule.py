from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from typing import Any

def _load(path: str) -> dict[str,Any]:
    p=Path(path)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}

def canonical(value: Any) -> str:
    return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"))

def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()

def _available(dispatch: dict[str,Any]) -> list[dict[str,Any]]:
    rows=[x for x in dispatch.get("assignments",[]) if x.get("state")=="available"]
    rows.sort(key=lambda x:(-int(x.get("priority",50) or 50),x.get("work_id","")))
    return [{
        "work_id":x.get("work_id"),
        "priority":x.get("priority"),
        "candidate_roles":x.get("candidate_roles",[]),
        "candidate_instances":x.get("candidate_instances",[]),
        "reason":x.get("reason"),
    } for x in rows[:5]]

def _open_help(jev: dict[str,Any]) -> list[dict[str,Any]]:
    rows=[]
    for x in jev.get("open_help_requests",[]) or []:
        rows.append({
            "request_id":x.get("request_id"),
            "work_id":x.get("work_id"),
            "target_role":x.get("target_role"),
            "question":x.get("question"),
        })
    return rows[:6]

def build_capsule(*,panel:dict[str,Any],jev:dict[str,Any],dispatch:dict[str,Any],health:dict[str,Any],validation:dict[str,Any],meta:dict[str,Any]|None=None) -> dict[str,Any]:
    focus=panel.get("current_focus",{}) or {}
    public=panel.get("public_web",{}) or {}
    body={
      "schema":"harum.context-capsule/v1",
      "source_last_event":jev.get("last_event"),
      "focus":{
        "project":focus.get("project"),
        "internal_name":focus.get("internal_name"),
        "rule":focus.get("rule"),
        "next_layer":focus.get("next_layer"),
      },
      "health":{
        "status":health.get("status"),
        "issues":(health.get("counts",{}) or {}).get("issues",0),
        "warnings":(health.get("counts",{}) or {}).get("warnings",0),
        "next_safe_action":health.get("next_safe_action"),
      },
      "checkpoint":jev.get("checkpoint"),
      "available_work":_available(dispatch),
      "open_help":_open_help(jev),
      "dispatch_summary":dispatch.get("summary",{}),
      "meta_advice":{
        "mode":(meta or {}).get("mode"),
        "primary_move":(meta or {}).get("primary_move"),
        "primary_recovery":(meta or {}).get("primary_recovery"),
        "recovery_queue":(meta or {}).get("recovery_queue",[]),
        "parallel_wave":(meta or {}).get("parallel_wave",[]),
        "coordination_budget":(meta or {}).get("coordination_budget",{}),
      },
      "public_web":{
        "github_pages":(public.get("github_pages",{}) or {}).get("url"),
        "vercel":(public.get("vercel",{}) or {}).get("url"),
        "atlas":public.get("atlas",{}),
      },
      "validation":validation.get("components",{}),
      "expand":{
        "full_jev":".harum-assembly/jev_view.json",
        "project_tree":"systems/harum_project_tree.json",
        "dispatch":"state/coordination/dispatch_plan.json",
        "health":"state/coordination/health.json",
        "meta_plan":"state/coordination/meta_plan.json",
        "capabilities":"systems/harum_capability_registry.json",
        "checkpoint":"docs/HARUMVERSO_CHECKPOINT.md",
        "global_continuity":"docs/GLOBAL_CONTINUITY_INSTRUCTION.md",
      },
      "rules":{
        "read_capsule_first":True,
        "canonical_files_override_capsule":True,
        "live_external_state_overrides_repo":True,
        "no_hidden_chain_of_thought":True,
        "no_secrets":True,
        "claim_before_execution":True,
      },
    }
    body["content_sha256"]=digest(body)
    return body

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--panel",default="systems/harum_instance_panel.json")
    p.add_argument("--jev",default=".harum-assembly/jev_view.json")
    p.add_argument("--dispatch",default="state/coordination/dispatch_plan.json")
    p.add_argument("--health",default="state/coordination/health.json")
    p.add_argument("--validation",default="state/coordination/validation.json")
    p.add_argument("--meta",default="state/coordination/meta_plan.json")
    p.add_argument("--out",default="state/coordination/context_capsule.json")
    a=p.parse_args()
    capsule=build_capsule(
      panel=_load(a.panel),jev=_load(a.jev),dispatch=_load(a.dispatch),
      health=_load(a.health),validation=_load(a.validation),meta=_load(a.meta)
    )
    out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(capsule,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(capsule,ensure_ascii=False))

if __name__=="__main__":
    main()
