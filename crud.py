from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import UploadFile
import models
import schemas

# ------------------------ CREATE ------------------------------

# ------ USER ----------


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name,
                          email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# ------ WORKOUT -------
def create_workout(db: Session, workout: schemas.WorkoutCreate, user_id: int):
    db_workout = models.Workout(**{"time": workout.time, "distance": workout.distance, "speed": workout.speed,
                                   "date": workout.date, "description": workout.description}, p_id=user_id)

    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)

    t_id = db.query(models.Workout).filter(
        models.Workout.p_id == user_id).order_by(models.Workout.date).first().id

    for coord in workout.coords:
        db_coords = models.Coordinates(
            **{"latitude": coord.latitude, "longitude": coord.longitude}, t_id=t_id)
        db.add(db_coords)
        db.commit()
        db.refresh(db_coords)

    return db_workout


# -------- FRIEND ---------
def create_friend(db: Session, p_id: int, f_id: int):
    db_friend = models.Friend(**{"p_id": p_id, "f_id": f_id})
    db.add(db_friend)

    db_friend2 = models.Friend(**{"p_id": f_id, "f_id": p_id})
    db.add(db_friend2)
    db.commit()
    db.refresh(db_friend)
    db.refresh(db_friend2)
    return [db_friend, db_friend2]


# --------- IMAGE -----------
async def create_images(db: Session, workout_id: int, images: List[UploadFile]):
    db_images = []
    for image in images:
        img = models.Image(
            **{"image": str(await image.read())}, t_id=workout_id, name=image.filename)
        db.add(img)
        db.commit()
        db.refresh(img)
        db_images.append(schemas.ImageBase(name=image.filename, id=img.id))
    return db_images
# ----------------------- GET ---------------------------------

# -------- USER -----------


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_login(db: Session, email: str, password: str):
    return db.query(models.User).filter_by(email=email, password=password).first()


# --------- WORKOUT ---------------
def get_feed(db: Session, user_id: int):
    friends = db.query(models.Friend).filter(
        models.Friend.p_id == user_id).all()
    friend_list = [friend.f_id for friend in friends]

    a = db.query(models.Workout) \
        .filter(or_(models.Workout.p_id == user_id, models.Workout.p_id.in_(friend_list))) \
        .order_by(models.Workout.date).all()

    return a


# ------ FRIEND -------------
def get_friends(db: Session, user_id: int):
    return db.query(models.Friend.f_id).filter(models.Friend.p_id == user_id).all()


# -------- IMAGE ---------
def get_images(db: Session, workout_id: int):
    return db.query(models.Image).filter(models.Image.t_id == workout_id).all()


# -------- COORDINATES ---------
def get_coords(db: Session, workout_id: int):
    return db.query(models.Coordinates.latitude, models.Coordinates.longitude).filter(models.Coordinates.t_id == workout_id).all()
