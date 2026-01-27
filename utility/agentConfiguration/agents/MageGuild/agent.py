from base import AgentConfiguration
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    PromptAgentDefinition,
    OpenApiAgentTool,        
    OpenApiFunctionDefinition,
    OpenApiAnonymousAuthDetails,
    AgentVersionDetails
)
import os
import json
import logging

class MageGuildAgent(AgentConfiguration):

    async def configure(self,project_client:AIProjectClient,chat_completion_model:str) -> AgentVersionDetails:

        openapi_path = os.path.join(os.path.dirname(__file__), "openapi.json")
        with open(openapi_path, 'r') as f:
            openapi_spec = json.load(f)

        instruction_path = os.path.join(os.path.dirname(__file__), "instruction.txt")
        with open(instruction_path, 'r') as f:
            agent_instruction = f.read()

        server_url = os.getenv('MAGE_GUILD_SERVER_URL')
        if 'servers' in openapi_spec and len(openapi_spec['servers']) > 0:
            openapi_spec['servers'][0]['url'] = server_url

        # For demo in prod never use anonymous
        auth = OpenApiAnonymousAuthDetails()

        # Initialize the main OpenAPI tool definition for weather
        openapi_tool = OpenApiAgentTool(
            openapi=OpenApiFunctionDefinition(
                name="MageGuild",
                spec=openapi_spec, 
                description="Embark into MageGuild quest", 
                auth=auth  
            )
            # spec=openapi_spec, description="Embark into MageGuild quest", auth=auth
        )        
        
        definition = PromptAgentDefinition(
            model=chat_completion_model,
            instructions=agent_instruction,
            tools=[openapi_tool]          
        )

        agent = project_client.agents.create_version("MageGuildAgent",definition=definition)

        return agent