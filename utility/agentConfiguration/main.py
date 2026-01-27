from azure.identity import AzureCliCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import AgentVersionDetails
from dotenv import load_dotenv
from pathlib import Path
from base import AgentConfiguration
from typing import List
import os
import importlib
import inspect
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

def discover_agents() -> List[AgentConfiguration]:
    """Discover all agent implementations in the agents directory."""
    agents_dir = Path(__file__).parent / "agents"
    agent_classes = []
    
    # Iterate through subdirectories in agents folder
    for subdir in agents_dir.iterdir():
        if subdir.is_dir() and not subdir.name.startswith('__'):
            agent_file = subdir / "agent.py"
            if agent_file.exists():
                # Construct module path: agents.MageGuild.agent
                module_path = f"agents.{subdir.name}.agent"
                try:
                    # Import the module
                    module = importlib.import_module(module_path)
                    
                    # Find all classes that inherit from AgentConfiguration
                    for name, obj in inspect.getmembers(module, inspect.isclass):
                        if (issubclass(obj, AgentConfiguration) and 
                            obj is not AgentConfiguration):
                            agent_classes.append(obj)
                except Exception as e:
                    print(f"Error loading agent from {module_path}: {e}")
    
    return agent_classes

async def main():

    load_dotenv(override=True)

    project = AIProjectClient(
        endpoint=os.getenv('AZURE_AI_FOUNDRY_ENDPOINT'),
        credential=AzureCliCredential()
    )
    
    agents = discover_agents()

    chat_completion_model = os.getenv('AZURE_OPENAI_CHAT_MODEL_COMPLETION')
    
    created_agents:List[AgentVersionDetails] = []

    for agent_class in agents:
        try:
            agent = agent_class()
            print(f"Configuring {agent_class.__name__}")
            created_agent = await agent.configure(project,chat_completion_model)
            created_agents.append(created_agent)
        except Exception as e:
            print(f"Error configuring {agent_class.__name__}")
            print(f"Exception: {e}")

    for a in created_agents:
        logging.info(f"Agent {a.name} version {a.version} created")


if __name__ == "__main__":
    asyncio.run(main())
