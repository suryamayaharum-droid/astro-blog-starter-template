from __future__ import annotations

import re
from typing import Any, Iterable
from urllib.parse import urlparse

A2A_PROTOCOL_VERSION = "1.0"
MCP_PROTOCOL_VERSION = "2026-07-28"
_ALLOWED_BINDINGS = {"JSONRPC", "HTTP+JSON", "GRPC"}


def _slug(value: str) -> str:
    text = re.sub(r"[^A-Za-z0-9._-]+", "-", (value or "").strip()).strip("-._")
    if not text:
        raise ValueError("non-empty identifier required")
    return text[:128]


def _https_or_local(endpoint: str) -> bool:
    parsed = urlparse(endpoint)
    if parsed.scheme == "https" and parsed.netloc:
        return True
    if parsed.scheme == "http" and parsed.hostname in {"localhost", "127.0.0.1", "::1"}:
        return True
    return False


def _selected_roles(capability_registry: dict[str, Any], roles: Iterable[str] | None) -> list[dict[str, Any]]:
    available = [r for r in capability_registry.get("roles", []) if isinstance(r, dict) and r.get("role")]
    if roles is None:
        return available
    wanted = set(roles)
    return [r for r in available if r.get("role") in wanted]


def build_a2a_agent_card(
    *,
    name: str,
    description: str,
    version: str,
    endpoint: str,
    capability_registry: dict[str, Any],
    roles: Iterable[str] | None = None,
    protocol_binding: str = "HTTP+JSON",
    documentation_url: str | None = None,
) -> dict[str, Any]:
    """Build a conservative A2A v1.0 Agent Card descriptor.

    This advertises only metadata already present in the capability registry.
    It does not start a server, grant permissions, or prove endpoint ownership.
    """
    if protocol_binding not in _ALLOWED_BINDINGS:
        raise ValueError(f"unsupported A2A binding: {protocol_binding}")
    if protocol_binding in {"JSONRPC", "HTTP+JSON"} and not _https_or_local(endpoint):
        raise ValueError("A2A HTTP endpoint must use HTTPS in production or loopback HTTP locally")
    if not name.strip() or not description.strip() or not version.strip():
        raise ValueError("name, description and version are required")
    if documentation_url and not _https_or_local(documentation_url):
        raise ValueError("documentation_url must use HTTPS or loopback HTTP")

    selected = _selected_roles(capability_registry, roles)
    skills: list[dict[str, Any]] = []
    for row in selected:
        role = str(row["role"])
        capabilities = [str(x) for x in row.get("capabilities", []) if str(x).strip()]
        limits = [str(x) for x in row.get("limits", []) if str(x).strip()]
        details = f"Declared capabilities: {', '.join(capabilities) if capabilities else 'none'}."
        if limits:
            details += f" Limits: {', '.join(limits)}."
        skills.append({
            "id": _slug(role),
            "name": role.replace("-", " ").title(),
            "description": details,
            "tags": sorted(set(capabilities))[:24],
            "inputModes": ["text/plain", "application/json"],
            "outputModes": ["text/plain", "application/json"],
        })

    card: dict[str, Any] = {
        "name": name.strip(),
        "description": description.strip(),
        "supportedInterfaces": [{
            "url": endpoint,
            "protocolBinding": protocol_binding,
            "protocolVersion": A2A_PROTOCOL_VERSION,
        }],
        "version": version.strip(),
        "capabilities": {
            "streaming": False,
            "pushNotifications": False,
            "extendedAgentCard": False,
        },
        "defaultInputModes": ["text/plain", "application/json"],
        "defaultOutputModes": ["text/plain", "application/json"],
        "skills": skills,
    }
    if documentation_url:
        card["documentationUrl"] = documentation_url
    return card


def build_mcp_discovery_template(
    *,
    server_name: str,
    server_version: str,
    instructions: str,
    tools: bool = False,
    resources: bool = True,
    prompts: bool = False,
    experimental: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Build the result payload shape for MCP 2026-07-28 server/discover.

    This is a descriptor template only. An actual MCP server must still
    implement protocol handling, auth, and per-request capability negotiation.
    """
    if not server_name.strip() or not server_version.strip():
        raise ValueError("server_name and server_version are required")
    capabilities: dict[str, Any] = {}
    if tools:
        capabilities["tools"] = {}
    if resources:
        capabilities["resources"] = {}
    if prompts:
        capabilities["prompts"] = {}
    if experimental:
        capabilities["experimental"] = experimental

    return {
        "resultType": "complete",
        "supportedVersions": [MCP_PROTOCOL_VERSION],
        "capabilities": capabilities,
        "instructions": instructions.strip(),
        "_meta": {
            "io.modelcontextprotocol/serverInfo": {
                "name": server_name.strip(),
                "version": server_version.strip(),
                "description": "MEAW/HARUM provider-neutral interoperability descriptor",
            }
        },
    }


def build_meaw_interop_profile(
    *,
    actor_id: str,
    current_focus: dict[str, Any],
    capability_registry: dict[str, Any],
    a2a_endpoint: str | None = None,
    documentation_url: str | None = None,
) -> dict[str, Any]:
    """Create a portable, non-authoritative interop profile for one MEAW peer."""
    if not actor_id.strip():
        raise ValueError("actor_id required")
    profile: dict[str, Any] = {
        "schema": "meaw.interop-profile/v1",
        "actor_id": actor_id.strip(),
        "authority": "descriptive-only",
        "focus": {
            "project": current_focus.get("project"),
            "next_layer": current_focus.get("next_layer"),
        },
        "mcp": build_mcp_discovery_template(
            server_name="meaw-harum-coordination",
            server_version="1.0",
            instructions=(
                "Expose only bounded coordination resources/capabilities. "
                "Live external writes remain separately permission-gated."
            ),
            resources=True,
            experimental={
                "org.harum/coordination": {
                    "authority": "advisory-only",
                    "canonicalMemory": "HIVE",
                    "hiddenReasoning": False,
                }
            },
        ),
        "a2a": None,
        "security": {
            "grants_permissions": False,
            "contains_credentials": False,
            "live_state_overrides_descriptor": True,
        },
    }
    if a2a_endpoint:
        profile["a2a"] = build_a2a_agent_card(
            name="MEAW HARUM Coordination Peer",
            description="Provider-neutral coordination peer for bounded HARUM/MEAW collaboration.",
            version="1.0",
            endpoint=a2a_endpoint,
            capability_registry=capability_registry,
            roles=[r.get("role") for r in capability_registry.get("roles", []) if r.get("role")],
            documentation_url=documentation_url,
        )
    return profile
