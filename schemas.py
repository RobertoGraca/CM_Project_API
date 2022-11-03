from datetime import datetime
from typing import List, Union

from pydantic import BaseModel


class CoordinatesBase(BaseModel):
    latitude: float
    longitude: float


class CoordinatesCreate(CoordinatesBase):
    pass


class Coordinates(CoordinatesBase):
    id: int
    workout_id: int

    class Config:
        orm_mode = True


class FriendBase(BaseModel):
    friend_id: int


class FriendCreate(FriendBase):
    pass


class Friend(FriendBase):
    user_id: int
    id: int

    class Config:
        orm_mode = True


class ImageBase(BaseModel):
    name: str


class ImageCreate(ImageBase):
    id: int


class ImageIdentification(ImageBase):
    image: str


class Image(ImageIdentification):
    workout_id: int

    class Config:
        orm_mode = True


class WorkoutBase(BaseModel):
    time: int
    distance: float
    speed: float
    date: datetime
    description: str


class WorkoutCreate(WorkoutBase):
    images: List[ImageIdentification]
    coords: List[CoordinatesCreate]


class Workout(WorkoutBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    name: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
