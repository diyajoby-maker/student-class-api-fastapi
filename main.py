from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4, UUID

app = FastAPI()

# ---------- Models ----------
class Student(BaseModel):
    first_name: str
    middle_name: str = None
    last_name: str
    age: int
    city: str

class StudentUpdate(BaseModel):
    first_name: str = None
    middle_name: str = None
    last_name: str = None
    age: int = None
    city: str = None

# ---------- Fake Database ----------
students_db = {}

# ---------- Routes ----------
@app.get("/")
def read_root():
    return {"message": "Welcome to the Student API!"}

@app.post("/students/")
def create_student(student: Student):
    student_id = str(uuid4())
    students_db[student_id] = student.dict()
    return {"id": student_id, "student": students_db[student_id]}

@app.put("/students/{student_id}")
def update_student(student_id: str, updated_data: StudentUpdate):
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    
    for key, value in updated_data.dict(exclude_unset=True).items():
        students_db[student_id][key] = value
    
    return {"id": student_id, "updated_student": students_db[student_id]}

@app.delete("/students/{student_id}")
def delete_student(student_id: str):
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    
    deleted = students_db.pop(student_id)
    return {"message": "Student deleted", "deleted_student": deleted}



# ---------- Class Models ----------
class ClassInfo(BaseModel):
    class_name: str
    description: str
    start_date: str  # Format: YYYY-MM-DD
    end_date: str
    hours: int

class ClassUpdate(BaseModel):
    class_name: str = None
    description: str = None
    start_date: str = None
    end_date: str = None
    hours: int = None

# ---------- Class Database ----------
classes_db = {}

# ---------- Class Routes ----------
@app.post("/classes/")
def create_class(class_info: ClassInfo):
    class_id = str(uuid4())
    classes_db[class_id] = class_info.dict()
    return {"id": class_id, "class": classes_db[class_id]}

@app.put("/classes/{class_id}")
def update_class(class_id: str, updated_data: ClassUpdate):
    if class_id not in classes_db:
        raise HTTPException(status_code=404, detail="Class not found")
    
    for key, value in updated_data.dict(exclude_unset=True).items():
        classes_db[class_id][key] = value

    return {"id": class_id, "updated_class": classes_db[class_id]}

@app.delete("/classes/{class_id}")
def delete_class(class_id: str):
    if class_id not in classes_db:
        raise HTTPException(status_code=404, detail="Class not found")
    
    deleted = classes_db.pop(class_id)
    return {"message": "Class deleted", "deleted_class": deleted}




# ---------- Student-Class Registration ----------
registrations = {}  # class_id → list of student_ids

@app.post("/register/")
def register_student_to_class(student_id: str, class_id: str):
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    if class_id not in classes_db:
        raise HTTPException(status_code=404, detail="Class not found")
    
    if class_id not in registrations:
        registrations[class_id] = []

    if student_id in registrations[class_id]:
        return {"message": "Student already registered"}

    registrations[class_id].append(student_id)
    return {"message": "Student registered", "class_id": class_id, "student_id": student_id}

@app.get("/classes/{class_id}/students")
def get_students_for_class(class_id: str):
    if class_id not in registrations:
        return {"message": "No students registered for this class"}
    
    registered_students = []
    for student_id in registrations[class_id]:
        student = students_db.get(student_id)
        if student:
            registered_students.append({"id": student_id, **student})
    
    return {"class_id": class_id, "students": registered_students}

