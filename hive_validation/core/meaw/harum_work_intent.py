from __future__ import annotations
import hashlib, json, re
from typing import Any

_STOP={
  "the","a","an","and","or","of","to","for","in","on","with","from","by",
  "o","a","os","as","e","ou","de","da","do","das","dos","para","em","com","por",
  "audit","auditar","review","revisar","task","work","trabalho"
}

def _norm_text(value: Any) -> str:
    text=str(value or "").lower()
    text=re.sub(r"[^a-z0-9À-ÿ]+"," ",text)
    return " ".join(text.split())

def _tokens(value: Any) -> set[str]:
    return {t for t in _norm_text(value).split() if len(t)>2 and t not in _STOP}

def _uniq(values: Any) -> list[str]:
    return sorted({str(v).strip() for v in (values or []) if str(v).strip()})

def explicit_intent_key(node: dict[str,Any]) -> str|None:
    value=str(node.get("intent_key") or "").strip()
    return value or None

def work_signature(node: dict[str,Any], *, branch: str|None=None) -> str:
    explicit=explicit_intent_key(node)
    payload={
      "intent_key":explicit,
      "branch":branch,
      "title_tokens":sorted(_tokens(node.get("title"))),
      "target_role":node.get("target_role"),
      "required_capabilities":_uniq(node.get("required_capabilities")),
      "required_connectors":_uniq(node.get("required_connectors")),
      "required_skills":_uniq(node.get("required_skills")),
      "write_scope":_uniq(node.get("write_scope")),
    }
    raw=json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(",",":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

def similarity(left: dict[str,Any], right: dict[str,Any]) -> float:
    lt=_tokens(left.get("title")); rt=_tokens(right.get("title"))
    if not lt or not rt:
        return 0.0
    title=len(lt&rt)/len(lt|rt)
    role_bonus=0.12 if left.get("target_role") and left.get("target_role")==right.get("target_role") else 0.0
    lc=set(_uniq(left.get("required_capabilities"))); rc=set(_uniq(right.get("required_capabilities")))
    cap_bonus=0.08 if lc and rc and lc==rc else 0.0
    return min(1.0,title+role_bonus+cap_bonus)

def detect_intent_collisions(nodes: dict[str,dict[str,Any]], *, open_ids: set[str]|None=None, probable_threshold: float=0.82) -> dict[str,list[dict[str,Any]]]:
    ids=sorted(open_ids or set(nodes))
    hard=[]; probable=[]
    seen_keys={}
    for work_id in ids:
        node=nodes.get(work_id,{})
        key=explicit_intent_key(node)
        if key:
            if key in seen_keys:
                hard.append({"intent_key":key,"work_ids":[seen_keys[key],work_id]})
            else:
                seen_keys[key]=work_id
    for i,left_id in enumerate(ids):
        left=nodes.get(left_id,{})
        for right_id in ids[i+1:]:
            right=nodes.get(right_id,{})
            if explicit_intent_key(left) and explicit_intent_key(left)==explicit_intent_key(right):
                continue
            score=similarity(left,right)
            if score>=probable_threshold:
                probable.append({"work_ids":[left_id,right_id],"similarity":round(score,3)})
    return {"hard":hard,"probable":probable}

def canonical_duplicate_map(nodes: dict[str,dict[str,Any]], *, open_ids:set[str]) -> dict[str,str]:
    """Return duplicate->canonical for explicit intent_key collisions only."""
    groups={}
    for work_id in sorted(open_ids):
        node=nodes.get(work_id,{})
        key=explicit_intent_key(node)
        if key:
            groups.setdefault(key,[]).append(work_id)
    result={}
    for rows in groups.values():
        if len(rows)<2:
            continue
        rows=sorted(rows,key=lambda wid:(-int(nodes.get(wid,{}).get("priority",50) or 50),wid))
        canonical=rows[0]
        for dup in rows[1:]:
            result[dup]=canonical
    return result
