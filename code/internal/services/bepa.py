from datetime import datetime

import requests

from code.internal.DB.database import get_db
from code.internal.model.models import Price


def fetch_latest_price(coin_name):
    response = requests.get(f'http://localhost:8000/api/data/{coin_name}')
    if response.status_code == 200:
        data = response.json()
        return data['value']
    return None


def write_price_to_database(coin_name, price):
    with get_db() as db:
        timestamp = datetime.now()
        db_price = Price(coin_name=coin_name, timestamp=timestamp, price=price)
        db.add(db_price)
        db.commit()


def bepa_service():
    active_currencies = requests.get('http://localhost:8000/api/data').json()
    for coin_name in active_currencies:
        price = fetch_latest_price(coin_name)
        if price is not None:
            write_price_to_database(coin_name, price)

    # Send email notifications to users based on alarm subscriptions
    # Implement your email notification logic here