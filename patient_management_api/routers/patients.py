from fastapi import APIRouter,Path, HTTPException,Query,Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import get_db
from models import PatientDB
from schemas import Patient, PatientUpdate

router = APIRouter()


@router.get("/view")
def view(db:Session=Depends(get_db)):
    rows=db.query(PatientDB).all()
    return [Patient.model_validate(row).model_dump(exclude={'id'}) for row in rows]

@router.get("/patient/{patient_id}")
def view_patient(patient_id:str=Path(...,description='ID of the patient in the DB',examples=['P001']),db:Session=Depends(get_db)):
    row=db.query(PatientDB).filter(PatientDB.id==patient_id).first()
    if not row:
        raise HTTPException(status_code=404,detail='patient not found')
    return Patient.model_validate(row).model_dump(exclude={'id'})    

@router.get('/sort')
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

@router.post('/create')
def create_patient(patient:Patient,db:Session=Depends(get_db)):
    new_patient=PatientDB(**patient.model_dump(exclude={"bmi", "verdict"}))
    db.add(new_patient)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail='Patient already exists')
    return JSONResponse(status_code=201,content={'message':'patient created successfully'})

@router.put('/edit/{patient_id}')
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

@router.delete('/delete/{patient_id}')
def delete_patient(patient_id:str,db:Session=Depends(get_db)):
    row=db.query(PatientDB).filter(PatientDB.id==patient_id).first()
    if not row:
        raise HTTPException(status_code=404,detail='patient not found')
    db.delete(row)
    db.commit()
    return JSONResponse(status_code=200,content={'message':'patient deleted successfully'})