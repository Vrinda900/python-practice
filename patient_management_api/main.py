from fastapi import FastAPI,Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional
import sqlite3

DB_File="patient.db"
def get_connection():
    conn=sqlite3.connect(DB_File)
    conn.row_factory=sqlite3.Row     
    return conn

def create_table():
    conn=get_connection()
    conn.execute("""CREATE TABLE IF NOT EXISTS patient(
    id TEXT PRIMARY KEY,
    name TEXT,
    city TEXT,
    age INTEGER,
    gender TEXT,
    height REAL,
    weight REAL
)
""")  
    conn.commit()
    conn.close()
    
create_table() 

app=FastAPI()

class Patient(BaseModel):
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
def view():
    conn=get_connection()
    rows= conn.execute("SELECT * FROM patient").fetchall()
    conn.close()
    result={}
    for row in rows:
        patient=Patient(**dict(row))
        result[patient.id]=patient.model_dump(exclude={'id'})
    return result

@app.get("/patient/{patient_id}")
def view_patient(patient_id:str=Path(...,description='ID of the patient in the DB',example='P001')):
    conn=get_connection()
    row= conn.execute("SELECT * FROM patient WHERE id = ?", (patient_id,)).fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404,detail='patient not found')
    patient = Patient(**dict(row))
    return patient.model_dump(exclude={'id'})      

@app.get('/sort')
def sort_patients(sort_by:str =Query(...,description='Sort on the basis of height, weight or bmi'),order:str=Query('asc',description='Sort in asc or desc order')):
    sort_columns={"height": "height","weight": "weight","bmi": "weight/(height*height)"}

    if sort_by not in sort_columns:
        raise HTTPException(status_code=400,detail=f'Invalid field select from {list(sort_columns)}')
    
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail=f'Invalid order select between asc and desc')
    
    odr="DESC" if order=="desc" else "ASC"
    conn= get_connection()
    rows= conn.execute(f"SELECT * FROM patient ORDER BY {sort_columns[sort_by]} {odr}").fetchall()
    conn.close()
    result={}
    for row in rows:
        patient=Patient(**dict(row))
        result[patient.id]=patient.model_dump(exclude={'id'})
    return result

@app.post('/create')
def create_patient(patient:Patient):
    conn=get_connection()
    try:
        conn.execute("INSERT INTO patient(id,name,city,age,gender,height,weight) VALUES (?,?,?,?,?,?,?)",(patient.id,patient.name,patient.city,patient.age,patient.gender,patient.height,patient.weight))
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400,detail='Patient already exists')
    finally:
        conn.close()
    return JSONResponse(status_code=201,content={'message':'patient created successfully'})

@app.put('/edit/{patient_id}')
def update_patient(patient_id:str,patient_update:PatientUpdate):
    conn=get_connection()
    try:
        row=conn.execute("SELECT * FROM patient WHERE id = ?", (patient_id,)).fetchone()
        if row is None:
            raise HTTPException(status_code=404,detail='patient not found')
    finally:
        conn.close()
    merged=dict(row)
    merged.update(patient_update.model_dump(exclude_unset=True))
    p=Patient(**merged)
    conn=get_connection()
    conn.execute("UPDATE patient SET name=? , city=? , age=?, gender=? , height=? , weight=? WHERE id=?",(p.name,p.city,p.age,p.gender,p.height,p.weight,patient_id))    
    conn.commit()
    conn.close()
    return JSONResponse(status_code=200,content={'message':'patient updated successfully'})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:str):
    conn=get_connection()
    cursor=conn.execute("DELETE FROM patient WHERE id = ?", (patient_id,))
    conn.commit()
    deleted=cursor.rowcount
    conn.close()
    if deleted==0:
        raise HTTPException(status_code=404,detail='patient not found')
    return JSONResponse(status_code=200,content={'message':'patient deleted successfully'})