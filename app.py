from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from google.api_core import retry
import os

app = Flask(__name__)

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
pro_model = genai.GenerativeModel('gemini-pro')

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
        short_model = genai.GenerativeModel(
            'gemini-1.5-flash',
            generation_config=genai.GenerationConfig(max_output_tokens=50))

        response = short_model.generate_content(user_message)
        bot_reply = response.text
        return jsonify({'reply': bot_reply})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'reply': 'Sorry, an error occurred while processing your request.'}), 500

if __name__ == '__main__':
    app.run(debug=True)