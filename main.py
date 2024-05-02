from fastapi import FastAPI, HTTPException, Query, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from sqlalchemy import func
from models import Base, Warrior, WarriorBase, WarriorCreate


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
def get_warrior_by_id(id: int, db: Session = Depends(get_db)):
    warrior = db.query(Warrior).filter(Warrior.id == id).first()
    if warrior is None:
        raise HTTPException(status_code=404, detail="Warrior not found")
    return warrior

# Endpoint to search warriors by attributes
@app.get("/warrior", response_model=List[WarriorBase])
def search_warriors(
    db: Session = Depends(get_db),
    t: Optional[str] = Query(None, description="Search term")
):
    if t is None:
        warriors = db.query(Warrior).all()
        if not warriors:
            raise HTTPException(status_code=404, detail="No warriors found")
        return warriors
    filtered_warriors = db.query(Warrior).filter(
        func.lower(Warrior.name).contains(func.lower(t))
    ).all()
    if not filtered_warriors:
        raise HTTPException(status_code=404, detail="No matching warriors found")
    return filtered_warriors


# Endpoint to count registered warriors
@app.get("/counting-warriors")
def count_warriors(db: Session = Depends(get_db)):
    count = db.query(Warrior).count()
    return {"Count: ": count}

# Endpiont to create a warrior
@app.post("/warrior", response_model=WarriorBase)
def create_warrior(warrior: WarriorCreate, db: Session = Depends(get_db)):
    db_warrior = Warrior(**warrior.dict())
    db.add(db_warrior)
    db.commit()
    db.refresh(db_warrior)
    return db_warrior


# Use port 8080
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)