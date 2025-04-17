# dispatcher.py

import os
import importlib
from pathlib import Path
from core.messages import MCPMessage

AGENTS = {}

def register_agent(name: str, instance):
    print(f"✅ 註冊 Agent：{name}")
    AGENTS[name] = instance

def auto_load_agents():
    agents_path = Path(__file__).parent / "agents"
    for file in os.listdir(agents_path):
        if file.endswith("_agent.py") and not file.startswith("__"):
            module_name = f"mcp_server.agents.{file[:-3]}"
            importlib.import_module(module_name)

# ✅ 在這裡載入 Agent modules（會觸發它們內部的 register）
auto_load_agents()

def dispatch(mcp_message: MCPMessage):
    agent = AGENTS.get(mcp_message.receiver)
    if not agent:
        return {"error": f"Agent not found: {mcp_message.receiver}"}
    return agent.handle(mcp_message)
