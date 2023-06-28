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


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event('startup')
async def startup_event():
    await connect_to_database()
    await connect_to_database()
    await create_tables()


@app.on_event('shutdown')
async def shutdown_event():
    await close_database_connection()


# Home page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Include the Bepa and peyk services
@app.get('/run_bepa_service')
async def run_bepa_service():
    result = await bepa_service()
    # print("SALAM")
    return {'result': result}


app.include_router(peyk_app)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8001, reload=True)
