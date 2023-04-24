# In this file we will have reusable functions that we can use to perform CRUD operations on our database
# CRUD = Create, Read, Update, Delete

# Read data

from datetime import datetime, timedelta
import random
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
    try:
        # db.begin()

        db_user = models.User(first_name=user.first_name, last_name=user.last_name, email=user.email, phone_number=user.phone_number)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except:
        db.rollback()
        raise
    
    return db_user


def create_booking(db: Session, booking: schemas.BookingCreate):
    try:
        # db.begin()

        db_booking = models.Booking(user_id=booking.passenger_id, car_id=booking.car_id, booking_date=booking.booking_date, booking_time=booking.booking_time, pickup_location=booking.pickup_location, dropoff_location=booking.dropoff_location)
        db.add(db_booking)
        db.commit()
        db.refresh(db_booking)
    except:
        db.rollback()
        raise
    return db_booking

def get_location(db: Session, location_id: int):
    return db.query(models.Location).filter(models.Location.location_id == location_id).first()

def view_past_bookings_by_user(db: Session, user_id: int):
    return db.query(models.Booking).filter(models.Booking.passenger_id == user_id).all()

# register driver
def register_driver(db: Session, driver: schemas.DriverCreate):
    try:
        # db.begin()

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
    except:
        db.rollback()
        raise
    return db_driver


def get_bookings_by_driver(db: Session, driver_id: int):
    return db.query(models.Booking).filter(models.Booking.driver_id == driver_id, models.Booking.status_id == 1).all()

def get_booking_by_id(db: Session, booking_id: int):
    return db.query(models.Booking).filter(models.Booking.booking_id == booking_id).first()

# def accept_booking(db: Session, booking_id: int):
#     db.query(models.Booking).filter(models.Booking.booking_id == booking_id).update({"status_id": 2})
#     db.commit()
#     return db.query(models.Booking).filter(models.Booking.booking_id == booking_id).first()

def complete_ride(db: Session, booking_id: int):
    # T := R(A) -> W(A) -> W(A)
    try:
        # db.begin()
        ongoing_ride = db.query(models.Booking).filter(models.Booking.booking_id == booking_id)
        ongoing_ride.update({"status_id": 2})
        ongoing_ride.update({"completion_datetime": datetime.now()})
        db.commit()
    except:
        db.rollback()
        raise
    return db.query(models.Booking).filter(models.Booking.booking_id == booking_id).first()

def cancel_ride(db: Session, booking_id: int):
    try:
        # db.begin()
        db.query(models.Booking).filter(models.Booking.booking_id == booking_id).update({"status_id": 3})
        db.commit()
    except:
        db.rollback()
        raise
    return db.query(models.Booking).filter(models.Booking.booking_id == booking_id).first()

def rate_ride(db: Session, booking_id: int, review: schemas.ReviewCreate):
    try:
        # db.begin()

        # First, create a review object in the Review table
        db_review = models.Review(star_review=review.star_review, feedback=review.feedback)
        db.add(db_review)
        db.flush()
        db.refresh(db_review)

        # Then, update the booking object with the review_id
        db.query(models.Booking).filter(models.Booking.booking_id == booking_id).update({"review_id": db_review.review_id})
        db.commit()
    except:
        db.rollback()
        raise
    return db.query(models.Booking).filter(models.Booking.booking_id == booking_id).first()

def view_past_bookings_by_driver(db: Session, driver_id: int):
    past_bookings = db.query(models.Booking).filter(models.Booking.driver_id == driver_id).all()
    return past_bookings

def get_ongoing_booking_by_user(db: Session, user_id: int):
    return db.query(models.Booking).filter(models.Booking.passenger_id == user_id, models.Booking.status_id == 1).first()

def new_booking(db: Session, booking: schemas.BookingCreate, user_id: int):

    # Calculate fare and distance
    fare, distance = calculate_fare_distance(booking.pickup_location_id, booking.dropoff_location_id)

    try:
        # if a transaction is already in progress, then the following line will raise an exception
        # db.begin()
        # Initiate payment
        db_payment = initiate_payment(db, fare)

        # Find available driver
        available_driver_id = None

        # Get the list of driver_id's from the driver table
        driver_ids = db.query(models.Driver.driver_id).all()

        # Iterate through driver_ids, and if either there is no entry in booking for that driver_id, or if the status_id is not 1, then assign that driver_id to available_driver_id and break out of the loop
        for driver_id in driver_ids:
            # If there is no entry in booking for that driver_id, then assign that driver_id to available_driver_id and break out of the loop
            if db.query(models.Booking).filter(models.Booking.driver_id == driver_id[0]).first() == None:
                available_driver_id = driver_id[0]
                break
            # If there is an entry in booking for that driver_id, but the status_id is not 1, then assign that driver_id to available_driver_id and break out of the loop
            elif db.query(models.Booking).filter(models.Booking.driver_id == driver_id[0], models.Booking.status_id == 1).all() is None:
                available_driver_id = driver_id[0]
                break

        db_booking = models.Booking(
            passenger_id=user_id,
            driver_id=available_driver_id,
            pickup_location_id=booking.pickup_location_id,
            dropoff_location_id=booking.dropoff_location_id,
            booking_datetime = datetime.now(),
            completion_datetime = datetime.now() + timedelta(days=1),
            payment_id=db_payment.payment_id,
            fare=fare,
            distance=distance,
            status_id=1
            )
        db.add(db_booking)
        db.commit()
        db.refresh(db_booking)
    except:
        db.rollback()
        raise
    return db_booking

def calculate_fare_distance(location_id_1: int, location_id_2: int):
    distance = abs(location_id_1 - location_id_2)
    fare = distance * 40
    return (fare, distance)

def initiate_payment(db: Session, fare: int):
    try:
        # db.begin()
        db_payment = models.Payment(
            payment_datetime=datetime.now(),
            payment_method=random.choice(["Cash", "Card", "UPI"]),
            payment_amount=fare
        )
        db.add(db_payment)
        db.commit()
        db.refresh(db_payment)
    except:
        db.rollback()
        raise
    return db_payment