"""Self-contained PTCG AI Battle submission agent.

Source: workspace/expA00_baseline/agents/heuristic.py
Policy: first-action baseline (picks action index 0 deterministically)
Local win-rate (fill in from evaluate.py before submitting):
    vs random   : ____ / ____   (____%)
    vs frozen_v1: ____ / ____   (____%)

This file inlines everything so it has zero local imports and can be submitted
to Kaggle as ``main.py`` inside ``submission.tar.gz``.

Submission format:
    submission.tar.gz
    ├── main.py      ← rename this file to main.py when packaging
    ├── deck.csv     ← deck list (60 cards)
    └── cg/          ← cabt engine library (copy from datasets/cg/)

Package command (run from submit/v001_expA00_baseline/):
    tar -czvf submission.tar.gz main.py deck.csv cg/

HARD RULE: never print() or use logging inside agent() — the scoring
environment captures stdout/stderr and any output breaks the episode.
"""

from __future__ import annotations

from typing import Any, Dict, List

# ---------------------------------------------------------------------------
# Constants / hyperparameters (Phase 1 baseline — update in later phases)
# ---------------------------------------------------------------------------
_LEGAL_ACTION_KEYS = ("availableActions", "legalActions", "available_actions", "legal_actions")


# ---------------------------------------------------------------------------
# Agent (inline — no local imports)
# ---------------------------------------------------------------------------
def agent(obs_dict: Dict[str, Any]) -> List[int]:
    """Return a list of action indices for the current PTCG game state.

    Phase 1: picks the first available legal action deterministically.
    Never raises — competition rules require the agent to always return a valid
    response without crashing.
    """
    for key in _LEGAL_ACTION_KEYS:
        if key in obs_dict:
            actions = obs_dict[key]
            if actions:
                return [0]  # first legal action

    # Fallback: unknown obs_dict structure — return [0] and hope for the best.
    # Update once the cabt engine SDK is confirmed and obs_dict keys are known.
    return [0]
