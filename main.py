# from fastapi import FastAPI
# import firebase_admin
# from firebase_admin import credentials, firestore
# from pydantic import BaseModel
# from dotenv import load_dotenv
# import os
# from typing import List
# from fastapi.middleware.cors import CORSMiddleware

# origins = [ 
#     "http://localhost:3000",
#     "http://127.0.0.1:3000",
#     "http://localhost:5000",
#     "http://192.168.1.100:3000",   # <- COMMA added
#     "http://localhost:5173" ,        # <- this is your Vite dev server
#     "http://127.0.0.1:5173",  # optional alternative
# ]
# load_dotenv()

# cred_path = os.getenv('FIREBASE_KEY_PATH' ,'firebase_key.json')

# cred = credentials.Certificate(cred_path)
# firebase_admin.initialize_app(cred)


# db = firestore.client()

# app = FastAPI()

# app.add_middleware( 
#     CORSMiddleware,
#         allow_origins= origins,  # allow all origins temporarily
#             # allow_origins=origins,       # allow only these origins
#     allow_credentials = True,
#     allow_methods = ["*"],
#     allow_headers =["*"]

# )


# class Answer(BaseModel):
#     question_id: str
#     answer:str

# class SubmitAnswers(BaseModel):
#     user_id:str
#     answers: List[Answer]




# @app.get('/questions')

# def get_questions():
#     """Fetch all questions from firestore and display as json"""
#     questions_ref = db.collection('questions')

#     docs=questions_ref.stream()

#     questions = [doc.to_dict() for doc in docs]

#     return {'questions': questions}


# @app.post("/submit")

# # Compares user answers with Firestore answers
# #     and returns the score.
    
# # def submit_answers(submission: SubmitAnswers):
# #     docs =db.collection('questions').stream()
# #     questions = [doc.to_dict() for doc in docs]

# #     # create a dictionary of correct answers

# #     correct_answers= {
# #         str(q['id']):q['answer'] for q in questions
# #     }

# #     score = 0
# #     for ans in submission.answers:
# #         if ans.question_id in correct_answers:
# #             if ans.answer == correct_answers[ans.question_id]:
# #                 score +=1
# #     return {
# #         'user_id': submission.user_id,
# #         'score': score}
# @app.post("/submit")
# def submit_answers(submission: SubmitAnswers):

#     try:
#         # FETCH all questions from Firestore
#         docs = db.collection("questions").stream()
#         questions = [doc.to_dict() for doc in docs]

#         # Build dictionary of correct answers
#         correct_answers = {}  # {"1": "cat", "2": "shower", ...}

#         for q in questions:
#             if "id" in q and "answer" in q:
#                 qid = str(q["id"]).strip()
#                 correct_answers[qid] = str(q["answer"]).strip().lower()
#             else:
#                 print("Skipped invalid question:", q)

#         # SCORE CALCULATION
#         score = 0

#         for ans in submission.answers:
#             qid = str(ans.question_id).strip()
#             user_ans = ans.answer.strip().lower()

#             if qid in correct_answers:
#                 if user_ans == correct_answers[qid]:
#                     score += 1

#         return {
#             "user_id": submission.user_id,
#             "score": score,
#             "total_questions": len(correct_answers)
#         }

#     except Exception as e:
#         return {"error": str(e)}

from fastapi import FastAPI
import firebase_admin
from firebase_admin import credentials, firestore
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from typing import List
from fastapi.middleware.cors import CORSMiddleware

# ---------------------------------------------------
# CORS SETTINGS
# ---------------------------------------------------
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://192.168.1.100:3000",
]

# ---------------------------------------------------
# FIREBASE INIT
# ---------------------------------------------------
load_dotenv()

cred_path = os.getenv('FIREBASE_KEY_PATH', 'firebase_key.json')
cred = credentials.Certificate(cred_path)

firebase_admin.initialize_app(cred)
db = firestore.client()

# ---------------------------------------------------
# FASTAPI APP
# ---------------------------------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ---------------------------------------------------
# PYDANTIC MODELS (REQUEST BODY VALIDATION)
# ---------------------------------------------------
class Answer(BaseModel):
    question_id: str
    answer: str

class SubmitAnswers(BaseModel):
    # user_id: str        # <-- user_id included here
    answers: List[Answer]


# ---------------------------------------------------
# GET QUESTIONS: Fetch all questions from Firestore
# ---------------------------------------------------
@app.get("/questions")
def get_questions():
    try:
        docs = db.collection('questions').stream()
        questions = [doc.to_dict() for doc in docs]
        return {"questions": questions}

    except Exception as e:
        return {"error": str(e)}


# ---------------------------------------------------
# POST SUBMIT: Score calculation logic
# ---------------------------------------------------
# @app.post("/submit")
# def submit_answers(submission: SubmitAnswers):

#     try:
#         # FETCH all questions from Firestore
#         docs = db.collection("questions").stream()
#         questions = [doc.to_dict() for doc in docs]

#         # Build dictionary of correct answers
#         correct_answers = {}  # {"1": "cat", "2": "shower", ...}

#         for q in questions:
#             if "id" in q and "answer" in q:
#                 qid = str(q["id"]).strip()
#                 correct_answers[qid] = str(q["answer"]).strip().lower()
#             else:
#                 print("Skipped invalid question:", q)

#         # SCORE CALCULATION
#         score = 0

