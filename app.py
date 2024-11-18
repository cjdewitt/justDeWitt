from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from google.api_core import retry
import chromadb
from init_db import initialize_db
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
pro_model = genai.GenerativeModel('gemini-pro')

db = initialize_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')

    try:
        if db is None:
            return jsonify({'reply': 'Database not initialized. Please contact support.'}), 500

        if 'resume' in user_message or 'Cory' in user_message or 'DeWitt' in user_message:
            result = db.query(query_texts=[user_message], n_results=1)
            if result['documents']:
                [[passage]] = result["documents"]
                passage_oneline = passage.replace("\n", " ")
                query_oneline = user_message.replace("\n", " ")
                prompt = f"""You are a helpful bot that answers questions using text from the reference passage below.
                Ensure to answer comprehensively and clearly.

                QUESTION: {query_oneline}
                PASSAGE: {passage_oneline}
                """
                model = genai.GenerativeModel("gemini-1.5-flash-latest")
                response = model.generate_content(prompt)

        else:
                response = genai.GenerativeModel("gemini-1.5-flash-latest").generate_content(user_message)

        return jsonify({'reply': response.text})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'reply': 'An error occurred while processing your request.'}), 500

if __name__ == "__main__":
    app.run(debug=True)