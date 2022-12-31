import uuid
from enum import unique
from datetime import tzinfo, timedelta, datetime
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, DateTime, Column, Integer,String, ForeignKey, Sequence,Enum
from sqlalchemy.dialects.postgresql import ENUM, JSON,UUID,ARRAY,JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy_json import mutable_json_type
from pydantic import BaseModel
from pydantic.dataclasses import dataclass
from typing import List, Optional,Literal
from .dbconnect import Base

###########################################################################
    #this is for functionality testing of variable types 
############################################################################

skill_level_enum =ENUM('Zero', 'A little', 'Some', 'A lot', name="skill_level",create_type=True)
class TestingDataTypes(Base):
    __tablename__ = 'testing_table'
    id = Column(Integer(), autoincrement="auto",primary_key=True)
    uuid = Column(UUID(as_uuid=True),unique=True,default=uuid.uuid4)
    JSON_TYPE = Column(mutable_json_type(dbtype=JSON, nested=True),nullable=True)
    JSONB_TYPE = Column(mutable_json_type(dbtype=JSONB, nested=True),nullable=True)
    ARRAY_TYPE = Column(ARRAY(Integer),nullable=True )
    ENUM_TYPE = Column(skill_level_enum,default="Zero")
    STRING_TYPE = Column(String(50),nullable=True,default="empty")
    BOOLEAN_TYPE = Column(Boolean(),default=False,nullable=False)
    DATE_TIMESTAMP_TYPE = Column(DateTime(timezone=True), default=func.now())
    
    def __repr__(self):
        return f"<TestingDatatypes '{self.id}'>"
    
    @staticmethod
    def read_roles():
        return ["superuser"]
    
    @staticmethod
    def write_roles():
        return ['superuser'] 
        
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

class TestingTableModel(BaseModel):
    id: Optional[int]
    uuid: Optional[uuid.UUID]
    JSON_TYPE :Optional[json_item]
    JSONB_TYPE : Optional[jsonb_item] 
    ARRAY_TYPE : Optional[List[int]]
    ENUM_TYPE : Optional[Literal['Zero', 'A little', 'Some', 'A lot']]
    BOOLEAN_TYPE : Optional[bool]
    STRING_TYPE:Optional[str]
    DATE_TIMESTAMP_TYPE : Optional[datetime]  
    class Config:
        orm_mode = True

class TestingTablePostModel(BaseModel):
    
    JSON_TYPE :Optional[json_item]
    JSONB_TYPE : Optional[jsonb_item] 
    ARRAY_TYPE : Optional[List[int]]
    ENUM_TYPE : Optional[Literal['Zero', 'A little', 'Some', 'A lot']]
    BOOLEAN_TYPE : Optional[bool]
    STRING_TYPE:Optional[str]
      
    class Config:
        orm_mode = True

