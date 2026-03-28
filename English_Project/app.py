from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import json

app = Flask(__name__)
CORS(app)

# Groq API kalitingizni shu yerga qo'ying
client = Groq(api_key="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")

# PDF-dagi Conversion Table [cite: 10]
conversion_table = {
    "17": 75, "16.5": 74, "16": 72, "15.5": 69, "15": 67, "14.5": 65, "14": 63, "13.5": 62, "13": 61,
    "12.5": 59, "12": 57, "11.5": 56, "11": 54, "10.5": 53, "10": 51, "9.5": 50, "9": 49, "8.5": 47,
    "8": 45, "7.5": 43, "7": 42, "6.5": 40, "6": 38, "5.5": 35, "5": 32, "4.5": 29, "4": 26, "3.5": 23,
    "3": 21, "2.5": 18, "2": 15, "1.5": 13, "1": 11, "0.5": 10, "0": 0
}

@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.json
    t1 = data.get('task1', '')
    t2 = data.get('task2', '')

    # AI-ga PDF-dagi mezonlar bo'yicha ko'rsatma beramiz [cite: 2, 4, 7]
    prompt = f"""
    Siz professional CEFR Examinerisiz. Quyidagi mezonlar asosida baholang:
    
    TASK 1: {t1}
    TASK 2: {t2}
    
    Baholash mezonlari (Rating Scales):
    1. Task 1.1/1.2: Band 5 (B2/C1) uchun murakkab grammatika va aniq punktuatsiya[cite: 2, 4].
    2. Task 2: Band 5 (C1) uchun aniq pozitsiya va mantiqiy bog'lanish[cite: 7].
    3. Umumiy Expert Markni (max 17) hisoblang[cite: 10].
    
    Javobni FAQAT ushbu JSON formatida bering:
    {{
      "task1_band": "0",
      "task2_band": "0",
      "expert_mark": "0",
      "feedback": "Batafsil tahlil..."
    }}
    """

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
        response_format={"type": "json_object"}
    )
    
    result = json.loads(chat_completion.choices[0].message.content)
    # Ballni konvertatsiya qilish [cite: 10]
    exp_mark = str(result.get('expert_mark', "0"))
    result['standard_score'] = conversion_table.get(exp_mark, 0)
    
    return jsonify(result)

if __name__ == '__main__':
    # Bu qator serverga "hamma ulanishi mumkin" degan buyruqni beradi
    app.run(host='0.0.0.0', port=5000)