from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Online Examination System")

# MODELS
# ============================================================

class Student(BaseModel):
    name: str
    email: str
    course: str

class Answer(BaseModel):
    option: int = Field(..., ge=1, le=4)


class ExamSubmission(BaseModel):
    student_id: int

    # Exactly 5 options must be selected.

    options: list[int] = Field(..., min_length=5, max_length=5)

# DATA
# ============================================================
students = [
    {"id": 1, "name": "Aarav", "email": "aarav@gmail.com", "course": "Python"},
    {"id": 2, "name": "Ananya", "email": "ananya@gmail.com", "course": "Python"},
    {"id": 3, "name": "Rahul", "email": "rahul@gmail.com", "course": "Python"},
    {"id": 4, "name": "Sneha", "email": "sneha@gmail.com", "course": "Python"},
    {"id": 5, "name": "Vikram", "email": "vikram@gmail.com", "course": "Python"},
    {"id": 6, "name": "Kavya", "email": "kavya@gmail.com", "course": "Python"},
    {"id": 7, "name": "Aditya", "email": "aditya@gmail.com", "course": "Python"},
    {"id": 8, "name": "Nisha", "email": "nisha@gmail.com", "course": "Python"},
    {"id": 9, "name": "Varun", "email": "varun@gmail.com", "course": "Python"},
    {"id": 10, "name": "Neha", "email": "neha@gmail.com", "course": "Python"},
]

# EXAMS
# ============================================================

exams = [
    {"id": 1, "name": "Python Identifiers"},
    {"id": 2, "name": "Conditional Statements"},
]

# QUESTIONS
# ============================================================

questions = [

    # ---------- Exam 1 ----------

    {
        "id": 1,
        "exam_id": 1,
        "question": "Which of the following is a valid identifier?",
        "options": {
            "1": "student_name",
            "2": "student-name",
            "3": "123student",
            "4": "student name"
        },
        "correct_option": 1
    },

    {
        "id": 2,
        "exam_id": 1,
        "question": "Which character cannot start an identifier?",
        "options": {
            "1": "_",
            "2": "A",
            "3": "1",
            "4": "a"
        },
        "correct_option": 3
    },

    {
        "id": 3,
        "exam_id": 1,
        "question": "Which is a valid variable name?",
        "options": {
            "1": "my-name",
            "2": "my_name",
            "3": "my name",
            "4": "2name"
        },
        "correct_option": 2
    },

    {
        "id": 4,
        "exam_id": 1,
        "question": "Are Python identifiers case-sensitive?",
        "options": {
            "1": "Yes",
            "2": "No",
            "3": "Sometimes",
            "4": "None"
        },
        "correct_option": 1
    },

    {
        "id": 5,
        "exam_id": 1,
        "question": "Which symbol is allowed in an identifier?",
        "options": {
            "1": "@",
            "2": "#",
            "3": "_",
            "4": "$"
        },
        "correct_option": 3
    },


    # ---------- Exam 2 ----------

    {
        "id": 6,
        "exam_id": 2,
        "question": "Which keyword checks a condition?",
        "options": {
            "1": "if",
            "2": "for",
            "3": "def",
            "4": "class"
        },
        "correct_option": 1
    },

    {
        "id": 7,
        "exam_id": 2,
        "question": "Which keyword runs when the if condition is false?",
        "options": {
            "1": "elif",
            "2": "else",
            "3": "for",
            "4": "while"
        },
        "correct_option": 2
    },

    {
        "id": 8,
        "exam_id": 2,
        "question": "Which keyword checks another condition?",
        "options": {
            "1": "else",
            "2": "elif",
            "3": "another",
            "4": "check"
        },
        "correct_option": 2
    },

    {
        "id": 9,
        "exam_id": 2,
        "question": "Which operator checks equality?",
        "options": {
            "1": "=",
            "2": "==",
            "3": "!=",
            "4": ">="
        },
        "correct_option": 2
    },

    {
        "id": 10,
        "exam_id": 2,
        "question": "What is the output of 10 > 5?",
        "options": {
            "1": "False",
            "2": "True",
            "3": "10",
            "4": "5"
        },
        "correct_option": 2
    },
]
# RESULTS
# ============================================================

results = []
# HELPER FUNCTIONS
# ============================================================
def get_assigned_exam_id(student_id: int) -> int:

    if student_id % 2 == 0:
        return 2

    return 1

def find_student(student_id: int):

    for student in students:

        if student["id"] == student_id:
            return student

    return None

def get_questions_for_exam(exam_id: int):

    exam_questions = []

    for q in questions:

        if q["exam_id"] == exam_id:
            exam_questions.append(q)

    return exam_questions
# STUDENT ROUTES
# ============================================================

@app.get("/students")
def get_students():

    return students

