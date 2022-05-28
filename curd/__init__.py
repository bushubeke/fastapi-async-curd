import asyncio
from fastapi import APIRouter,FastAPI,Request,Depends,Header
from sqlalchemy import select,update,delete
from sqlalchemy.orm import declarative_base as Base, session, sessionmaker
from pydantic import BaseModel,EmailStr,Field
from typing import List,Dict,Tuple,Optional
from passlib.hash import pbkdf2_sha512
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import uuid
from dataclasses import is_dataclass, asdict