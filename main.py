from typing import List

from fastapi import Depends, FastAPI, HTTPException, UploadFile
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/login", response_model=schemas.User)
def login_user(email: str, password: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_login(db, email=email, password=password)
    if db_user is None:
        raise HTTPException(
            status_code=404, detail="Password or email are incorrect")
    return db_user


@app.post("/workouts", response_model=schemas.Workout)
def create_workout_for_user(
        user_id: int, workout: schemas.WorkoutCreate, db: Session = Depends(get_db)):
    return crud.create_workout(db=db, workout=workout, user_id=user_id)


@app.get("/workouts", response_model=List[schemas.Workout])
def get_workout_for_me_and_friends(
        user_id: int, db: Session = Depends(get_db)):
    return crud.get_feed(db=db, user_id=user_id)


@app.get("/workouts/images", response_model=List[schemas.Image])
def get_workout_images(
        workout_id: int, db: Session = Depends(get_db)):
    return crud.get_images(db=db, workout_id=workout_id)


@app.get("/workouts/coords", response_model=List[schemas.CoordinatesBase])
def get_workout_coordinates(
        workout_id: int, db: Session = Depends(get_db)):
    return crud.get_coords(db=db, workout_id=workout_id)


@app.post("/friends", response_model=schemas.User)
def add_friend(user_id: int, friend_id: int, db: Session = Depends(get_db)):
    db_friend = crud.get_friends(db, user_id)
    friend_list = [friend.id for friend in db_friend]
    if friend_id in friend_list or user_id == friend_id:
        raise HTTPException(
            status_code=400, detail="Friend can not be registered")
    return crud.get_user(db=db, user_id=crud.create_friend(db=db, user_id=user_id, friend_id=friend_id).friend_id)


@app.get("/friends", response_model=List[schemas.User])
def get_friends(user_id: int, db: Session = Depends(get_db)):
    return crud.get_friends(db, user_id)
