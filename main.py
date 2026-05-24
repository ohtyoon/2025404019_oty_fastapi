from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os

app = FastAPI()

FILE_PATH = "courses.json"

class Course(BaseModel):
    course_name: str
    year: str
    semester: str
    grade: str

def load_data():
    if not os.path.exists(FILE_PATH):
        return []
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_data(data):
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@app.get("/courses")
def get_courses():
    data = load_data()
    return data


@app.get("/courses")
@app.post("/courses")
def create_course(course: Course):
    try:
        data = load_data()
        
        data.append(course.model_dump())
        
        save_data(data)
        return {"message": "수강기록이 성공적으로 추가되었습니다.", "inserted": course}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 내부 오류: {str(e)}")