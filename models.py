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
        # json_encoders = {
        #     datetime_date: lambda v: v.strftime('%Y-%d-%m')
        # }

    @validator('fight_skills')
    def check_length(cls, v):
        if len(v) > 20:
            raise ValueError('Max skills is 20')
        for skill in v:
            if len(skill) > 250:
                raise ValueError('Max char len is 250')
        return v
    
    # @root_validator(pre=True)
    # def format_dates(cls, values):
    #     print("Mdl44ValType: ", type(values))
    #     print("Mdl45Values: ", values)
    #     # dob_str = values.get('dob')
    #     # dob_str = values.dob
    #     dob_str = None
    #     if isinstance(values, dict):
    #         dob_str = values.get('dob')
    #     elif isinstance(values, WarriorCreate):
    #         dob_str = values.dob
    #     elif isinstance(values, Warrior):
    #         dob_str = values.dob
    #     # if 'dob' in values:
    #     #     dob_str = values['dob']
    #     print("Mdl46dobType: ", type('dob'))
    #     print("Model45dob_Str: ",dob_str)
    #     print("Mdl46dob_strType: ", type(dob_str))
    #     if dob_str:
    #         year, day, month = map(int, dob_str.split('-'))
    #         dob_datetime = datetime(year, month, day)
    #         print("Model63DOB_datetime: ", dob_datetime)
    #         values['dob'] = dob_datetime.strftime('%Y-%m-%d')
    #         cls.check_date_format(values['dob'])
    #         print("Model51Day", day)
    #         print("Model5month", month)
    #     # print("Model48Vals: ", values['dob'])
    #     print("Mdl49ValType: ", type(values['dob']))
    #     print("Mdl52Vals: ", values)
    #     print("Mdl53ValType: ", type(values))
    #     return values
        # dob = values['dob']
        # warrior.dob = warrior.dob.strftime('%Y-%d-%m')
        # print("warrior.dob: ", warrior.dob)
        # dob = values.get('dob')
        # print("mdlDOB: ", dob)
        # dob = values['dob'] if 'dob' in values else None
        # if dob and isinstance(dob, str):
        #     try:
        #         year, day, month = map(int, dob.split('-'))
        #         print("Modlmonth: ", month)
        #         print("ModlDay: ", day)
        #         formatted_date = datetime_date(year, month, day)
        #         print("Modlformatted_date: ", formatted_date)
        #         values['dob'] = formatted_date.strftime('%Y-%m-%d')
        #     except ValueError as e:
        #         raise ValueError(f"Mdl56Date format error: {str(e)}")
        # print("Model57Vals: ", values)
        # print("Mdl58ValType: ", type(values))
        # return values

        
    # @validator('dob')
    # def check_date_format(cls, v):
    #     print("Modl62v: ", v)
    #     print("Model85_v_type: ", type(v))
    #     if isinstance(v, datetime):
    #         v = v.strftime('%Y-%m-%d')
    #     elif not isinstance(v, str):
    #         raise ValueError("89Model Invalid date format; not a string or datetime obj")

    #     if not re.match(r'\d{4}-\d{2}-\d{2}', v):
    #         raise ValueError('50Invalid date format; YYYY-DD-MM')
    
    #     year, month, day = map(int, v.split('-')) # Extract yr, day, month
    #     print("Modl94month: ", month)
    #     print("Modl95Day: ", day)
    #     if month > 12:
    #         raise ValueError("Month value is > 12")
    #     try:            
    #         datetime_date(year, month, day) # Create  a date object to validate date
    #         # print(f'Validated Date: Month: {month}, Day: {day}')

    #         # datetime.datetime.strptime(str(v), '%Y-%d-%m').date()
    #     except ValueError as e:
    #         raise ValueError(f'57Invalid date format: {e}')
    #     return v

    # @property
    # def formatted_dob(self):
    #     year, day, month = map(int, self.dob.split('-'))
    #     return f"{year:04d}-{day:02d}-{month:02d}" # Return YYYY-DD-MM
    
# Pydantic model representing the data needed to create a warrior
class WarriorCreate(WarriorBase): #Changed from BaseModel to WarriorBase
    
    # name: str
    # dob: str
    # fight_skills: List[str] = Field(..., max_items=20, example=["Skill1", "Skill2"], min_items=1)
    @validator('dob', pre=True)
    def parse_dob(cls, value: str):
        try:
            # Ensure data is in the right format
            print("136dob: ", datetime.strptime(value, "%Y-%m-%d").date() )
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError as e:
            raise ValueError("dob must be in format YYYY-DD-MM") from e
    pass

