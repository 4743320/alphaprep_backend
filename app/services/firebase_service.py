# import firebase_admin
# from firebase_admin import credentials, firestore

# import os
# from dotenv import load_dotenv

# load_dotenv()

# cred_path = os.getenv('FIREBASE_KEY_PATH','firebase_key.json')

# if not firebase_admin._apps:

#     cred = credentials.Certificate(cred_path)
#     firebase_admin.initialize_app(cred)

# db = firestore.client()

# def get_questions():
#     """
#     Fetch all questions from the 'questions' collection in Firestore.
#     Returns a list of dictionaries, where each dictionary is a question document.
#     """
#     questions_ref = db.collection('questions')
#     docs = questions_ref.stream()

#     questions = [doc.to_dict() for doc in docs]

#     return questions
