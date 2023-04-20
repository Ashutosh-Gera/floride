# In this file we will have reusable functions that we can use to perform CRUD operations on our database
# CRUD = Create, Read, Update, Delete

# Read data

from sqlalchemy.orm import Session
import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_driver_by_email(db: Session, email: str):
    return db.query(models.Driver).filter(models.Driver.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    #fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(first_name=user.first_name, last_name=user.last_name, email=user.email, phone_number=user.phone_number)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_booking(db: Session, booking: schemas.BookingCreate):
    db_booking = models.Booking(user_id=booking.user_id, car_id=booking.car_id, booking_date=booking.booking_date, booking_time=booking.booking_time, pickup_location=booking.pickup_location, dropoff_location=booking.dropoff_location)
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def get_location(db: Session, location_id: int):
    return db.query(models.Location).filter(models.Location.location_id == location_id).first()

def view_past_bookings(db: Session, user_id: int):
    # FOR SOME REASON .all() IS NOT WORKING. I am using .first() for now
    return db.query(models.Booking).filter(models.Booking.passenger_id == user_id).first()

# register driver
def register_driver(db: Session, driver: schemas.DriverCreate):
    db_driver = models.Driver(
        first_name=driver.first_name,
        last_name=driver.last_name,
        email=driver.email,
        phone_number=driver.phone_number,
        gender=driver.gender,
        license_number=driver.license_number,
        rating=driver.rating,
        date_of_birth=driver.date_of_birth,
        car_id=driver.car_id,
        location_id=driver.location_id,
        )
    db.add(db_driver)
    db.commit()
    db.refresh(db_driver)
    return db_driver
