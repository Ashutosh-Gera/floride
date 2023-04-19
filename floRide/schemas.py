import datetime
from typing import List, Optional
from pydantic import BaseModel, validator, constr, PositiveInt
from decimal import Decimal

#This file is to store all the pydantic schemas that we make
#This is a pydantic model i.e a class that inherits from BaseModel and 
# we use it to define the data types of the attributes of the class

# class Blog(BaseModel):
#     title : str
#     body : str

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str 
    phone_number: constr(max_length=12)

class UserLogin(BaseModel):
    email: str

class UserCreate(UserBase):
    #password: str
    pass


class User(UserBase):
    user_id: PositiveInt

    class Config:
        orm_mode = True


class CarBase(BaseModel):
    car_type: str
    vin_number: str


class CarCreate(CarBase):
    pass


class Car(CarBase):
    car_id: PositiveInt

    class Config:
        orm_mode = True


class ReviewBase(BaseModel):
    star_review: int
    feedback: Optional[str]

    _validate_star_review = validator("star_review", allow_reuse=True)(lambda v: 1 <= v <= 5)


class ReviewCreate(ReviewBase):
    pass


class Review(ReviewBase):
    review_id: PositiveInt

    class Config:
        orm_mode = True


class LocationCoordsBase(BaseModel):
    latitude: Decimal
    longitude: Decimal


class LocationCoordsCreate(LocationCoordsBase):
    pass


class LocationCoords(LocationCoordsBase):
    location_id: PositiveInt

    class Config:
        orm_mode = True


class PaymentBase(BaseModel):
    payment_datetime: datetime.datetime
    payment_method: str
    payment_amount: int


class PaymentCreate(PaymentBase):
    pass


class Payment(PaymentBase):
    payment_id: PositiveInt

    class Config:
        orm_mode = True


class DriverBase(BaseModel):
    first_name: str
    last_name: str
    email: str 
    phone_number: constr(max_length=12)
    gender: constr(max_length=1)
    license_number: str
    rating: Decimal
    date_of_birth: datetime.datetime
    car_id: PositiveInt
    location_id: PositiveInt


class DriverCreate(DriverBase):
    # password: str
    pass


class Driver(DriverBase):
    driver_id: PositiveInt
    car: Optional[Car] = None
    location_coords: Optional[LocationCoords] = None

    class Config:
        orm_mode = True


class BookingStatusBase(BaseModel):
    status_name: str


class BookingStatusCreate(BookingStatusBase):
    pass


class BookingStatus(BookingStatusBase):
    status_id: PositiveInt

    class Config:
        orm_mode = True


class BookingBase(BaseModel):
    passenger_id: PositiveInt
    driver_id: PositiveInt
    pickup_location_id: PositiveInt
    dropoff_location_id: PositiveInt
    booking_datetime: datetime.datetime
    completion_datetime: datetime.datetime
    payment_id: PositiveInt
    fare: Decimal
    distance: Decimal
    status_id: PositiveInt
    review_id: Optional[PositiveInt]


class BookingCreate(BookingBase):
    pass


class Booking(BookingBase):
    booking_id: PositiveInt
    passenger: Optional[User] = None
    driver: Optional[Driver] = None
    pickup_location: Optional[LocationCoords] = None
    dropoff_location: Optional[LocationCoords] = None
    payment: Optional[Payment] = None
    status: Optional[BookingStatus] = None
    review: Optional[Review] = None

    class Config:
        orm_mode = True
