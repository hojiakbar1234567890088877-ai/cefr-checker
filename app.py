import os
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

# Sizning API kalitingiz joylashtirildi
client = Groq(api_key="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")

@app.route('/')
def home():
    # Asosiy sahifani ochish uchun
    return render_template('index.html')

@app.route('/evaluate', methods=['POST'])
def evaluate():
    try:
        data = request.json
        t1 = data.get('task1', '')
        t2 = data.get('task2', '')

        # AI ga yuboriladigan so'rov
        prompt = f"""
        You are a professional CEFR examiner. 
        Evaluate the following two tasks:
        Task 1: {t1}
        Task 2: {t2}
        
        Provide:
        1. Estimated CEFR level for each.
        2. Detailed feedback on grammar and vocabulary.
        3. How to improve to the next level.
        """

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful CEFR writing examiner."},
                {"role": "user", "content": prompt}
            ]
        )
        
        result = completion.choices[0].message.content
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
