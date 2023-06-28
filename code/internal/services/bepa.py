from datetime import datetime

import requests

from code.internal.DB.database import get_db
from code.internal.model.models import Price, AlertSubscription

# Mailgun configuration
MAILGUN_API_KEY = 'e88254122f9aadcfd8b789490578edaf-e5475b88-057fdc51'
MAILGUN_DOMAIN = 'https://api.mailgun.net/v3/sandboxd810fa8fbc0944a39c6fb2760433b07d.mailgun.org'
MAILGUN_SENDER = 'mailgun@sandboxd810fa8fbc0944a39c6fb2760433b07d.mailgun.org'


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
    active_currencies = requests.get('http://localhost:8000/api/data').json()
    list_of_coins = []
    for coin_name in active_currencies:
        price = fetch_latest_price(coin_name)
        if price is not None:
            await write_price_to_database(coin_name, price)
            list_of_coins.append(coin_name)

    # Send email notifications to users based on alarm subscriptions
    await send_email_notifications(list_of_coins)


async def send_email_notifications(coins):
    async with get_db() as db:
        # Fetch users subscribed to the price changes of the given coins
        subscriptions = await db.query(AlertSubscription).filter(AlertSubscription.coin_name.in_(coins)).all()

        for subscription in subscriptions:
            # Calculate the percentage change of the subscribed coin
            percentage_change = calculate_percentage_change(subscription.coin_name)

            # Check if the current price change exceeds the subscribed difference percentage
            if abs(percentage_change) >= subscription.difference_percentage:
                # Compose email content
                subject = f"Price Change Alert: {subscription.coin_name}"
                message = f"The price of {subscription.coin_name} has changed by {percentage_change}%."

                # Send email using Mailgun API
                send_email(subscription.email, subject, message)


def calculate_percentage_change(coin_name):
    async with get_db() as db:
        # Fetch the last recorded price for the given coin
        last_price = await db.query(Price).filter(Price.coin_name == coin_name).order_by(Price.timestamp.desc()).first()

        # Calculate the percentage change compared to the previous price
        if last_price is not None:
            current_price = fetch_latest_price(coin_name)
            if current_price is not None:
                percentage_change = (current_price - last_price.price) / last_price.price * 100
                return round(percentage_change, 2)

    return 0.0


def send_email(recipient, subject, message):
    url = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages"
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
        print(f"Failed to send email to {recipient}")
