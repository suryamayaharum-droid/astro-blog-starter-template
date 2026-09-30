from __future__ import annotations

from typing import Any, Mapping


REQUIRED_PROJECTIONS=(
    "dispatch",
    "health",
    "meta",
    "capsule",
    "capability_board",
)


def assess_projection_freshness(
    *,
    jev: Mapping[str,Any],
    projections: Mapping[str,Mapping[str,Any] | None],
) -> dict[str,Any]:
    """Compare derived projection watermarks with the canonical JEV event.

    This helper is deliberately read-only. It never refreshes projections and
    never grants write permission; callers may use it to fail closed until a
    canonical sync has regenerated derived state.
    """
    current=jev.get("last_event")
    rows={}
    stale=[]
    missing=[]

    for name in REQUIRED_PROJECTIONS:
        value=projections.get(name) or {}
        source=value.get("source_last_event")
        rows[name]={"source_last_event":source}
        if current is None:
            if source is not None:
                stale.append(name)
        elif source is None:
            missing.append(name)
        elif source!=current:
            stale.append(name)

    fresh=not stale and not missing
    return {
        "schema":"harum.projection-freshness/v1",
        "fresh":fresh,
        "current_jev_event":current,
        "projections":rows,
        "stale":sorted(stale),
        "missing_watermark":sorted(missing),
        "action":"continue" if fresh else "run-harum-coord-sync",
    }
