from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric, DateTime
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = "user"
    
    user_id = Column(Integer, primary_key=True, index=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    phone_number = Column(String(50), nullable=False, unique=True)

class Car(Base):
    __tablename__ = "car"
    
    car_id = Column(Integer, primary_key=True, index=True, nullable=False)
    car_type = Column(String(50), nullable=False)
    vin_number = Column(String(50), nullable=False, unique=True)
    
class Review(Base):
    __tablename__ = "review"
    
    review_id = Column(Integer, primary_key=True, index=True, nullable=False)
    #check the star_review attribute to be between 1 and 5
    star_review = Column(Integer, nullable=False)
    feedback = Column(String(500))

class Location_coords(Base):
    __tablename__ = "location_coords"
    
    location_id = Column(Integer, primary_key=True, index=True, nullable=False)
    latitude = Column(Numeric(18,15), nullable=False)
    longitude = Column(Numeric(18,15), nullable=False)

class Payment(Base):
    __tablename__ = "payment"
    
    payment_id = Column(Integer, primary_key=True, index=True, nullable=False)
    payment_datetime = Column(DateTime, nullable=False)
    payment_method = Column(String(10), nullable=False)
    payment_amount = Column(Integer, nullable=False)

class Driver(Base):
    __tablename__ = "driver"
    
    driver_id = Column(Integer, primary_key=True, index=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    phone_number = Column(String(12), nullable=False)
    gender = Column(String(1), nullable=False)
    license_number = Column(String(18), nullable=False, unique=True)
    rating = Column(Numeric(3,2), nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    car_id = Column(Integer, ForeignKey("car.car_id"), nullable=False)
    location_id = Column(Integer, ForeignKey("location_coords.location_id"), nullable=False)
    

class Booking_status(Base):
    __tablename__ = "booking_status"
    
    status_id = Column(Integer, primary_key=True, index=True, nullable=False, unique=True)
    status_name = Column(String(16), nullable=False, unique=True)

class Booking(Base):
    __tablename__ = "booking"
    
    booking_id = Column(Integer, primary_key=True, index=True, nullable=False, unique=True)
    passenger_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    driver_id = Column(Integer, ForeignKey("driver.driver_id"), nullable=False)
    pickup_location_id = Column(Integer, ForeignKey("location_coords.location_id"), nullable=False)
    dropoff_location_id = Column(Integer, ForeignKey("location_coords.location_id"), nullable=False)
    booking_datetime = Column(DateTime, nullable=False)
    completion_datetime = Column(DateTime, nullable=False)
    payment_id = Column(Integer, ForeignKey("payment.payment_id"), nullable=False)
    fare = Column(Numeric(10,2), nullable=False)
    distance = Column(Numeric(4,1), nullable=False)
    status_id = Column(Integer, ForeignKey("booking_status.status_id"), nullable=False)
    review_id = Column(Integer, ForeignKey("review.review_id"))




