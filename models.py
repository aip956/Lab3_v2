from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.dialects.postgresql import ARRAY
from pydantic import BaseModel, Field, validator, constr, root_validator
from database import Base
from typing import List
from datetime import datetime
from datetime import date as datetime_date
import re


#SQLAlchemy model for database representation
class Warrior(Base):
    __tablename__ = "warriors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    dob = Column(Date)
    fight_skills = Column(ARRAY(String))

# Pydantic model representing the basic structure of a warrior
class WarriorBase(BaseModel):
    name: str
    dob: datetime
    fight_skills: List[str] = Field(..., max_items=20, example=["Skill1", "Skill2"], min_items=1)


    class Config:
        from_attributes = True

    @validator('fight_skills')
    def check_length(cls, v):
        if len(v) > 20:
            raise ValueError('Max skills is 20')
        for skill in v:
            if len(skill) > 250:
                raise ValueError('Max char len is 250')
        return v
    
    
# Pydantic model representing the data needed to create a warrior
class WarriorCreate(WarriorBase): #Changed from BaseModel to WarriorBase

    @validator('dob', pre=True)
    def parse_dob(cls, value: str):
        try:
            # Ensure data is in the right format
            print("136dob: ", datetime.strptime(value, "%Y-%m-%d").date() )
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError as e:
            raise ValueError("dob must be in format YYYY-DD-MM") from e
    pass

