from fastapi import FastAPI,Path, HTTPException,Query,Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field,ConfigDict
from typing import Annotated,Literal,Optional
from sqlalchemy import create_engine, Column, String,Integer,Float
from sqlalchemy.orm import sessionmaker, declarative_base,Session
from sqlalchemy.exc import IntegrityError

app=FastAPI()

DB_URL="sqlite:///patient.db"
engine=create_engine(DB_URL,connect_args={"check_same_thread":False})
sessionLocal=sessionmaker(bind=engine)
Base=declarative_base()

class PatientDB(Base):
    __tablename__="patient"
    id=Column(String,primary_key=True)
    name=Column(String)
    city=Column(String)
    age =Column(Integer)
    gender=Column(String)
    height=Column(Float)
    weight=Column(Float)

Base.metadata.create_all(bind=engine)

def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()

class Patient(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id:Annotated[str,Field(...,description='ID of the patient', examples=['P001'])]
    name:Annotated[str,Field(...,description='Name of the patient')]
    city:Annotated[str,Field(...,description='City where the patient is living')]
    age:Annotated[int,Field(...,gt=0,lt=120,description='Age of the patient')]
    gender:Annotated[Literal['male','female','other'],Field(...,description='Gender of the patient')]
    height:Annotated[float,Field(...,gt=0,description='Height of the patient in mtrs')]
    weight:Annotated[float,Field(...,gt=0,description='Weight of the patient in kgs')]

    @computed_field
    @property
    def bmi(self)->float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi

    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi<18.5:
            return 'Underweight'
        elif self.bmi<25:
            return 'Normal'
        elif self.bmi<30:
            return 'Overweight'
        else:
            return 'Obese'

class PatientUpdate(BaseModel):
    name:Annotated[Optional[str],Field(default=None)]
    city:Annotated[Optional[str],Field(default=None)]
    age:Annotated[Optional[int],Field(default=None,gt=0,lt=120)]
    gender:Annotated[Optional[Literal['male','female','other']],Field(default=None)]
    height:Annotated[Optional[float],Field(default=None,gt=0)]
    weight:Annotated[Optional[float],Field(default=None,gt=0)]


@app.get('/')
def hello():
    return {"message":"Patient Management System API"}

@app.get("/about")
def about():
    return {"message":"A fully functional API to manage your patient records"}

@app.get("/view")
def view(db:Session=Depends(get_db)):
    rows=db.query(PatientDB).all()
    return [Patient.model_validate(row).model_dump(exclude={'id'}) for row in rows]

@app.get("/patient/{patient_id}")
def view_patient(patient_id:str=Path(...,description='ID of the patient in the DB',example='P001'),db:Session=Depends(get_db)):
    row=db.query(PatientDB).filter(PatientDB.id==patient_id).first()
    if not row:
        raise HTTPException(status_code=404,detail='patient not found')
    return Patient.model_validate(row).model_dump(exclude={'id'})    

@app.get('/sort')
def sort_patients(sort_by:str =Query(...,description='Sort on the basis of height, weight or bmi'),order:str=Query('asc',description='Sort in asc or desc order'),db:Session=Depends(get_db)):
    sort_columns={
        "height": PatientDB.height,
        "weight": PatientDB.weight,
        "bmi": PatientDB.weight/(PatientDB.height*PatientDB.height)}

    if sort_by not in sort_columns:
        raise HTTPException(status_code=400,detail=f'Invalid field select from {list(sort_columns)}')
    
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail=f'Invalid order select between asc and desc')
    
    column = sort_columns[sort_by]
    column = column.desc() if order == "desc" else column.asc()
    rows = db.query(PatientDB).order_by(column).all()
    return [Patient.model_validate(row).model_dump(exclude={'id'}) for row in rows]

@app.post('/create')
def create_patient(patient:Patient,db:Session=Depends(get_db)):
    new_patient=PatientDB(**patient.model_dump(exclude={"bmi", "verdict"}))
    db.add(new_patient)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail='Patient already exists')
    return JSONResponse(status_code=201,content={'message':'patient created successfully'})

@app.put('/edit/{patient_id}')
def update_patient(patient_id:str,patient_update:PatientUpdate,db:Session=Depends(get_db)):
    row=db.query(PatientDB).filter(PatientDB.id==patient_id).first()
    if not row:
        raise HTTPException(status_code=404,detail='patient not found')
    merged=Patient.model_validate(row).model_dump(exclude={"bmi","verdict"})
    merged.update(patient_update.model_dump(exclude_unset=True))
    p=Patient(**merged) 
    for field in ("name", "city", "age", "gender", "height", "weight"):
        setattr(row, field, getattr(p, field))
    db.commit()
    return JSONResponse(status_code=200,content={'message':'patient updated successfully'})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:str,db:Session=Depends(get_db)):
    row=db.query(PatientDB).filter(PatientDB.id==patient_id).first()
    if not row:
        raise HTTPException(status_code=404,detail='patient not found')
    db.delete(row)
    db.commit()
    return JSONResponse(status_code=200,content={'message':'patient deleted successfully'})