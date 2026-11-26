# Patient Management API

A REST API built with FastAPI to manage patient records. Data is stored in a SQLite, and BMI and a health verdict are calculated automatically.

## Features
- Create, view, update and delete patient records
- Automatic BMI and verdict (Underweight / Normal / Overweight / Obese)
- Sort patients by height, weight or BMI and order by asc or desc
- Input validation with Pydantic
- Interactive API docs at `/docs`

## Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/about` | About the API |
| GET | `/view` | View all patients |
| GET | `/patient/{patient_id}` | View one patient |
| GET | `/sort?sort_by=bmi&order=desc` | Sort by height, weight or bmi and order by asc or desc|
| POST | `/create` | Add a new patient |
| PUT | `/edit/{patient_id}` | Update a patient |
| DELETE | `/delete/{patient_id}` | Delete a patient |

## Sample patient

```json
{
  "id": "P001",
  "name": "Riya",
  "city": "Delhi",
  "age": 22,
  "gender": "female",
  "height": 1.65,
  "weight": 58
}
```

`bmi` and `verdict` are computed by the API, so they are not sent in the request.

## How to run

```
python -m venv venv
venv\Scripts\activate
fastapi dev main.py
```

Then open http://127.0.0.1:8000/docs to try the endpoints.

## Tech used
Python, FastAPI, Pydantic