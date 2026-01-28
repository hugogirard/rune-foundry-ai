from base import AgentConfiguration
from azure.ai.projects.models import (
    PromptAgentDefinition,
    OpenApiAgentTool,        
    OpenApiFunctionDefinition,
    OpenApiAnonymousAuthDetails,
    AgentVersionDetails
)
import os
import json

class MageGuildAgent(AgentConfiguration):

    async def configure(self) -> AgentVersionDetails:

        chat_completion_model = os.getenv('AZURE_OPENAI_CHAT_MODEL_COMPLETION')

        openapi_path = os.path.join(os.path.dirname(__file__), "openapi.json")
        with open(openapi_path, 'r') as f:
            openapi_spec = json.load(f)

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
        )        
        
        return self.create_agent(agent_name="MageGuildAgent",                          
                                 agent_description="Embark into quest on the MageGuild",
                                 chat_completion_model=chat_completion_model,
                                 tools=[openapi_tool])