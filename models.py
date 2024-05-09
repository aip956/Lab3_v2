from fastapi import HTTPException
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from uuid import uuid4
from pydantic import BaseModel, Field, validator, constr, root_validator, ValidationError
from database import Base
from typing import List
from datetime import datetime
import re


#SQLAlchemy model for database representation
class Warrior(Base):
    __tablename__ = "warriors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    name = Column(String, index=True)
    dob = Column(Date)
    fight_skills = Column(ARRAY(String))

# Pydantic model representing the basic structure of a warrior
class WarriorBase(BaseModel):
    # id: Optional[UUID] = None #If id might not be known at time of object creation
    name: str
    dob: datetime
    fight_skills: List[str] 
    # = Field(..., max_items=20, example=["Skill1", "Skill2"], min_items=1)


    class Config:
        from_attributes = True

    @validator('fight_skills')
    def check_length_skills(cls, skills):
        # Check <= 20 skills
        if len(skills) > 20:
            raise ValueError('Max skills is 20')
        # Check string length is <= 250 chars
        combined_skills = ' '.join(skills)
        if len(combined_skills) > 250:
            raise ValueError('Max char len is 250')
        # Check each skill is valid
        valid_styles = [
            "BJJ", "Karate", "Judo", "KungFu", "Capoeira", "Boxing", 
            "Taekwondo", "Aikido", "KravMaga", "MuayThai", "KickBoxing", 
            "Pankration", "Wrestling", "Sambo", "Savate", "Sumo", "Kendo", 
            "Hapkido", "LutaLivre", "WingChu", "Ninjutsu", "Fencing", 
            "ArmWrestling", "SuckerPunch", "44Magnum"
        ]
        for skill in skills:
            if skill not in valid_styles:
                raise ValueError("Invalid skill")
        return skills
    
    @validator('name')
    def validate_name(cls, value):
        if len(value) > 100:
            raise ValueError("Name too long")
        if not value.replace(' ', '').isalpha():
            raise ValueError("Name must contain only alphanumeric chars and spaces")
        return value
    
    
# Pydantic model representing the data needed to create a warrior
class WarriorCreate(WarriorBase): #Changed from BaseModel to WarriorBase

    @validator('dob', pre=True)
    def parse_dob(cls, value: str):
        try:
            # Ensure data is in the right format
            # print("136dob: ", datetime.strptime(value, "%Y-%m-%d").date() )
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError as e:
            raise ValueError("53Models, DOB must be in format YYYY-MM-DD") from e
    pass

