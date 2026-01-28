from abc import ABC, abstractmethod
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import AgentVersionDetails
from azure.identity import AzureCliCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import Tool
from dotenv import load_dotenv
from typing import final,List
from azure.ai.projects.models import (
    PromptAgentDefinition,
    AgentVersionDetails
)
import os

class AgentConfiguration(ABC):
    
    def __init__(self):

        instruction_path = os.path.join(os.path.dirname(__file__), "instruction.txt")
        
        if os.path.exists(instruction_path):        
            with open(instruction_path, 'r') as f:
                self.agent_instruction = f.read()        
        else:
            self.agent_instruction = ""

        load_dotenv(override=True)

        self.project_client = AIProjectClient(
            endpoint=os.getenv('AZURE_AI_FOUNDRY_ENDPOINT'),
            credential=AzureCliCredential()
        )            

    @abstractmethod
    async def configure(self) -> AgentVersionDetails:
        pass
    
    @final
    def create_agent(self,agent_name:str,agent_description:str,chat_completion_model:str,tools:List[Tool]) -> AgentVersionDetails:
        
        definition = PromptAgentDefinition(
            model=chat_completion_model,
            instructions=self.agent_instruction,
            tools=tools        
        )

        return self.project_client.agents.create_version(agent_name=agent_name,
                                                         definition=definition,
                                                         description=agent_description)

    @property
    def get_agent_instruction(self) -> str:
        return self.agent_instruction