from base import AgentConfiguration
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    PromptAgentDefinition,
    OpenApiAgentTool,
    OpenApiFunctionDefinition,
    OpenApiAnonymousAuthDetails,
)

class MageGuildAgent(AgentConfiguration):

    async def configure(self,project_client:AIProjectClient,chat_completion_model:str):

        definition = PromptAgentDefinition(
            model=chat_completion_model,
            instructions='You are an agent that tell joke, you are funny'            
        )

        agent = project_client.agents.create_version("testAgent",definition=definition)