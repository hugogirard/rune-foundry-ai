from base import AgentConfiguration
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    PromptAgentDefinition,
    OpenApiAgentTool,
    OpenApiFunctionDefinition,
    OpenApiAnonymousAuthDetails,
)
import os
import json

class MageGuildAgent(AgentConfiguration):

    async def configure(self,project_client:AIProjectClient,chat_completion_model:str):

        openapi_path = os.path.join(os.path.dirname(__file__), "openapi.json")
        with open(openapi_path, 'r') as f:
            openapi_spec = json.load(f)

        definition = PromptAgentDefinition(
            model=chat_completion_model,
            instructions='You are an agent that tell joke, you are funny'            
        )

        agent = project_client.agents.create_version("testAgent",definition=definition)