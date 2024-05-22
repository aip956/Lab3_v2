import json
from fastapi import FastAPI, HTTPException, Query, Depends, Response, status
from typing import List, Optional
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from sqlalchemy import func, create_engine
from models import Base, Warrior, WarriorBase, WarriorCreate
from typing import List
from datetime import datetime
from datetime import date as datetime_date
import logging
from uuid import uuid4
from redis_config import get_redis_client, redis_dependency
import json



app = FastAPI()
logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

def prepare_database():
    #drop table if exists
    # Warrior.__table__.drop(engine, checkfirst=True)
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
@app.get("/warrior/{id}", response_model=WarriorBase, status_code=200)
async def get_warrior_by_id(id: str, db: Session = Depends(get_db), redis_client = Depends(redis_dependency)): #Do same with redis?
    # redis_client = get_redis_client()
    # async with redis_client as client:
    warrior_data = await client.get(f"warrior_{id}")
    logger.info("45id: ", id)
    if warrior_data:
        logger.info(f"47cache hit for warrior {id}")
        return json.loads(warrior_data)
    else:
        logger.info(f"cache miss line 50 id: {id}")
        # logger.info("id: ", id)
        warrior = db.query(Warrior).get(id)
        if warrior is None:
            logger.error(f"54Warrior not found for ID {id}")
            raise HTTPException(status_code=404, detail="Warrior not found")
        # warrior_data = warrior.dict()
        # convert warrior from 52 into json directly?
        warrior_data = {
            "id": warrior.id,
            "name": warrior.name,
            "dob": warrior.dob.strftime('%Y-%m-%d'),
            "fight_skills": warrior.fight_skills
        }
        await redis_client.set(f"warrior_{id}", json.dumps(warrior_data), ex=3600) # Cache for 1 hour
        logger.info(f"66Data for warrior {id} cached for 1 hour")
        return warrior_data


# Endpoint to search warriors by attributes
@app.get("/warrior", response_model=List[WarriorBase], status_code=200)
def search_warriors(
    db: Session = Depends(get_db),
    t: Optional[str] = Query(None, description="Search term")
):
    # query = db.query(Warrior)
    # logger.info("search: ", t)
    if t:
        warriors = db.query(Warrior).filter(func.lower(Warrior.name).contains(func.lower(t))).all()
    else:
        # warriors = db.query(Warrior).all()
    # if not warriors:
        raise HTTPException(status_code=400, detail="Search term is required")
        
    
    for warrior in warriors:
        warrior.dob = warrior.dob.strftime('%Y-%m-%d') # Format date
    return warriors
   

# Endpoint to count registered warriors
@app.get("/counting-warriors", status_code=200)
async def count_warriors(db: Session = Depends(get_db), redis_client = Depends(redis_dependency)):
    # redis_client = get_redis_client()
    # might need await below
    # async with redis_client as client:
    count = await redis_client.get("warrior_count")
    logger.info(f"97Number of warriors counted: {count}")
    if count is None:
        count = db.query(Warrior).count()
        await redis_client.set("warrior_count", count, ex=3600) # Cached for 1 hour
        logger.info(f"101Number of warriors counted: {count}")
    else:
        logger.info(f"103Retrieved warrior count from cache: {count}")
    return {"Count: ": count}

# Endpiont to create a warrior
def parse_date_from_string(date_str):
    year, day, month = map(int, date_str.split('-'))
    return datetime(year, month, day).date()

@app.post("/warrior", response_model=WarriorBase, status_code=status.HTTP_201_CREATED)
async def create_warrior(response: Response, warrior: WarriorCreate, db: Session = Depends(get_db), redis_client = Depends(redis_dependency)):
    try:
        db_warrior = Warrior(**warrior.dict())
        db_warrior.id = str(uuid4())
        db.add(db_warrior)
        db.commit()
        db.refresh(db_warrior)
        response.headers["Location"] = f"/warrior/{db_warrior.id}"


        # async with redis_client as client:
            #Serialize and cache new warrior
        warrior_data = {
            "id": db_warrior.id,
            "name": db_warrior.name,
            "dob": db_warrior.dob.strftime('%Y-%m-%d'),
            "fight_skills": db_warrior.fight_skills
        }
        await redis_client.set(f"warrior_{db_warrior.id}", json.dumps(warrior_data), ex=3600) # Cache for 1 hour
        return db_warrior
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Use port 8080
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)