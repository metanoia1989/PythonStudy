#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from enum import Enum
from fastapi import FastAPI

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"
    
app = FastAPI()

@app.get("/model/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return { "model_name": model_name, "message": "Deep Learning FTW!" }

    if model_name.value == "lenet":
        return { "model_name": model_name, "message": "LeCNN all the images!" }
    
    return { "model_name": model_name, "message": "Have some residuals" }
        

@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return { "file_path": file_path }