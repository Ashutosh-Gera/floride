from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine


app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/users/signup", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/users/login", response_model=schemas.User)
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect email")
    return db_user

# Given a user id, return all the past bookings of that user
@app.get("/users/{user_id}/bookings", response_model=schemas.Booking)
def view_past_bookings(user_id: int, db: Session = Depends(get_db)):
    db_booking = crud.view_past_bookings(db, user_id=user_id)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="No bookings found")
    return db_booking


# driver registration
@app.post("/drivers/signup", response_model=schemas.Driver)
def register_driver(driver: schemas.DriverCreate, db: Session = Depends(get_db)):
    # date_of_birth throwing an error for some reason and I have no clue why
    db_driver = crud.get_driver_by_email(db, email=driver.email)
    if db_driver:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.register_driver(db=db, driver=driver)
