import asyncio
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from code.internal.DB.database import connect_to_database, close_database_connection, engine
from code.internal.model.models import Base
from code.internal.services.bepa import bepa_service
from code.internal.services.peyk import app as peyk_app

app = FastAPI()
templates = Jinja2Templates(directory="code/templates")

# Create a global variable to control the bepa_service task
bepa_service_task = None


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event('startup')
async def startup_event():
    await connect_to_database()
    await connect_to_database()
    await create_tables()
    # Start the bepa_service task upon startup
    start_bepa_service()


@app.on_event('shutdown')
async def shutdown_event():
    await close_database_connection()
    # Stop the bepa_service task upon shutdown
    stop_bepa_service()


# Home page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Include the Bepa and peyk services
@app.get('/run_bepa_service')
async def run_bepa_service():
    start_bepa_service()
    return {'result': 'Bepa service started'}


@app.get('/stop_bepa_service')
async def stop_bepa_service():
    global bepa_service_task
    if bepa_service_task is not None:
        bepa_service_task.cancel()
        bepa_service_task = None
        return {'result': 'Bepa service stopped'}
    else:
        return {'result': 'Bepa service is not running'}


async def bepa_service_wrapper():
    while True:
        await bepa_service()
        await asyncio.sleep(60)  # Run every 60 seconds


def start_bepa_service():
    global bepa_service_task
    if bepa_service_task is None:
        bepa_service_task = asyncio.create_task(bepa_service_wrapper())


app.include_router(peyk_app)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8001, reload=True)
