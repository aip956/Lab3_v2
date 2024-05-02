from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.dialects.postgresql import ARRAY
from pydantic import BaseModel, Field, validator, constr
from database import Base
from typing import List
import datetime
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
    dob: str
    fight_skills: List[str] = Field(..., max_items=20, example=["Skill1", "Skill2"], min_items=1)


    class Config:
        orm_mode = True

    @validator('fight_skills')
    def check_length(cls, v):
        if len(v) > 20:
            raise ValueError('Max skills is 20')
        for skill in v:
            if len(skill) > 250:
                raise ValueError('Max char len is 250')
        return v
    
    @validator('dob')
    def check_date_format(cls, v):
        if not re.match(r'\d{4}-\d{2}-\d{2}', str(v)):
            raise ValueError('Invalid date format; YYYY-DD-MM')
        try:
            year, day, month = map(int, str(v).split('-')) # Extract yr, day, month
            datetime.date(year, month, day) # Create  a date object to validate date
            # datetime.datetime.strptime(str(v), '%Y-%d-%m').date()
        except ValueError as e:
            raise ValueError('Invalid date format; YYYY-DD-MM')
        return v




# Pydantic model representing the data needed to create a warrior
class WarriorCreate(WarriorBase): #Changed from BaseModel to WarriorBase
    pass

