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
#     "http://localhost:5173",
#     "http://127.0.0.1:5173",
#     "http://192.168.1.100:3000",

# ]

# load_dotenv()
# # loads the env, to read .env file and get access to .env not sensitive keys of firebase_key.json
# cred_path = os.getenv('FIREBASE_KEY_PATH', 'firebase_key.json')
# #tells us we are credible and have certificate to connect
# cred = credentials.Certificate(cred_path)
# #starts the connection
# firebase_admin.initialize_app(cred)
# # makes a varuable db to read nd write to firesore db
# db = firestore.client()

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins= origins, # ontop
#     allow_credentials =True,
#     allow_methods = ["*"], # methods = CRUD
#     allow_headers =["*"]  
# )

# class Answer(BaseModel):
#     question_id :str
#     answer:str

# class SubmitAnswers(BaseModel):
#     answers: List[Answer] # makes an array of Answers which will have a q_id and a correct answer 

# @app.get('/questions')

# def get_questions():
#     try:
#         docs = db.collection('questions').stream()
#         questions = [doc.to_dict() for doc in docs]
#         return {
#             "questions": questions
#         }
#     except Exception as e:
#         return {"error": str(e)}
    
#  # a single answer frm user
# #{question_id : '1', answer: "cat"}
#  # collection of all
# #  answers[{question_id : '1', answer: "cat"},
# #             {question_id : '2', answer: "bat"}]
    
# @app.post('/submit')

# #submission.answers[0].question_id=1
# # submission.answers[0].answers="cat"

# def submit_answers(submission: SubmitAnswers):
#     try:
#         docs = db.collection('questions').stream()
#         questions = [doc.to_dict() for doc in docs]
#        # Build a dictionary of correct answers
#         correct_answers={}

#         for q in questions:
#             if "id" in q and "answer" in q:
#                 qid = str(q["id"]).strip()
#                 ans = str(q["answer"]).strip().lower()
#                 correct_answers[qid] = ans 
        
#         # now work with user response
#         score = 0
# #submission.answers[0].question_id=1
# # submission.answers[0].answers="cat"

#         for ans in submission.answers:
#             qid = str(ans.question_id).strip()
#             user_ans = ans.answer.strip().lower()

#         if qid in correct_answers:
#             correct = correct_answers[qid]
# # here the photo/photograph is being created into  array and spaces removed to compare
#             correct_options = [c.strip() for c in correct.split("/")]

#             # compare answers

#             if user_ans in correct_options:
#                 score +=1
# # Return Result

#         return {
#             "Score" :score,
#             "total_score" : len(correct_answers)
#         }    

#     except Exception as e:

#         return{"error", e}    

