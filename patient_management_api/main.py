from fastapi import FastAPI
from database import engine, Base
import models
from routers import patients

app=FastAPI()

Base.metadata.create_all(bind=engine)

@app.get('/')
def hello():
    return {"message":"Patient Management System API"}

@app.get("/about")
def about():
    return {"message":"A fully functional API to manage your patient records"}

app.include_router(patients.router)

