import sqlalchemy as sa
from fastapi import HTTPException, APIRouter

from src.internal.DB.database import get_db
from src.internal.model.models import Price, AlertSubscription

app = APIRouter()


@app.put('/subscribe_coin')
async def subscribe_coin(email: str, coin_name: str, difference_percentage: float):
    async with get_db() as db:
        db_subscription = AlertSubscription(email=email, coin_name=coin_name,
                                            difference_percentage=difference_percentage)
        db.add(db_subscription)
        await db.commit()

    return {'message': 'Subscription added successfully.'}


@app.get('/get_price_history')
async def get_price_history(coin_name: str):
    async with get_db() as db:
        prices = await db.execute(
            sa.select(Price).filter(Price.coin_name == coin_name).order_by(Price.timestamp)
        )
        prices = prices.scalars().all()

        if not prices:
            raise HTTPException(status_code=404, detail='Price history not found.')

        return [{'value': price.price, 'date': price.timestamp} for price in prices]
