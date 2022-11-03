from sqlalchemy import Column, ForeignKey, Integer, String, Float, BLOB, DateTime
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    name = Column(String, default=True)

    workout_list = relationship("Workout", back_populates="owner")
    friends_list = relationship("Friend", back_populates="my_friends")


class Workout(Base):
    __tablename__ = "workout"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("people.id"))
    time = Column(Integer)
    distance = Column(Float)
    speed = Column(Float)
    date = Column(DateTime)
    description = Column(String)

    owner = relationship("User", back_populates="workout_list")
    images = relationship("Image", back_populates="my_image")
    coords_list = relationship("Coordinates", back_populates="workout_path")


class Coordinates(Base):
    __tablename__ = "coords"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    workout_id = Column(Integer, ForeignKey("workout.id"), index=True)
    latitude = Column(Float)
    longitude = Column(Float)

    workout_path = relationship("Workout", back_populates="coords_list")


class Friend(Base):
    __tablename__ = "friends"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("people.id"), index=True)
    friend_id = Column(Integer, index=True)

    my_friends = relationship("User", back_populates="friends_list")


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    workout_id = Column(Integer, ForeignKey("workout.id"), index=True)
    image = Column(String)
    name = Column(String)

    my_image = relationship("Workout", back_populates="images")
