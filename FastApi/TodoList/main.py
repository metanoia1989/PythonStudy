#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from fastapi import FastAPI, Depends, HTTPException
from schemas import SessionLocal as Session
import schemas

app = FastAPI()

def get_db():
    """
    provide db session to path operation functions
    """
    try:
        db = Session()
        yield db
    finally:
        db.close()
        
def get_current_user(db: Session = Depends(get_db), 
        token: str = Depends(oauth2_scheme)):
    return decode_access_token(db, token)

@app.post("/api/users", response_model=schemas.User)
def signup(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    add new user
    """
    user = crud.get_user_by_email(db, user_data.email)
    if user:
        raise HTTPException(status_code=409,
            detail="Email already registered.")
    signedup_user = crud.create_user(db, user_data)
    return signedup_user