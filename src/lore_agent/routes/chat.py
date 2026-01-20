from fastapi import APIRouter, Depends, HTTPException
from contract import ChatRequest
from services import LoreAgentService
from typing import Annotated
from dependencies import get_lore_agent_service
from starlette.responses import StreamingResponse
import logging 

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/chat"
)

@router.post('/')
async def post(chat_request:ChatRequest,
               agent_service: Annotated[LoreAgentService, Depends(get_lore_agent_service)]) -> StreamingResponse:
    
    try:
        return StreamingResponse(agent_service.get_lore_information(chat_request.question),media_type="text/event-stream")
        #answer = await agent_service.get_lore_information(chat_request.question)
        #return answer
    except Exception as err:
        logger.error(err)
        raise HTTPException(status_code=500, detail='Internal Server Error')