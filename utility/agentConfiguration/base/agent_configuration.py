from abc import ABC, abstractmethod
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import AgentVersionDetails

class AgentConfiguration(ABC):
    
    @abstractmethod
    async def configure(self,project_client:AIProjectClient,chat_completion_model:str) -> AgentVersionDetails:
        pass