from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from google.api_core import retry
import chromadb
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
pro_model = genai.GenerativeModel('gemini-pro')

DB_NAME = "cory_db"
chroma_client = chromadb.Client()
db = chroma_client.get_collection(name=DB_NAME)

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
        if 'resume' in user_message or 'Cory' in user_message or 'DeWitt' in user_message:
            result = db.query(query_texts=[user_message], n_results=1)
            if result['documents']:
                [[passage]] = result["documents"]
                passage_oneline = passage.replace("\n", " ")
                query_oneline = query.replace("\n", " ")
                prompt = f"""You are a helpful bot that answers questions using text from the reference passage below.
                Ensure to answer comprehensively and clearly.

                QUESTION: {query_oneline}
                PASSAGE: {passage_oneline}
                """
                model = genai.GenerativeModel("gemini-1.5-flash-latest")
                response = model.generate_content(prompt)
        else:
            response = pro_model.generate_content(user_message)
        
        bot_reply = response.text
        return jsonify({'reply': bot_reply})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'reply': 'Sorry, an error occurred while processing your request.'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)