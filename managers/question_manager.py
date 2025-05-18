import json
import os
from utils.helpers import generate_id

QUESTION_FILE = "data/questions.json"

def load_questions(subject=None):
    if not os.path.exists(QUESTION_FILE):
        return []
    with open(QUESTION_FILE, "r", encoding="utf-8") as f:
        questions = json.load(f)
    if subject:
        # Lọc câu hỏi theo môn
        questions = [q for q in questions if q.get("subject") == subject]
    return questions

def save_questions(questions):
    with open(QUESTION_FILE, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

def add_question(question_text, options, correct_answer, subject=None):
    questions = load_questions()
    question_id = generate_id("Q", questions)
    questions.append({
        "id": question_id,
        "question": question_text,
        "options": options,
        "answer": correct_answer,
        "subject": subject  # thêm môn học
    })
    save_questions(questions)
    return question_id

def delete_question(question_id):
    questions = load_questions()
    questions = [q for q in questions if q["id"] != question_id]
    save_questions(questions)

def update_question(question_id, question_text, options, correct_answer, subject=None):
    questions = load_questions()
    for q in questions:
        if q["id"] == question_id:
            q["question"] = question_text
            q["options"] = options
            q["answer"] = correct_answer
            q["subject"] = subject
            break
    save_questions(questions)