@app.get("/students/{student_id}")
def get_student(student_id: int):

    student = find_student(student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student

@app.post("/students")
def add_student(student: Student):

    new_student = {
        "id": len(students) + 1,
        "name": student.name,
        "email": student.email,
        "course": student.course
    }

    students.append(new_student)

    return {
        "message": "Student added",
        "student": new_student
    }

@app.put("/students/{student_id}")
def update_student_email(student_id: int, email: str):

    student = find_student(student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    student["email"] = email

    return {
        "message": "Email updated",
        "student": student
    }

@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    student = find_student(student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    students.remove(student)

    return {
        "message": "Student deleted"
    }
# EXAM ROUTES
# ============================================================
@app.get("/exams")
def get_exams():

    return exams

# ASSIGNED EXAM
# ============================================================

@app.get("/students/{student_id}/assigned-exam")
def get_assigned_exam(student_id: int):

    student = find_student(student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    exam_id = get_assigned_exam_id(student_id)

    exam = exams[exam_id - 1]

    exam_questions = get_questions_for_exam(exam_id)

    return {
        "student_id": student_id,
        "student_name": student["name"],
        "assigned_exam_id": exam["id"],
        "assigned_exam_name": exam["name"],

        # Question IDs automatically displayed
        "question_ids": [
            q["id"] for q in exam_questions
        ]
    }
# GET QUESTIONS
# ============================================================
@app.get("/exams/{exam_id}/questions")
def get_exam_questions(exam_id: int):

    exam_questions = get_questions_for_exam(exam_id)

    if not exam_questions:

        raise HTTPException(
            status_code=404,
            detail="Exam not found"
        )

    return {
        "exam_id": exam_id,
        "questions": [
            {
                "question_id": q["id"],
                "question": q["question"],
                "options": q["options"]
            }
            for q in exam_questions
        ]
    }

# SUBMIT EXAM
# ============================================================
@app.post("/submit-exam")
def submit_exam(data: ExamSubmission):

    
    # 1. Find student
    # --------------------------------------------------------

    student = find_student(data.student_id)

    if student is None:

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # 2. Automatically determine assigned exam
    # --------------------------------------------------------

    exam_id = get_assigned_exam_id(data.student_id)

    # 3. Get the 5 questions
    # --------------------------------------------------------

    exam_questions = get_questions_for_exam(exam_id)


    if len(exam_questions) != 5:

        raise HTTPException(
            status_code=500,
            detail="Exam must contain exactly 5 questions"
        )

    # 4. Check that exactly 5 answers were submitted
    # --------------------------------------------------------

    if len(data.options) != 5:

        raise HTTPException(
            status_code=400,
            detail="Please select options for all 5 questions"
        )
    
    # 5. Check options are between 1 and 4
    # --------------------------------------------------------

    for option in data.options:

        if option not in [1, 2, 3, 4]:

            raise HTTPException(
                status_code=400,
                detail="Each option must be 1, 2, 3 or 4"
            )


    # --------------------------------------------------------
    # 6. Calculate score


    score = 0

    submitted_answers = []

    for index in range(5):

        question = exam_questions[index]

        selected_option = data.options[index]

        if selected_option == question["correct_option"]:
            score += 1

        submitted_answers.append({
            "question_id": question["id"],
            "selected_option": selected_option,
            "correct_option": question["correct_option"]
        })

    # 7. Calculate percentage
    # --------------------------------------------------------

    percentage = (score / 5) * 100

    result = "PASS" if percentage >= 50 else "FAIL"

    # 8. Create result
    # --------------------------------------------------------

    student_result = {

        "student_id": data.student_id,

        "student_name": student["name"],

        "exam_id": exam_id,

        "exam_name": exams[exam_id - 1]["name"],

        "question_ids": [
            q["id"] for q in exam_questions
        ],

        "answers": submitted_answers,

        "score": score,

        "total_questions": 5,

        "percentage": percentage,

        "result": result
    }

    # 9. Save / update result
    # --------------------------------------------------------

    existing = None

    for r in results:

        if r["student_id"] == data.student_id:

            existing = r
            break


    if existing:

        existing.update(student_result)

    else:

        results.append(student_result)


    # --------------------------------------------------------
    # 10. Return result immediately
    # --------------------------------------------------------

    return {
        "message": "Exam submitted successfully",

        "student_id": data.student_id,

        "student_name": student["name"],

        "exam_id": exam_id,

        "exam_name": exams[exam_id - 1]["name"],

        "question_ids": [
            q["id"] for q in exam_questions
        ],

        "score": score,

        "total_questions": 5,

        "percentage": percentage,

        "result": result
    }
# GET RESULT
# ============================================================
@app.get("/results/{student_id}")
def get_result(student_id: int):

    # First check student exists
    student = find_student(student_id)

    if student is None:

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Find result
    for r in results:

        if r["student_id"] == student_id:

            return r

    raise HTTPException(
        status_code=404,
        detail="No result found for this student. Please submit the exam first."
    )
# GET ALL RESULTS
# ============================================================
@app.get("/results")
def get_all_results():

    return results
# RESULTS SUMMARY
# ============================================================
@app.get("/results-summary")
def get_results_summary():

    passed = 0
    failed = 0

    for r in results:

        if r["result"] == "PASS":
            passed += 1

        else:
            failed += 1

    return {

        "total_attempts": len(results),

        "passed": passed,

        "failed": failed,

        "not_yet_attempted":
            len(students) - len(results)
    }