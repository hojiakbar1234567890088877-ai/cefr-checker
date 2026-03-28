from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import json
import os

app = Flask(__name__)
CORS(app)

# Groq API kalitingiz rasmda ko'rindi, uni xavfsiz saqlang
client = Groq(api_key="gsk_wKPOK2QnesOXi3IYgCe4WG...") 

@app.route('/evaluate', methods=['POST'])
def evaluate():
    try:
        data = request.json
        t1 = data.get('task1', '')
        t2 = data.get('task2', '')
        
        # AI ga so'rov yuborish
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a CEFR examiner. Evaluate the text and return ONLY a JSON with 'standard_score' (0-100) and 'feedback' keys."},
                {"role": "user", "content": f"Task 1: {t1}\nTask 2: {t2}"}
            ],
            response_format={"type": "json_object"}
        )
        
        result = json.loads(completion.choices[0].message.content)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
