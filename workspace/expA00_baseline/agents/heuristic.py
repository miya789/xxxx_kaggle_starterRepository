"""Rule-based baseline agent for PTCG AI Battle Challenge.

I/O contract:
  obs_dict : dict — game state provided by the cabt engine each turn.
             Keys are engine-specific; inspect obs_dict.keys() once the SDK is
             installed. Likely candidates for legal actions:
               obs_dict["availableActions"]  — list of action dicts or indices
               obs_dict["legalActions"]      — alternative key name
  return   : list[int] — indices of chosen action(s) from the legal action list.
             Return exactly what the engine expects; an empty list may mean
             "pass" depending on the engine spec.

Strategy (Phase 1 — first-action baseline):
  Select the first available legal action (index 0). This beats "crash" and
  gives a floor to measure improvements against. Replace this logic once the
  obs_dict structure is confirmed from the SDK.

IMPORTANT: never print/log inside this function. stdout/stderr inside agent()
  pollutes the scoring environment's log.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# obs_dict helpers
# ---------------------------------------------------------------------------
_LEGAL_ACTION_KEYS = ("availableActions", "legalActions", "available_actions", "legal_actions")


def get_legal_actions(obs_dict: Dict[str, Any]) -> Optional[List[Any]]:
    """Return the legal-action list from obs_dict, trying known key names."""
    for key in _LEGAL_ACTION_KEYS:
        if key in obs_dict:
            actions = obs_dict[key]
            if actions:
                return list(actions)
    return None


# ---------------------------------------------------------------------------
# Agent
# ---------------------------------------------------------------------------
def heuristic_agent(obs_dict: Dict[str, Any]) -> List[int]:
    """Return a list of action indices. Phase-1 strategy: pick the first legal action.

    Falls back to [0] if the legal-action list cannot be located in obs_dict,
    so the agent never crashes (required by competition rules).
    """
    actions = get_legal_actions(obs_dict)
    if actions is None:
        # Unknown obs_dict structure — return index 0 as a safe fallback.
        # Update once the engine SDK is confirmed.
        return [0]

    # Phase 1: deterministically pick the first legal action.
    # TODO(Phase 2): replace with a real heuristic once obs_dict keys are known.
    return [0]
