from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Price(Base):
    __tablename__ = 'prices'

    id = Column(Integer, primary_key=True, autoincrement=True)
    coin_name = Column(String)
    timestamp = Column(DateTime)
    price = Column(Float)


class AlertSubscription(Base):
    __tablename__ = 'alert_subscriptions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String)
    coin_name = Column(String)
    difference_percentage = Column(Integer)
