import os
from datetime import datetime

import requests
from sqlalchemy import create_engine, select, desc, Column, Integer, Float, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# MySQL configurations
MYSQL_HOST = os.environ.get('MYSQL_HOST', 'db')
MYSQL_PORT = os.environ.get('MYSQL_PORT', '3306')
MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'password')
MYSQL_DB = os.environ.get('MYSQL_DB', 'db')

# Mailgun configuration
MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY", 'e88254122f9aadcfd8b789490578edaf-e5475b88-057fdc51')
MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN",
                                'https://api.mailgun.net/v3/sandboxd810fa8fbc0944a39c6fb2760433b07d.mailgun.org')
MAILGUN_SENDER = os.environ.get("MAILGUN_SENDER", 'mailgun@sandboxd810fa8fbc0944a39c6fb2760433b07d.mailgun.org')

is_bepa_service_running = False  # Flag to indicate if the bepa_service is running

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


engine = create_engine(f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}')
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)


def get_db():
    return Session()


def fetch_latest_price(coin_name):
    print("fetching the latest prices")
    response = requests.get(f'http://coinnews-container:8000/api/data/{coin_name}')
    if response.status_code == 200:
        data = response.json()
        return data['value']
    return None


async def write_price_to_database(coin_name, price):
    session = get_db()
    timestamp = datetime.now()
    db_price = Price(coin_name=coin_name, timestamp=timestamp, price=price)
    session.add(db_price)
    session.commit()


async def bepa_service():
    active_currencies = requests.get('http://coinnews-container:8000/api/data').json()
    coins = {}
    for coin_name in active_currencies:
        price = fetch_latest_price(coin_name)
        if price is not None:
            coins[coin_name] = price

    # Send email notifications to users based on alarm subscriptions
    await send_email_notifications(list(coins.keys()))
    for coin_name, price in coins.items():
        await write_price_to_database(coin_name, price)


async def send_email_notifications(coins):
    session = get_db()
    # Fetch users subscribed to the price changes of the given coins
    subscriptions = session.execute(
        select(AlertSubscription).where(AlertSubscription.coin_name.in_(coins))
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
    session = get_db()
    # Fetch the last recorded price for the given coin
    last_price = session.execute(
        select(Price).filter(Price.coin_name == coin_name).order_by(desc(Price.timestamp)).limit(1)
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


if __name__ == '__main__':
    bepa_service()
