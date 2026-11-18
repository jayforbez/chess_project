"""One registry so the GUI menu, the harness CLI and the tests list the same agents."""
from agents.agent_a_raider import RaiderAgent
from agents.agent_b_fortress import FortressAgent
from agents.reference_agent import ReferenceAgent

AGENT_REGISTRY = {
    "Raider": RaiderAgent,
    "Fortress": FortressAgent,
    "Reference": ReferenceAgent,
}
