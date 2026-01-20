from azure.identity import DefaultAzureCredential
from agent_framework.azure import AzureOpenAIChatClient
from config import Config
import logging

class LoreAgentService:

    def __init__(self,config:Config):
        self.agent = AzureOpenAIChatClient(
            endpoint=config.azure_openai_endpoint,
            instruction_role="You are a joke assistant",
            credential=DefaultAzureCredential(),
            name="loreAgent"
        )
        self.logger = logging.getLogger(__name__)

    async def get_lore_information(self,question:str) -> str:
        result = await self.agent.run(question)
        return result.text
