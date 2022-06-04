from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from .config import settings

engine = create_engine(settings.DATABASE_MIGRATION_URI,future=True, echo=True)
asyncengine=create_async_engine(settings.DATABASE_ASYNC_URI,echo=True)
Base = declarative_base()   
#####################################################
async def async_main():
    #engine = create_async_engine(DATABASE_URL, future=True, echo=True)

    async with asyncengine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

######################################################
async def droptables():
    async with asyncengine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
######################################################