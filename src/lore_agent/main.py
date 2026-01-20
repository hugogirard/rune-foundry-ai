from fastapi import FastAPI
from bootstrapper import Boostrapper
from fastapi.responses import RedirectResponse
from routes import routes
from config import config
import logging
import sys

app = Boostrapper().run()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Get a logger for this module
logger = logging.getLogger(__name__)

# Load all the routes
for route in routes:
    app.include_router(route,prefix="/api")

# Redirect to the swagger file by default
# remove this if this behavior is not needed
@app.get('/', include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")    