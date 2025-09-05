# Switch between Single Agent and Multi-Agent patterns
# 
# For Single Agent Pattern (direct function tools):
# Uncomment the line below:
# from .agent import root_agent

# For Multi-Agent Pattern (LlmAgent with sub-agents):
# Uncomment the line below:
from .multi_agent_system import root_agent

# The root_agent will be automatically detected by ADK
__all__ = ["root_agent"]
