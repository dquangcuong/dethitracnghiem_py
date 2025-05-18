import random
from managers.question_manager import load_questions
from utils.helpers import generate_id
import json
import os

EXAM_FILE = "data/exams.json"
AVAILABLE_SUBJECTS = ["Python", "Java", "C#", "C/C++", "Toán", "Lý", "Hóa", "Sử", "Địa", "GDCD", "Tiếng Anh"]

def load_exams(subject=None):
    if not os.path.exists(EXAM_FILE):
        return []
    with open(EXAM_FILE, "r", encoding="utf-8") as f:
        exams = json.load(f)
    if subject:
        exams = [e for e in exams if e.get("subject") == subject]
    return exams

def save_exams(exams):
    with open(EXAM_FILE, "w", encoding="utf-8") as f:
        json.dump(exams, f, ensure_ascii=False, indent=2)

def create_exam(name, question_ids=None, subject=None, num_questions=None):
    """
    Nếu truyền question_ids thì tạo đề với các câu hỏi đó,
    nếu không thì tạo đề theo môn (subject) và số câu hỏi (num_questions) lấy ngẫu nhiên từ question.json
    """
    if subject and num_questions:
        if subject not in AVAILABLE_SUBJECTS:
            raise ValueError(f"Môn học không hợp lệ: {subject}")

        questions = load_questions()
        filtered_questions = [q for q in questions if q.get("subject") == subject]

        if len(filtered_questions) < num_questions:
            raise ValueError(f"Không có đủ câu hỏi cho môn {subject}. Số câu hỏi hiện có: {len(filtered_questions)}")

        selected_questions = random.sample(filtered_questions, num_questions)
        question_ids = [q["id"] for q in selected_questions]

    if not question_ids:
        raise ValueError("Phải cung cấp question_ids hoặc subject và num_questions để tạo đề thi")

    exams = load_exams()
    exam_id = generate_id("E", exams)
    exams.append({
        "id": exam_id,
        "name": name,
        "questions": question_ids,
        "subject": subject
    })
    save_exams(exams)
    return exam_id

def delete_exam(exam_id):
    exams = load_exams()
    exams = [e for e in exams if e["id"] != exam_id]
    save_exams(exams)
