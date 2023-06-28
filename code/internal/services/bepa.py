import asyncio
from datetime import datetime

import requests
import sqlalchemy as sa

from code.internal.DB.database import get_db
from code.internal.model.models import Price, AlertSubscription

# TIME INTERVALS IN SECONDS
TIME_INTERVAL_TO_CHECK_FOR_PRICE = 10

# Mailgun configuration
MAILGUN_API_KEY = 'e88254122f9aadcfd8b789490578edaf-e5475b88-057fdc51'
MAILGUN_DOMAIN = 'https://api.mailgun.net/v3/sandboxd810fa8fbc0944a39c6fb2760433b07d.mailgun.org'
MAILGUN_SENDER = 'mailgun@sandboxd810fa8fbc0944a39c6fb2760433b07d.mailgun.org'

is_bepa_service_running = False  # Flag to indicate if the bepa_service is running


def fetch_latest_price(coin_name):
    response = requests.get(f'http://localhost:8000/api/data/{coin_name}')
    if response.status_code == 200:
        data = response.json()
        return data['value']
    return None


async def write_price_to_database(coin_name, price):
    async with get_db() as db:
        timestamp = datetime.now()
        db_price = Price(coin_name=coin_name, timestamp=timestamp, price=price)
        db.add(db_price)
        await db.commit()


async def bepa_service():
    global is_bepa_service_running
    is_bepa_service_running = True

    while is_bepa_service_running:
        active_currencies = requests.get('http://localhost:8000/api/data').json()
        coins = {}
        for coin_name in active_currencies:
            price = fetch_latest_price(coin_name)
            if price is not None:
                coins[coin_name] = price

        # Send email notifications to users based on alarm subscriptions
        await send_email_notifications(coins.keys())
        for coin_name, price in coins.items():
            await write_price_to_database(coin_name, price)

        await asyncio.sleep(TIME_INTERVAL_TO_CHECK_FOR_PRICE)  # Run the service every TIME_INTERVAL_TO_CHECK_FOR_PRICE seconds


async def send_email_notifications(coins):
    async with get_db() as db:
        # Fetch users subscribed to the price changes of the given coins
        subscriptions = await db.execute(
            sa.select(AlertSubscription).where(AlertSubscription.coin_name.in_(coins))
        )
        for subscription in subscriptions.scalars():
            # Calculate the percentage change of the subscribed coin
            percentage_change = await calculate_percentage_change(subscription.coin_name)

            # Check if the current price change exceeds the subscribed difference percentage
            if abs(percentage_change) >= subscription.difference_percentage:
                # Compose email content
                subject = f"Price Change Alert: {subscription.coin_name}"
                message = f"The price of {subscription.coin_name} has changed by {percentage_change}%."

                # Send email using Mailgun API
                send_email(subscription.email, subject, message)


async def calculate_percentage_change(coin_name):
    async with get_db() as db:
        # Fetch the last recorded price for the given coin
        last_price = await db.execute(
            sa.select(Price).filter(Price.coin_name == coin_name).order_by(Price.timestamp.desc()).limit(1)
        )
        last_price = last_price.scalars().first()

        # Calculate the percentage change compared to the previous price
        if last_price is not None:
            current_price = fetch_latest_price(coin_name)
            if current_price is not None:
                percentage_change = (current_price - last_price.price) / last_price.price * 100
                return round(percentage_change, 2)

    return 0.0


def send_email(recipient, subject, message):
    url = f"{MAILGUN_DOMAIN}/messages"
    auth = ("api", MAILGUN_API_KEY)
    data = {
        "from": MAILGUN_SENDER,
        "to": recipient,
        "subject": subject,
        "text": message
    }

    response = requests.post(url, auth=auth, data=data)
    if response.status_code == 200:
        print(f"Email sent to {recipient}")
    else:
        print(response.json())
        print(f"Failed to send email to {recipient}")


def stop_bepa_service():
    global is_bepa_service_running
    is_bepa_service_running = False
    print("Bepa service stopped.")
