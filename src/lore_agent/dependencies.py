from fastapi import Request, HTTPException
from services import LoreAgentService
from config import config


# We leverage Easy Auth for the JWT Token
# Since the App is hosted in App Service
# Remove this to implement proper JWT validation
def get_easy_auth_token(request: Request)->str:
    if config.is_development:
        user_principal_id = config.user_principal_name_dev
    else:
        user_principal_id = request.headers.get(key='X-MS-CLIENT-PRINCIPAL-NAME',default=None)
    
    if user_principal_id is None:
        raise HTTPException(401,'No user identity present')
    
    return user_principal_id

def get_lore_agent_service(request: Request) -> LoreAgentService:
    return request.app.state.lore_agent_service