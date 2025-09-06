from flask import Flask, request, render_template
from openai import OpenAI
import os

app = Flask(__name__)

# ✅ استخدمي مكتبة OpenAI الحديثة
client = OpenAI(api_key="YOUR_OPENAI_API_KEY")  # ← بدلي المفتاح هنا

@app.route('/')
def index():
    return render_template('ONE.html')

@app.route('/شرح', methods=['POST'])
def شرح():
    user_code = request.form['code']

    prompt = f"""أنت مساعد خبير في البرمجة. يرجى شرح الكود التالي سطرًا بسطر، وبلغة عربية مبسطة، مع تبسيط المفاهيم البرمجية وذكر وظيفة كل جزء من الكود، سواء كان بلغة Python أو أي لغة أخرى. الكود:\n\n{user_code}\n\nالشرح:"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        explanation = response.choices[0].message.content
    except Exception as e:
        explanation = f"حدث خطأ أثناء الشرح:\n\n{str(e)}"

    return f"""
        <h2>🔍 الشرح:</h2>
        <pre>{explanation}</pre>
        <br><a href="/">⬅️ رجوع</a>
    """

if __name__ == '__main__':
    app.run(debug=True)