#         for ans in submission.answers:
#             qid = str(ans.question_id).strip()
#             user_ans = ans.answer.strip().lower()

#             if qid in correct_answers:
#                 if user_ans == correct_answers[qid]:
#                     score += 1

#         return {
#             "user_id": submission.user_id,
#             "score": score,
#             "total_questions": len(correct_answers)
#         }

#     except Exception as e:
#         return {"error": str(e)}
@app.post("/submit")
def submit_answers(submission: SubmitAnswers):

    try:
        # Fetch all correct answers
        docs = db.collection("questions").stream()
        questions = [doc.to_dict() for doc in docs]

        # Build correct answers dictionary
        correct_answers = {}

        for q in questions:
            if "id" in q and "answer" in q:
                qid = str(q["id"]).strip()
                ans = str(q["answer"]).strip().lower()
                correct_answers[qid] = ans
            else:
                print("Invalid question skipped:", q)

        score = 0

        for ans in submission.answers:
            qid = str(ans.question_id).strip()
            user_ans = ans.answer.strip().lower()

            if qid in correct_answers:

                correct = correct_answers[qid]

                # ------------------------------
                # NEW: Support multiple correct answers separated by "/"
                # Example: Firestore answer = "photos/ photographs pictures"
                # ------------------------------
                correct_options = [c.strip() for c in correct.split("/")]  # <-- NEW
                if user_ans in correct_options:                            # <-- NEW
                    score += 1                                              # <-- NEW

        return {
            "score": score,                   # <-- REMOVED user_id from return
            "total_questions": len(correct_answers)
        }

    except Exception as e:
        return {"error": str(e)}

# questions (collection)
#    └── docID
#          - id
#          - part
#          - question
#          - options
#          - answer

@app.get("/")
def get_ielts_questions():
    
    ref = db.collection("ielts-questions_answers")
    docs = ref.stream()

    ielts_data=[]

    for doc in docs:
        item = doc.to_dict()
        item["id"] = doc.id

        ielts_data.append(item)

    return {"tests": ielts_data}


# @app.post("/submit/{test_id}")
# def submit_answers(test_id:str, submission: SubmitAnswers):
#     try:
#         doc_ref = db.collection('ielts-questions_answers').document(test_id)
#         doc = doc_ref.get()

#         if not doc.exists:
#             return{"error": "test Not Found"}
        
#         test_data = doc.to_dict()

#         correct_answers={}
#         # ---------------------------------------
#     # section_name  → "Listening" / "Reading"
#     # section_data  → dictionary of parts
#     # Example:
#     # {
#     #   "P1": [ {id:1, answer:"fish"}, ... ],
#     #   "P2": [ ... ]
#     # }
#     # ---------------------------------------
# # .get("sections",{})= if no sections present return {}, .items() convetrs data into key value pair
#         score =0

#         for section_name, section_data in test_data.get("sections",{}).items():
#              # ---------------------------------------
#         # part_name     → "P1", "P2", "Passage1"
#         # part_answers  → list of Q/A objects
#         # Example:
#         # [
#         #   { "id": "1", "answer": "fish" },
#         #   { "id": "2", "answer": "roof" }
#         # ]
#         # ---------------------------------------

#             for part_name,part_answers in section_data.items():
#                 for q in part_answers:
#                     qid= str(q["id"]).strip()
#                     correct_answer = str(q["answer"]).strip().lower()
#             # ---------------------------------------
#             # Build final correct_answers dictionary:
#             #
#             # correct_answers = {
#             #    "1": "fish",
#             #    "2": "roof",
#             #    ...
#             # }
#             # ---------------------------------------
                    
#                     correct_answers[qid]= correct_answer
                    
            
#             for ans in submission.answers:
#                 qid = str(ans.question_id).strip()
#                 user_answer = ans.answer.strip().lower()

#                 if qid in correct_answers:
#                     correct = correct_answers[qid]

#                     correct_options =[c.strip() for c in correct.split('/')]

#                     if user_answer in correct_options:
#                         score +=1

#         return {
#             "test_id":test_id,
#             "score": score,
#             "total_questions": len(correct_answers),
#         }
    

#     except Exception as e:
#         return{"error":e}

@app.post('/submit/{test_id}/{section}')
def submit_answers(test_id: str, section: str, submission: SubmitAnswers):
    try:
        doc_ref = db.collection('ielts-questions_answers').document(test_id)
        doc = doc_ref.get()

        if not doc.exists:
            return {"error": "test not found"}

        test_data = doc.to_dict()

        sections = test_data.get("sections", {})

        if section not in sections:
            return {"error": f"Section '{section}' not found in this test"}

        section_data = sections[section]

        correct_answers = {}

        # build all correct answers for this specific section only
        for part_name, part_questions in section_data.items():
            for q in part_questions:
                qid = str(q["id"]).strip()
                correct_ans = str(q["answer"]).strip().lower()
                correct_answers[qid] = correct_ans

        score = 0

        for ans in submission.answers:
            qid = str(ans.question_id).strip()
            user_ans = ans.answer.strip().lower()

            if qid in correct_answers:
                correct = correct_answers[qid]
                correct_options = [c.strip() for c in correct.split('/')]

                if user_ans in correct_options:
                    score += 1

        return {
            "test_id": test_id,
            "section": section,
            "score": score,
            "total_questions": len(correct_answers),
        }

    except Exception as e:
        return {"error": str(e)}
