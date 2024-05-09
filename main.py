from fastapi import FastAPI, HTTPException, Query, Depends, Response, status
from typing import List, Optional
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from sqlalchemy import func, create_engine
from models import Base, Warrior, WarriorBase, WarriorCreate
from typing import List
from datetime import datetime
from datetime import date as datetime_date


app = FastAPI()

def prepare_database():
    #drop table if exists
    Warrior.__table__.drop(engine, checkfirst=True)
    # Create database tables
    Base.metadata.create_all(bind=engine)

# Call the function to prepare the db
prepare_database()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint to get warrior by ID
@app.get("/warrior/{id}", response_model=WarriorBase, status_code=201)
async def get_warrior_by_id(id: int, db: Session = Depends(get_db)):
    warrior = db.query(Warrior).filter(Warrior.id == id).first()
    if warrior is None:
        raise HTTPException(status_code=404, detail="Warrior not found")
    warrior.dob = warrior.dob.strftime('%Y-%m-%d') # Format date to Y-D-M
    # return warrior
    return WarriorBase.from_orm(warrior)


# Endpoint to search warriors by attributes
@app.get("/warrior", response_model=List[WarriorBase], status_code=201)
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
        warrior.dob = warrior.dob.strftime('%Y-%m-%d') # Format date
    return warriors
   

# Endpoint to count registered warriors
@app.get("/counting-warriors", status_code=201)
def count_warriors(db: Session = Depends(get_db)):
    count = db.query(Warrior).count()
    return {"Count: ": count}

# Endpiont to create a warrior
def parse_date_from_string(date_str):
    year, day, month = map(int, date_str.split('-'))
    return datetime(year, month, day).date()

@app.post("/warrior", response_model=WarriorBase, status_code=status.HTTP_201_CREATED)
def create_warrior(response: Response, warrior: WarriorCreate, db: Session = Depends(get_db)):
    try:
        db_warrior = Warrior(**warrior.dict())
        db.add(db_warrior)
        db.commit()
        db.refresh(db_warrior)
        response.headers["Location"] = f"/warrior/{db_warrior.id}"
        return db_warrior
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Use port 8080
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)