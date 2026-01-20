from azure.identity import DefaultAzureCredential
from agent_framework.azure import AzureOpenAIResponsesClient
from config import Config
from typing import AsyncGenerator, Any
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

    async def get_lore_information(self,question:str) -> AsyncGenerator[str, None]:

        complete_response = ""
        async for chunk in self.agent.get_streaming_response(question):
            if chunk.text:
                complete_response += chunk.text
                yield chunk.text
