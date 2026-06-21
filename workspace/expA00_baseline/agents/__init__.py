"""Policy agents for PTCG AI Battle Challenge.

Each agent exposes ``*_agent(obs_dict: dict) -> list[int]`` that returns
a list of action indices. Agents are deterministic for reproducibility.

NOTE: nothing in this package may ``print`` or ``logging`` inside the move
function — the scoring environment captures stdout/stderr and noise there
can break an episode. Logging belongs in ``evaluate.py`` only.
"""

from .heuristic import heuristic_agent

__all__ = ["heuristic_agent"]
