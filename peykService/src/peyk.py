import os

from fastapi import APIRouter, HTTPException
from sqlalchemy import select, Column, Integer, String, DateTime, Float
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

# Read MySQL configuration from environment variables
MYSQL_HOST = os.environ.get('MYSQL_HOST', 'db')
MYSQL_PORT = os.environ.get('MYSQL_PORT', 3306)
MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'password')
MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'mydb')

print(os.getcwd())
app = APIRouter()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="templates/static"), name="static")

# Create the MySQL engine and session
db_url = f"mysql+aiomysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
engine = create_async_engine(db_url, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession)

# MySQL setup
Base = declarative_base()


class Price(Base):
    __tablename__ = 'prices'
    id = Column(Integer, primary_key=True)
    coin_name = Column(String(255))
    timestamp = Column(DateTime)
    price = Column(Float)


class AlertSubscription(Base):
    __tablename__ = 'alert_subscriptions'
    id = Column(Integer, primary_key=True)
    coin_name = Column(String(255))
    difference_percentage = Column(Float)
    email = Column(String(255))


@app.put('/subscribe_coin')
async def subscribe_coin(email: str, coin_name: str, difference_percentage: float):
    async with async_session() as session:
        db_subscription = AlertSubscription(email=email, coin_name=coin_name, difference_percentage=difference_percentage)
        session.add(db_subscription)
        await session.commit()

    return {'message': 'Subscription added successfully.'}


@app.get('/get_price_history')
async def get_price_history(coin_name: str):
    async with async_session() as session:
        prices = await session.execute(select(Price).filter(Price.coin_name == coin_name).order_by(Price.timestamp))
        prices = prices.scalars().all()

        if not prices:
            raise HTTPException(status_code=404, detail='Price history not found.')

        return [{'value': price.price, 'date': price.timestamp} for price in prices]


# Home page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8080)
