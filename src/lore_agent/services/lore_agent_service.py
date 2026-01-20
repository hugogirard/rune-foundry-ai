from azure.identity import DefaultAzureCredential
from agent_framework.azure import AzureOpenAIResponsesClient
from config import Config
import logging

class LoreAgentService:

    def __init__(self,config:Config):
        self.agent = AzureOpenAIResponsesClient(
            endpoint=config.azure_openai_endpoint,
            deployment_name=config.openai_chat_deployment_name,
            api_version=config.azure_openai_version,
            instruction_role="You are a joke assistant",
            credential=DefaultAzureCredential()
        )                
        self.logger = logging.getLogger(__name__)

    async def get_lore_information(self,question:str) -> str:
        result = await self.agent.get_response(question)                
        return result.text
