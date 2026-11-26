# Practice script: SQLite CRUD basics, before moving the API to SQLite

import sqlite3

conn=sqlite3.connect("practice.db")
cursor=conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS patient(
    id Text PRIMARY KEY ,
    name TEXT,
    city TEXT,
    age INTEGER,
    gender TEXT,
    height REAL,
    weight REAL
)
""")
conn.commit()

def add_patient(id,name,city,age,gender,height,weight):
    try:
        cursor.execute("INSERT INTO patient (id,name,city,age,gender,height,weight) VALUES(?,?,?,?,?,?,?)",(id,name,city,age,gender,height,weight))
        conn.commit()
        print("Patient Added")
    except sqlite3.IntegrityError:
        print("Patient already exists")

def view_patient():
    cursor.execute("SELECT * FROM patient")
    for i in cursor.fetchall():
        print(i)

def delete_patient(p_id):
    cursor.execute("DELETE FROM patient WHERE id=?",(p_id,))
    conn.commit()
    if cursor.rowcount==0:
            print("Patient not found")
    else:
        print("Patient Deleted")

ALLOWED = {"name", "city", "age", "gender", "height", "weight"}

def update_patient(p_id,**fields):
    fields={k: v for k, v in fields.items() if k in ALLOWED and v is not None}
    if not fields:
        print("Nothing to update")
        return
    set_clause=", ".join(f"{col} = ?" for col in fields)   
    values=list(fields.values())+[p_id]     

    cursor.execute(f"UPDATE patient SET {set_clause} WHERE id = ?", values)
    conn.commit()
    if cursor.rowcount==0:
        print("Patient not found")
    else:
        print("Patient Updated")

