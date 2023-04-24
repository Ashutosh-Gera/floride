from typing import List
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
@app.get("/users/{user_id}/bookings", response_model=List[schemas.Booking])
def view_past_bookings_by_user(user_id: int, db: Session = Depends(get_db)):
    db_booking = crud.view_past_bookings_by_user(db, user_id=user_id)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="No bookings found")
    return db_booking

# driver registration
@app.post("/drivers/signup", response_model=schemas.Driver)
def register_driver(driver: schemas.DriverCreate, db: Session = Depends(get_db)):
    db_driver = crud.get_driver_by_email(db, email=driver.email)
    if db_driver:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.register_driver(db=db, driver=driver)

# driver login
@app.post("/drivers/login", response_model=schemas.Driver)
def login_driver(driver: schemas.DriverLogin, db: Session = Depends(get_db)):
    db_driver = crud.get_driver_by_email(db, email=driver.email)
    if not db_driver:
        raise HTTPException(status_code=400, detail="Incorrect email")
    return db_driver

# Given a driver id, return the active booking of that driver
@app.get("/drivers/{driver_id}/bookings", response_model=List[schemas.Booking])
def view_bookings(driver_id: int, db: Session = Depends(get_db)):
    # Check if there exists a booking with driver_id=driver_id and status_id=1
    db_bookings = crud.get_bookings_by_driver(db, driver_id=driver_id)
    if db_bookings is None:
        raise HTTPException(status_code=404, detail="No bookings found")
    return db_bookings

# Given a booking_id, let the driver reject the booking
@app.post("/drivers/{driver_id}/bookings/{booking_id}/reject", response_model=schemas.Booking)
def reject_booking(driver_id: int, booking_id: int, db: Session = Depends(get_db)):
    # Check if there exists a booking with driver_id=driver_id and status_id=1
    db_booking = crud.get_booking_by_id(db, booking_id=booking_id)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="No bookings found")
    return crud.cancel_ride(db=db, booking_id=booking_id)

# Given a booking_id, let the driver complete the booking
@app.post("/drivers/{driver_id}/bookings/{booking_id}/complete", response_model=schemas.Booking)
def complete_booking(driver_id: int, booking_id: int, db: Session = Depends(get_db)):
    # Check if there exists a booking with driver_id=driver_id and status_id=1
    db_booking = crud.get_booking_by_id(db, booking_id=booking_id)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="No bookings found")
    if db_booking.status_id == 2:
        raise HTTPException(status_code=400, detail="Ride is already complete")
    elif db_booking.status_id == 3:
        raise HTTPException(status_code=400, detail="Ride has been cancelled")

    # Check if the driver is the same as the driver_id
    ride = crud.complete_ride(db=db, booking_id=booking_id)

    return ride

# Given a booking_id, let the user rate the ride
@app.post("/users/{user_id}/bookings/{booking_id}/rate", response_model=schemas.Booking)
def rate_ride(review: schemas.ReviewCreate, booking_id: int, db: Session = Depends(get_db)):
    # Check if there exists a booking with user_id=user_id and status_id=2
    db_booking = crud.get_booking_by_id(db, booking_id=booking_id)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="No bookings found")
    if db_booking.status_id == 1:
        raise HTTPException(status_code=400, detail="Ride is not complete")
    elif db_booking.status_id == 3:
        raise HTTPException(status_code=400, detail="Ride has been cancelled")

    # Check if the user is the same as the user_id

    return crud.rate_ride(db=db, booking_id=booking_id, review=review)


# View the past bookings of a driver
@app.get("/drivers/{driver_id}/past-bookings", response_model=List[schemas.Booking])
def view_past_bookings_by_driver(driver_id: int, db: Session = Depends(get_db)):
    db_bookings = crud.view_past_bookings_by_driver(db, driver_id=driver_id)
    if db_bookings is None:
        raise HTTPException(status_code=404, detail="No bookings found")
    return db_bookings


# new booking
@app.post("/users/{user_id}/bookings/new", response_model=schemas.Booking)
def new_booking(booking: schemas.BookingCreate, user_id: int, db: Session = Depends(get_db)):
    # Check if there exists a booking with user_id=user_id and status_id=1
    db_bookings = crud.get_ongoing_booking_by_user(db, user_id=user_id)
    if db_bookings:
        raise HTTPException(status_code=400, detail="You have an ongoing booking")
    return crud.new_booking(db=db, booking=booking, user_id=user_id)