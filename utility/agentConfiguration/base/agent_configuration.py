from abc import ABC, abstractmethod
from azure.ai.projects import AIProjectClient

class AgentConfiguration(ABC):
    
    @abstractmethod
    async def configure(project_client:AIProjectClient,chat_completion_model:str):
        pass