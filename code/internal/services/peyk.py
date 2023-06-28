from fastapi import FastAPI, HTTPException, APIRouter

from code.internal.DB.database import get_db
from code.internal.model.models import Price

app = APIRouter()


# app must be of type response class

@app.get('/subscribe_coin')
def subscribe_coin(email: str, coin_name: str, difference_percentage: int):
    pass


# Implement your logic to save the subscription details to the database
# You can use the AlertSubscription model to create a new record

@app.get('/get_price_history')
def get_price_history(coin_name: str):
    with get_db() as db:
        prices = db.query(Price).filter(Price.coin_name == coin_name).all()
        if not prices:
            raise HTTPException(status_code=404, detail='Price history not found.')
        return [{'value': price.price, 'date': price.timestamp} for price in prices]
