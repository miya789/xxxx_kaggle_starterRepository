"""Frozen opponent v1 — self-contained PTCG first-action baseline.

This is a FROZEN copy of agents/heuristic.py (Phase 1) inlined with no
package imports. Part of the opponent pool (the simulation-competition analogue
of a fold definition): once frozen it must not change, so win-rates against it
stay comparable over time. See opponents/README.md.

Exposes ``agent(obs_dict: dict) -> list[int]`` (PTCG interface).
Never print/log inside ``agent``.

Logic: picks the first available legal action (index 0). Deterministic.
"""

from __future__ import annotations

from typing import Any, Dict, List

_LEGAL_ACTION_KEYS = ("availableActions", "legalActions", "available_actions", "legal_actions")


def agent(obs_dict: Dict[str, Any]) -> List[int]:
    for key in _LEGAL_ACTION_KEYS:
        if key in obs_dict:
            actions = obs_dict[key]
            if actions:
                return [0]
    return [0]
