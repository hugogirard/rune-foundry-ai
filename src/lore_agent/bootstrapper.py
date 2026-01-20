from fastapi import FastAPI
from contextlib import asynccontextmanager
from services import LoreAgentService
from config import config

@asynccontextmanager
async def lifespan_event(app: FastAPI):
    
    app.state.lore_agent_service = LoreAgentService(config)

    yield

class Bootstrapper:

    def run(self) -> FastAPI:

        app = FastAPI(lifespan=lifespan_event)

        self._configure_monitoring(app)

        return app        

    def _configure_monitoring(self, app: FastAPI):
        pass        