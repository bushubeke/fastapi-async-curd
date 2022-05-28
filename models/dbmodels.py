from enum import unique
from .dbconnect import Base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, DateTime, Column, Integer,String, ForeignKey, Sequence,Enum
from sqlalchemy.sql import func
# import datetime
from datetime import tzinfo, timedelta, datetime
from sqlalchemy.sql import func
import uuid
from typing import List, Optional,Literal
from pydantic import BaseModel,EmailStr
# from fastapi import Form  
from sqlalchemy.dialects.postgresql import ENUM, JSON,UUID,ARRAY,JSONB
from pydantic.dataclasses import dataclass

from sqlalchemy_json import mutable_json_type



###########################################################################
    #this is for functionality testing of variable types 
############################################################################

skill_level_enum =ENUM('Zero', 'A little', 'Some', 'A lot', name="skill_level",create_type=True)
class TestingDataTypes(Base):
    __tablename__ = 'testing_table'
    id = Column(Integer(), autoincrement="auto",primary_key=True)
    UUID_TYPE = Column('uuid_type',UUID(as_uuid=True),unique=True,default=uuid.uuid4)
    JSON_TYPE = Column('json_type',mutable_json_type(dbtype=JSON, nested=True),nullable=True)
    JSONB_TYPE = Column('jsonb_type',mutable_json_type(dbtype=JSONB, nested=True),nullable=True)
    ARRAY_TYPE = Column('array_type',ARRAY(Integer),nullable=True )
    ENUM_TYPE = Column('enum_type',skill_level_enum,default="Zero")
    STRING_TYPE = Column('string_type',String(50),nullable=True,default="empty")
    BOOLEAN_TYPE = Column('boolean_type',Boolean(),default=False,nullable=False)
    DATE_TIMESTAMP_TYPE = Column('date_time_stamp', DateTime(timezone=True), default=func.now())
    
    def __repr__(self):
        return f"<TestingDatatypes '{self.role_id}'>"
    
    @staticmethod
    def tableroute():
        return "test"    

@dataclass
class json_item:
    jid: int
    name: str = 'John Doe'
    test_list: Optional[List[str]] = None

@dataclass
class jsonb_item:
    jbid: int
    name: str = 'John Doe'
    test_list: Optional[List[str]] = None
        
# class TestingTableModel(BaseModel):
#     ID : int 
#     UUID_TYPE: uuid.UUID
#     JSON_TYPE :json_item
#     JSONB_TYPE : jsonb_item 
#     ARRAY_TYPE : List[int]
#     ENUM_TYPE : List[Literal['Zero', 'A little', 'Some', 'A lot']]
#     BOOLEAN_TYPE : bool
#     DATE_TIMESTAMP_TYPE : datetime  

class TestingTableModel(BaseModel):
    ID: Optional[int]
    UUID_TYPE: Optional[uuid.UUID]
    JSON_TYPE :Optional[json_item]
    JSONB_TYPE : Optional[jsonb_item] 
    ARRAY_TYPE : Optional[List[int]]
    ENUM_TYPE : Optional[Literal['Zero', 'A little', 'Some', 'A lot']]
    BOOLEAN_TYPE : Optional[bool]
    STRING_TYPE:Optional[str]
    DATE_TIMESTAMP_TYPE : Optional[datetime]  
    class Config:
        orm_mode = True
###########################################################################
    #this is for many to many roles models relationship 
############################################################################
