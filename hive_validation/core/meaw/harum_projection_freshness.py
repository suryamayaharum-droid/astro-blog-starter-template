from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any, Mapping


REQUIRED_PROJECTIONS=(
    "dispatch",
    "health",
    "meta",
    "capsule",
    "capability_board",
)

GENERATOR_FILES=(
    "harum_projection_refresh.py",
    "harum_dispatcher.py",
    "harum_coordination_doctor.py",
    "harum_meta_coordinator.py",
    "harum_context_capsule.py",
    "capability_board.py",
    "capability_federation.py",
    "harum_work_intent.py",
)


def projection_generator_fingerprint(base_dir: str | Path | None=None) -> str:
    """Hash the code that materially generates coordination projections."""
    base=Path(base_dir).resolve() if base_dir is not None else Path(__file__).resolve().parent
    digest=hashlib.sha256()
    for name in GENERATOR_FILES:
        path=base/name
        if not path.exists():
            raise FileNotFoundError(f"projection generator source missing: {path}")
        digest.update(name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def assess_projection_freshness(
    *,
    jev: Mapping[str,Any],
    projections: Mapping[str,Mapping[str,Any] | None],
    expected_generator_fingerprint: str | None=None,
) -> dict[str,Any]:
    """Compare derived projection event and generator watermarks.

    This helper is deliberately read-only. It never refreshes projections and
    never grants write permission; callers may use it to fail closed until a
    canonical sync has regenerated derived state.
    """
    current=jev.get("last_event")
    rows={}
    stale=[]
    missing=[]
    stale_generator=[]
    missing_generator=[]

    initial_empty=current is None and all(not (projections.get(name) or {}) for name in REQUIRED_PROJECTIONS)

    for name in REQUIRED_PROJECTIONS:
        value=projections.get(name) or {}
        source=value.get("source_last_event")
        generator=value.get("source_generator_fingerprint")
        rows[name]={
            "source_last_event":source,
            "source_generator_fingerprint":generator,
        }
        if current is None:
            if source is not None:
                stale.append(name)
        elif source is None:
            missing.append(name)
        elif source!=current:
            stale.append(name)

        if expected_generator_fingerprint is not None and not initial_empty:
            if generator is None:
                missing_generator.append(name)
            elif generator!=expected_generator_fingerprint:
                stale_generator.append(name)

    fresh=not stale and not missing and not stale_generator and not missing_generator
    return {
        "schema":"harum.projection-freshness/v2",
        "fresh":fresh,
        "current_jev_event":current,
        "expected_generator_fingerprint":expected_generator_fingerprint,
        "projections":rows,
        "stale":sorted(stale),
        "missing_watermark":sorted(missing),
        "stale_generator":sorted(stale_generator),
        "missing_generator_fingerprint":sorted(missing_generator),
        "action":"continue" if fresh else "run-harum-coord-sync",
    }
