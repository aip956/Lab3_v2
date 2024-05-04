from fastapi import FastAPI, HTTPException, Query, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from sqlalchemy import func
from models import Base, Warrior, WarriorBase, WarriorCreate
from typing import List
from datetime import datetime
from datetime import date as datetime_date


app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint to get warrior by ID
@app.get("/warrior/{id}", response_model=WarriorBase)
async def get_warrior_by_id(id: int, db: Session = Depends(get_db)):
    warrior = db.query(Warrior).filter(Warrior.id == id).first()
    if warrior is None:
        raise HTTPException(status_code=404, detail="Warrior not found")
    warrior.dob = warrior.dob.strftime('%Y-%d-%m') # Format date to Y-D-M
    # return warrior
    return WarriorBase.from_orm(warrior)


# Endpoint to search warriors by attributes
@app.get("/warrior", response_model=List[WarriorBase])
def search_warriors(
    db: Session = Depends(get_db),
    t: Optional[str] = Query(None, description="Search term")
):
    # query = db.query(Warrior)
    if t:
        warriors = db.query(Warrior).filter(func.lower(Warrior.name).contains(func.lower(t))).all()
    else:
        warriors = db.query(Warrior).all()
    if not warriors:
        raise HTTPException(status_code=404, detail="No warriors found")
    for warrior in warriors:
        warrior.dob = warrior.dob.strftime('%Y-%d-%m') # Format date
    return warriors
   

# Endpoint to count registered warriors
@app.get("/counting-warriors")
def count_warriors(db: Session = Depends(get_db)):
    count = db.query(Warrior).count()
    return {"Count: ": count}

# Endpiont to create a warrior
def parse_date_from_string(date_str):
    year, day, month = map(int, date_str.split('-'))
    return datetime(year, month, day).date()

@app.post("/warrior", response_model=WarriorBase)
def create_warrior(warrior: WarriorCreate, db: Session = Depends(get_db)):
    # Format date before saving to DB
    print("In main Post80")
    # Print received data
    print("warrior: ", warrior)
    print("Received data:", warrior.dict())

    # Check type of 'warrior'
    print("Type of 'warrior':", type(warrior))

    # Check individual fields of 'warrior'
    print("Name:", warrior.name)
    print("DOB:", warrior.dob)
    print("Fight skills:", warrior.fight_skills)
    print("MainPost90")  
    db_warrior = Warrior(**warrior.dict())
    print("MainPost96")  
    db.add(db_warrior)
    db.commit()
    db.refresh(db_warrior)
    print("MainPost100")  
    return db_warrior

# Use port 8080
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)