#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.schema import ForeignKey
import settings
from pydantic import BaseModel
from pydantic import EmailStr

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
BaseModel = declarative_base()

# 数据库模型类
class User(BaseModel):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    lname = Column(String)
    fname = Column(String)
    email = Column(String, unique=True, index=True)
    todos = relationship("TODO", back_populates="onwer", cascade="all, delete-orphan")
    
class TODO(BaseModel):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    completed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="todos")
    
# 参数验证模型
class UserBase(BaseModel):
    email: EmailStr
    
class UserCreate(UserBase):
    lname: str
    fname: str
    password: str
    
class TODOCreate(BaseModel):
    text: str
    completed: bool
    
class TODOUpdate(TODOCreate):
    id: int