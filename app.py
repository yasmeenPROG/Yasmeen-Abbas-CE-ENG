from flask import Flask, request, render_template
import openai
import os

app = Flask(__name__)

# ✅ الخيار 1: تحميل من متغير بيئة (آمن)
api_key = os.getenv("YOUR_OPENAI_API_KEY")

# ✅ الخيار 2: أو اكتبيه مباشرة بشكل مؤقت (غير آمن للاستخدام العام)
# api_key = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# تحقق أن المفتاح موجود فعلاً
if not api_key:
    raise ValueError("❌ لم يتم العثور على مفتاح OpenAI API. يرجى تعيينه في متغير البيئة YOUR_OPENAI_API_KEY أو إدخاله مباشرة.")

client = openai.OpenAI(api_key=api_key)

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
        explanation = f"حدث خطأ أثناء الشرح: {str(e)}"

    return f"""
        <h2>🔍 الشرح:</h2>
        <pre>{explanation}</pre>
        <br><a href="/">⬅️ رجوع</a>
    """

if __name__ == '__main__':
    app.run(debug=True)
