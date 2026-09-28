from __future__ import annotations

import hashlib
import json
import time
import uuid
from dataclasses import dataclass, asdict
from typing import Any, Iterable


KINDS={"register-set","register-delete","set-add","set-remove"}


def canonical(value: Any) -> str:
    return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class Operation:
    op_id: str
    actor: str
    seq: int
    lamport: int
    kind: str
    path: str
    value: Any = None
    observed_tags: tuple[str,...] = ()
    created_at: float = 0.0
    integrity: str = ""

    def payload_without_integrity(self)->dict:
        row=asdict(self)
        row.pop("integrity",None)
        row["observed_tags"]=list(self.observed_tags)
        return row

    def valid(self)->bool:
        return bool(self.op_id and self.actor and self.path and self.kind in KINDS and self.integrity==digest(self.payload_without_integrity()))


class PortableCRDT:
    def __init__(self,actor: str):
        if not actor: raise ValueError("actor required")
        self.actor=actor
        self.seq=0
        self.lamport=0
        self._ops: dict[str,Operation]={}

    def _emit(self,kind:str,path:str,*,value:Any=None,observed_tags:Iterable[str]=())->Operation:
        if kind not in KINDS: raise ValueError(kind)
        if not path: raise ValueError("path required")
        self.seq+=1;self.lamport+=1
        base={
          "op_id":uuid.uuid4().hex,"actor":self.actor,"seq":self.seq,"lamport":self.lamport,
          "kind":kind,"path":path,"value":value,"observed_tags":list(observed_tags),"created_at":time.time()
        }
        op=Operation(**{**base,"observed_tags":tuple(base["observed_tags"]),"integrity":digest(base)})
        self._ops[op.op_id]=op
        return op

    def set(self,path:str,value:Any)->Operation:
        return self._emit("register-set",path,value=value)

    def delete(self,path:str)->Operation:
        return self._emit("register-delete",path)

    def add(self,path:str,value:Any)->Operation:
        return self._emit("set-add",path,value=value)

    def remove(self,path:str,value:Any)->Operation:
        target=digest(value)
        tags=[
          op.op_id for op in self._ops.values()
          if op.kind=="set-add" and op.path==path and digest(op.value)==target
        ]
        return self._emit("set-remove",path,value={"value_hash":target},observed_tags=tags)

    def ingest(self,op:Operation|dict)->bool:
        if isinstance(op,dict):
            row=dict(op)
            row["observed_tags"]=tuple(row.get("observed_tags") or ())
            op=Operation(**row)
        if not op.valid(): raise ValueError("invalid operation integrity")
        if op.op_id in self._ops:return False
        self._ops[op.op_id]=op
        self.lamport=max(self.lamport,int(op.lamport))+1
        return True

    def merge(self,other:"PortableCRDT")->int:
        count=0
        for op in other.operations():
            count+=1 if self.ingest(asdict(op)) else 0
        return count

    def operations(self)->list[Operation]:
        return sorted(self._ops.values(),key=lambda o:(o.lamport,o.actor,o.op_id))

    def materialize(self)->dict:
        registers={}
        reg_winner={}
        adds:dict[str,dict[str,tuple[Any,set[str]]]]={}
        removed:set[str]=set()

        for op in self.operations():
            if op.kind in {"register-set","register-delete"}:
                order=(op.lamport,op.actor,op.op_id)
                if order>reg_winner.get(op.path,(-1,"","")):
                    reg_winner[op.path]=order
                    registers[op.path]=None if op.kind=="register-delete" else op.value
            elif op.kind=="set-add":
                vh=digest(op.value)
                adds.setdefault(op.path,{})
                if vh not in adds[op.path]:adds[op.path][vh]=(op.value,set())
                adds[op.path][vh][1].add(op.op_id)
            elif op.kind=="set-remove":
                removed.update(op.observed_tags)

        state={"registers":{},"sets":{}}
        for path,value in registers.items():
            if value is not None:state["registers"][path]=value
        for path,by_hash in adds.items():
            values=[]
            for _,(value,tags) in sorted(by_hash.items()):
                if any(tag not in removed for tag in tags):values.append(value)
            state["sets"][path]=values
        return state

    def export(self)->dict:
        ops=[]
        for op in self.operations():
            row=asdict(op);row["observed_tags"]=list(op.observed_tags);ops.append(row)
        payload={"schema":"meaw.portable-crdt-state/v1","actor":self.actor,"lamport":self.lamport,"operations":ops}
        payload["root_sha256"]=digest(payload)
        return payload

    @classmethod
    def restore(cls,payload:dict,actor:str)->"PortableCRDT":
        clone=dict(payload);expected=clone.pop("root_sha256","")
        if expected!=digest(clone):raise ValueError("CRDT root hash mismatch")
        crdt=cls(actor)
        for row in clone.get("operations",[]):crdt.ingest(row)
        return crdt
