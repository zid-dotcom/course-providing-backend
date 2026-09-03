import os
import shutil
import json

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form
)

from sqlalchemy.orm import Session

from database import SessionLocal
from database_models import Course

from schemas.course import CourseResponse

from routers.auth import get_current_admin


router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)


# ==========================================
# DATABASE DEPENDENCY
# ==========================================

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# ==========================================
# UPLOAD DIRECTORY
# ==========================================

UPLOAD_DIR = "uploads/courses"

os.makedirs(UPLOAD_DIR, exist_ok=True)


# ==========================================
# GET ALL COURSES
# PUBLIC
# ==========================================

@router.get(
    "/",
    response_model=list[CourseResponse]
)
def get_all_courses(
    db: Session = Depends(get_db)
):

    courses = db.query(Course).filter(
        Course.is_active == True
    ).all()

    return courses


# ==========================================
# GET COURSE BY ID
# PUBLIC
# ==========================================

@router.get(
    "/{course_id}",
    response_model=CourseResponse
)
def get_course(
    course_id: int,
    db: Session = Depends(get_db)
):

    course = db.query(Course).filter(
        Course.id == course_id
    ).first()

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return course


# ==========================================
# ADD COURSE
# ADMIN ONLY
# ==========================================

@router.post(
    "/",
    response_model=CourseResponse
)
def add_course(
    title: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    duration: str = Form(...),
    category: str = Form(...),
    level: str = Form(...),

    # Curriculum comes as JSON string
    curriculum: str = Form(...),

    image: UploadFile = File(...),

    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):

    # ==========================================
    # CONVERT CURRICULUM JSON STRING
    # ==========================================

    try:
        curriculum_data = json.loads(curriculum)

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400,
            detail="Invalid curriculum JSON"
        )


    # ==========================================
    # SAVE IMAGE
    # ==========================================

    filename = image.filename

    file_path = os.path.join(
        UPLOAD_DIR,
        filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            image.file,
            buffer
        )


    # ==========================================
    # SAVE COURSE
    # ==========================================

    new_course = Course(
        title=title,
        description=description,
        price=price,
        duration=duration,
        category=category,
        level=level,
        curriculum=curriculum_data,
        image=file_path
    )

    db.add(new_course)

    db.commit()

    db.refresh(new_course)

    return new_course


# ==========================================
# UPDATE COURSE
# ADMIN ONLY
# ==========================================

@router.put(
    "/{course_id}",
    response_model=CourseResponse
)
def update_course(
    course_id: int,

    title: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    duration: str = Form(...),
    category: str = Form(...),
    level: str = Form(...),

    curriculum: str = Form(...),

    image: UploadFile | None = File(None),

    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    

    # ==========================================
    # FIND COURSE
    # ==========================================

    db_course = db.query(Course).filter(
        Course.id == course_id
    ).first()

    if not db_course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )


    # ==========================================
    # CONVERT CURRICULUM
    # ==========================================

    try:
        curriculum_data = json.loads(curriculum)

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400,
            detail="Invalid curriculum JSON"
        )


    # ==========================================
    # UPDATE TEXT FIELDS
    # ==========================================

    db_course.title = title
    db_course.description = description
    db_course.price = price
    db_course.duration = duration
    db_course.category = category
    db_course.level = level
    db_course.curriculum = curriculum_data


    # ==========================================
    # UPDATE IMAGE IF PROVIDED
    # ==========================================

    if image:

        filename = image.filename

        file_path = os.path.join(
            UPLOAD_DIR,
            filename
        )

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(
                image.file,
                buffer
            )

        db_course.image = file_path


    # ==========================================
    # SAVE CHANGES
    # ==========================================

    db.commit()

    db.refresh(db_course)

    return db_course


# ==========================================
# DELETE COURSE
# ADMIN ONLY
# ==========================================

@router.delete("/{course_id}")
def delete_course(
    course_id: int,

    db: Session = Depends(get_db),

    admin=Depends(get_current_admin)
):

    db_course = db.query(Course).filter(
        Course.id == course_id
    ).first()

    if not db_course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    db.delete(db_course)

    db.commit()

    return {
        "message": "Course deleted successfully"
    }