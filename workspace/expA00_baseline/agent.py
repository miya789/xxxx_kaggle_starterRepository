"""Development entrypoint for the PTCG AI Battle Challenge agent.

Selects a policy at import time and exposes ``agent(obs_dict)``
which the cabt engine calls to obtain a list of action indices.

This module imports from the ``agents`` package, so it is NOT self-contained —
use it for local development / evaluation only. For the actual Kaggle submission,
use ``submit_agent.py`` which inlines everything into one self-contained file.

Switch the policy with the ``POLICY`` constant below, or by overriding the
``SIM_POLICY`` environment variable.

NOTE: ``agent()`` must never print/log — stdout inside the agent pollutes the
scoring environment's log.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List

from agents.heuristic import heuristic_agent

# --- Policy selection (edit here) ------------------------------------------
POLICY = "heuristic"   # "heuristic" (Phase 1); add "search" etc. in later phases

POLICY = os.environ.get("SIM_POLICY", POLICY)


def agent(obs_dict: Dict[str, Any]) -> List[int]:
    """Return a list of action indices for the current game state."""
    if POLICY == "heuristic":
        return heuristic_agent(obs_dict)
    raise ValueError(f"unknown POLICY: {POLICY!r} (expected 'heuristic')")
