from databases import Database
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'sqlite+aiosqlite:///./database.db'

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)  # Specify `future=True`
Base = declarative_base()
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)  # Add `expire_on_commit=False`
database = Database(SQLALCHEMY_DATABASE_URL)


async def connect_to_database():
    await database.connect()


async def close_database_connection():
    await database.disconnect()


async def get_db():
    async with async_session() as session:
        yield session

