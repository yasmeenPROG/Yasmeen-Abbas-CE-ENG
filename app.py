from flask import Flask, request, render_template
from openai import OpenAI, APIStatusError, APIConnectionError
import os
import logging

# تفعيل تسجيل الدخول للمساعدة بالتصحيح
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# إنشئي العميل مع الاستفادة من متغير البيئة السرّي (أفضل للمشروع الإنتاجي)
openai_api_key = os.getenv("YOUR_OPENAI_API_KEY")
logging.info(f"YOUR_OPENAI_API_KEY موجود؟ {'نعم' if openai_api_key else 'لا'}")

if not openai_api_key:
    logging.error("متغير البيئة OPENAI_API_KEY غير موجود أو فارغ!")

client = OpenAI(api_key=openai_api_key)

@app.route('/')
def index():
    return render_template('ONE.html')

@app.route('/شرح', methods=['POST'])
def شرح():
    user_code = request.form.get('code', '').strip()
    
    if not user_code:
        return "<h2>رجاءً أدخلي الكود أولاً!</h2><br><a href='/'>رجوع</a>"
    
    prompt = (
        f"أنت مساعد برمجي خبير. يرجى شرح الكود التالي سطرًا بسطر،"
        f" بلغة عربية مبسطة، مع تبسيط المفاهيم ووظيفة كل جزء:\n\n{user_code}\n\nالشرح:"
    )
    
    logging.info("إرسال الطلب إلى OpenAI...")
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        explanation = response.choices[0].message.content
        logging.info("الشرح تم استلامه بنجاح.")
    except APIStatusError as e:
        logging.error(f"APIStatusError: code={e.status_code}, response={e.response}")
        explanation = f"خطأ من الخادم: {e.status_code}"
    except APIConnectionError as e:
        logging.error(f"APIConnectionError: {e}")
        explanation = "خطأ في الاتصال بالسيرفر، يرجى المحاولة لاحقًا."
    except Exception as e:
        logging.error(f"خطأ غير متوقع: {e}")
        explanation = f"حدث خطأ غير معروف: {e}"

    return f"""
        <h2>🔍 الشرح:</h2>
        <pre>{explanation}</pre>
        <br><a href="/">⬅️ رجوع</a>
    """

if __name__ == '__main__':
    app.run(debug=True)

