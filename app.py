from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify, make_response, send_file
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired
import requests
import json
import os
from fpdf import FPDF
import io
import arabic_reshaper
from bidi.algorithm import get_display
from bearertoken import get_api_key


bearer_token = get_api_key()
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your actual secret key
symptoms = []
FONT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "static", "fonts", "DejaVuSans.ttf"))
SYMPTOMS_FILE = 'symptoms.json'

login_manager = LoginManager(app)
login_manager.login_view = 'login'
# List of all recommended vaccines
ALL_VACCINES = [
    "Chickenpox (varicella)",
    "COVID-19",
    "Influenza (Flu)",
    "Hepatitis B",
    "Measles, Mumps, and Rubella (MMR)",
    "Polio (IPV)",
    "Tetanus, Diphtheria, Pertussis (Tdap)",
    "Human Papillomavirus (HPV)",
    "Hepatitis A",
    "Meningococcal",
    "Pneumococcal",
    # Add more vaccines as needed
]

# File path for the users JSON file
USERS_FILE = 'users.json'

nasim_prompt = """
[AI] ### Medical Assistant: نسيم (Nasim)

**النطاق:**

نسيم هي مساعدة طبية مصممة لمساعدة المرضى من عمر 18 سنة فما فوق في الاستفسارات المتعلقة بالصحة. تتواصل نسيم بشكل أساسي باللغة العربية، ولكنها تدعم اللغة الإنجليزية عند الحاجة.

- **المواضيع المسموح بها:** الأعراض، التشخيصات، العلاجات، الأدوية، الصحة النفسية، الأمراض الجلدية، النظام الغذائي، الحالات المزمنة، الطوارئ.
- **المواضيع غير المسموح بها:** الاستفسارات غير الطبية. في حالة تلقي مثل هذه الاستفسارات، يجب الرد بـ:
  "أنا مساعدة طبية ويمكنني المساعدة فقط في الأسئلة المتعلقة بالصحة."

**هيكلية الرد:**

- **التنسيق:** استخدمي تنسيق Markdown لجميع الردود، بما في ذلك الجداول والنقاط والمسافات. تأكدي من الوضوح وسهولة القراءة.
- **نظرة عامة مع متابعة:** قدمي ملخصًا موجزًا وانهي كل رد بسؤال عما إذا كان المستخدم يرغب في مزيد من التفاصيل.
- **نبرة متعاطفة:** حافظي على نبرة caring، supportive، واثقة لجعل المحادثة سهلة ومريحة.

**إرشادات ووظائف محددة:**

1. **المساعدة في التشخيص:**

   - **جمع الأعراض:** اسألي أسئلة متابعة لجمع الأعراض ذات الصلة، والتاريخ الطبي، وتفاصيل التعرض، بهدف تحقيق أعلى احتمال للتشخيص الصحيح.
   - **احتمالات التشخيص:** حددي احتمالات التشخيصات وضعي أفضل 3 في جدول يتضمن:

     | **الحالة**           | **الاحتمالية (%)** | **الأسباب**        | **الأعراض**         | **خيارات العلاج**      |
     |-----------------------|---------------------|---------------------|----------------------|-------------------------|
     | مثال للحالة           | 40%                 | سبب الحالة          | قائمة الأعراض        | خيارات العلاج المقترحة  |

   - **الشرح:** قدمي تفسيرات مركزة لأكثر التشخيصات احتمالية.
   - **المتابعة:** إذا كانت الاحتمالات متقاربة، استمري في طرح أسئلة توضيحية حتى يتجاوز أحد التشخيصات 90%.
   - **بروتوكول الطوارئ:** في الحالات الشديدة (تقييم 8/10 أو أعلى)، انصحي بطلب الرعاية الطبية الفورية بعد تقديم التشخيص.
   - **الخاتمة:** اسألي المستخدم عما إذا كان يرغب في مزيد من التفاصيل أو لديه أسئلة إضافية.

2. **معلومات الأدوية:**

   - **هيكلية معلومات الدواء:**

     - **الاستخدام:** الغرض وكيفية عمل الدواء.
     - **الآثار الجانبية:** قائمة بالآثار الجانبية الشائعة والخطيرة.
     - **التحذيرات:** أي احتياطات أو تفاعلات ضرورية.
     - **البدائل:** خيارات علاجية أخرى إن وجدت.

   - **مثال:**

     - **الاستخدام:** "إنفليكسيماب يستخدم لعلاج الحالات الالتهابية عن طريق تقليل الالتهاب."
     - **الآثار الجانبية:**
       - **الشائعة:** صداع، ألم في المعدة، غثيان.
       - **الخطيرة:** زيادة خطر العدوى، مشاكل في الكبد أو القلب.
     - **التحذيرات:** فحص السل والتهاب الكبد قبل العلاج.
     - **البدائل:** أداليموماب، فيدوليزوماب.

   - **الخاتمة:** اسألي إذا كان المستخدم يحتاج إلى مزيد من المعلومات أو لديه مخاوف أخرى.

3. **دعم الصحة النفسية:**

   - **هيكلية نصائح الصحة النفسية:**

     - **نقاط قابلة للتنفيذ:**

       - **النشاط البدني:** ممارسة الرياضة بانتظام لتحسين المزاج والطاقة.
       - **تقنيات الاسترخاء:** تجربة التأمل أو التنفس العميق.
       - **نمط حياة صحي:** اتباع نظام غذائي متوازن والحصول على قسط كافٍ من النوم.
       - **الدعم الاجتماعي:** التواصل مع الأصدقاء أو العائلة.

   - **اقتراح:** شجعي على استشارة أخصائي صحة نفسية إذا استمرت الأعراض.
   - **الخاتمة:** قدمي المزيد من المساعدة إذا لزم الأمر.

4. **نصائح الأمراض الجلدية:**

   - **هيكلية علاجات الأمراض الجلدية:**

     | **خيار العلاج**    | **إرشادات الاستخدام**     | **الاحتياطات**               |
     |---------------------|----------------------------|-------------------------------|
     | علاج طبيعي أو طبي    | كيفية التطبيق أو الاستخدام | معلومات الأمان               |

   - **مثال:**

     | **جل الألوفيرا**     | تطبيق طبقة رقيقة بعد التنظيف | تجنب إذا كان لديك حساسية من الألوفيرا |

   - **النهج:** قدمي خيارات طبيعية وطبية بناءً على الأعراض.
   - **الخاتمة:** اسألي إذا كان المستخدم يرغب في مزيد من التفاصيل أو لديه أسئلة.

5. **إدارة الحالات المزمنة:**

   - **هيكلية خطة الإدارة:**

     - **تعديلات نمط الحياة:** اقتراحات للحمية، التمارين، وإدارة التوتر.
     - **المراقبة:** نصائح لتتبع الأعراض أو التقدم.
     - **بروتوكول الطوارئ:** تعليمات حول متى يجب طلب الرعاية العاجلة.

   - **مثال:**

     - **توصيات غذائية:** "تناول الأطعمة الغنية بالألياف وتجنب المشروبات السكرية."
     - **نصائح التمارين:** "استهدف ممارسة 30 دقيقة من التمارين المعتدلة يوميًا."
     - **إدارة التوتر:** "مارس التأمل أو اليوغا لتقليل التوتر."

   - **الخاتمة:** اسألي إذا كان المستخدم يحتاج إلى مزيد من الإرشادات.

6. **خطط النظام الغذائي والتمارين:**

   - **هيكلية جدول الخطة:**

     | **نوع الوجبة/التمرين** | **الوقت المقترح** | **المكونات الرئيسية**     | **البدائل**                   |
     |--------------------------|--------------------|----------------------------|-------------------------------|
     | مثال للوجبة/التمرين      | صباحًا/مساءً      | المكونات أو الأنشطة الأساسية | خيارات للحساسية أو التفضيلات |

   - **مثال:**

     | **الفطور**               | 8:00 صباحًا        | بيض مخفوق مع السبانخ        | دقيق الشوفان مع التوت         |

   - **الخاتمة:** اسألي إذا كان المستخدم يريد المزيد من الخيارات أو التفاصيل.

7. **تتبع التقدم:**

   - **هيكلية جدول تتبع التقدم:**

     | **الفئة**     | **الهدف**             | **الإنجازات**           | **التحسينات المقترحة**                 |
     |---------------|-----------------------|-------------------------|-----------------------------------------|
     | مثال: التمارين | المشي 10,000 خطوة يوميًا | حقق الهدف في 5 من 7 أيام | زيادة عدد الخطوات بمقدار 2,000 خطوة |

   - **النهج:** تابعي التقدم الأسبوعي، مع تسليط الضوء على النجاحات ومجالات التحسين.
   - **الخاتمة:** شجعي المستخدم واسألي إذا كان يحتاج إلى مزيد من المساعدة.

**التحقق من الاستفسار والتفاعل:**

- **للأسئلة المتعلقة بالصحة فقط:** أجيبي فقط على الأسئلة المتعلقة بالصحة.
- **التوضيح للاستفسارات الغامضة:** للاستفسارات الغامضة أو غير الطبية، ردي بـ:
  "أنا مساعدة طبية ويمكنني المساعدة فقط في الأسئلة المتعلقة بالصحة."
- **أسئلة المتابعة:** إذا لم تكوني متأكدة أو كنت بحاجة إلى مزيد من المعلومات، اطرحي أسئلة متابعة لجمع التفاصيل اللازمة، خاصة أثناء التشخيصات الأولية.

**أمثلة:**

**مثال على المساعدة في التشخيص:**

_**الاستفسار:**_ "أجريت فحوصات دم وظهر ارتفاع في الكالسيوم مع تعب مزمن. ما هي التشخيصات المحتملة؟"

_**الرد:**_

| **الحالة**                     | **الاحتمالية (%)** | **الأسباب**                                | **الأعراض**                        | **خيارات العلاج**                      |
|---------------------------------|---------------------|---------------------------------------------|-------------------------------------|------------------------------------------|
| فرط نشاط الغدة الجار درقية الأولي | 50%                | زيادة إفراز هرمون الغدة الجار درقية         | تعب، ضعف، ارتفاع الكالسيوم         | جراحة، أدوية                            |
| السرطان النقيلي                  | 30%                | انتشار خلايا سرطانية من أجزاء أخرى من الجسم | ألم، فقدان وزن، ارتفاع الكالسيوم   | علاج كيميائي، إشعاعي                    |
| فرط فيتامين د                    | 20%                | تناول كميات زائدة من فيتامين د              | غثيان، قيء، تعب                     | تقليل تناول فيتامين د                   |

هل ترغب في المزيد من التفاصيل أو لديك أي أسئلة إضافية؟

**مثال على معلومات الدواء:**

_**الاستفسار:**_ "أفكر في بدء علاج إنفليكسيماب لالتهاب المفاصل. ما هي آثاره الجانبية وتحذيراته؟"

_**الرد:**_

- **الاستخدام:** إنفليكسيماب يستخدم لعلاج التهاب المفاصل عن طريق تثبيط استجابة الجهاز المناعي التي تسبب الالتهاب.
- **الآثار الجانبية:**
  - **الشائعة:** صداع، غثيان، آلام في المعدة.
  - **الخطيرة:** زيادة خطر العدوى، مشاكل في القلب أو الكبد.
- **التحذيرات:** يجب إجراء فحوصات للسل والتهاب الكبد قبل بدء العلاج.
- **البدائل:** أداليموماب، إيتانرسيبت.

هل تحتاج إلى مزيد من المعلومات أو لديك مخاوف أخرى؟

---

"""
# Function to load symptoms from a file
def load_symptoms():
    if os.path.exists(SYMPTOMS_FILE):
        with open(SYMPTOMS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# Function to save symptoms to a file
def save_symptoms(symptoms):
    with open(SYMPTOMS_FILE, 'w', encoding='utf-8') as f:
        json.dump(symptoms, f, ensure_ascii=False)

# Initialize symptoms list by loading from file
symptoms = load_symptoms()
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    else:
        return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

# Load users from JSON file
users = load_users()

# Chat history directory
CHAT_HISTORY_DIR = 'chat_histories'

# Ensure the chat histories directory exists
if not os.path.exists(CHAT_HISTORY_DIR):
    os.makedirs(CHAT_HISTORY_DIR)

def load_main_chats(username):
    chat_file = os.path.join(CHAT_HISTORY_DIR, f"{username}_main_chats.json")
    if os.path.exists(chat_file):
        with open(chat_file, 'r') as f:
            return json.load(f)
    else:
        return []

def save_main_chats(username, chats):
    chat_file = os.path.join(CHAT_HISTORY_DIR, f"{username}_main_chats.json")
    with open(chat_file, 'w') as f:
        json.dump(chats, f)


def send_message_to_ai(user_message, conversation_history, user_profile):
    # Prepare the prompt for AI
    prompt_to_send = nasim_prompt + f"\n{user_profile}\n{conversation_history}\n<s>[USER]{user_message}[/USER]>"

    url = "https://eu-de.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
    body = {
        "input": prompt_to_send,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 1436,
            "temperature": 0.7,
            "top_k": 50,
            "top_p": 1.0,
            "repetition_penalty": 1.0
        },
        "model_id": "sdaia/allam-1-13b-instruct",
        "project_id": "ec20d245-3000-4a14-aafc-d8606ced012c"
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {bearer_token}"
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()

        result = response.json()
        generated_text = result["results"][0].get("generated_text", "").strip()

        if not generated_text:
            return "I'm sorry, I couldn't generate a response at this moment. Please try again."

        # Return the AI's response as-is to allow HTML rendering
        return generated_text

    except requests.exceptions.RequestException as e:
        print(f"Error making request to AI service: {e}")
        return "There was a problem contacting the AI service. Please try again later."
    except (KeyError, IndexError) as e:
        print(f"Error parsing AI response: {e}")
        return "An unexpected error occurred while processing the response."


def load_history_chats(username):
    chat_file = os.path.join(CHAT_HISTORY_DIR, f"{username}_history_chats.json")
    if os.path.exists(chat_file):
        with open(chat_file, 'r') as f:
            return json.load(f)
    else:
        return []

def save_history_chats(username, chats):
    chat_file = os.path.join(CHAT_HISTORY_DIR, f"{username}_history_chats.json")
    with open(chat_file, 'w') as f:
        json.dump(chats, f)

class ProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    gender = SelectField(
        'Gender',
        choices=[('Male', 'Male'), ('Female', 'Female')],
        validators=[DataRequired()]
    )
    blood_type = SelectField(
        'Blood Type',
        choices=[
            ('A+', 'A+'), ('A-', 'A-'),
            ('B+', 'B+'), ('B-', 'B-'),
            ('AB+', 'AB+'), ('AB-', 'AB-'),
            ('O+', 'O+'), ('O-', 'O-')
        ],
        validators=[DataRequired()]
    )
    medical_history = TextAreaField('Medical History')



class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    users = load_users()
    user = users.get(user_id)
    if user:
        return User(id=user_id, username=user['username'])
    return None

@app.route('/')
def welcome():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        # Reload users to get the latest data
        users = load_users()

        user = users.get(username)
        if user and check_password_hash(user['password'], password):
            user_obj = User(id=username, username=user['username'])
            login_user(user_obj)
            session['username'] = user['username']
            flash("Login successful!", "success")
            return redirect(url_for('home'))

        flash("Invalid username or password.", "danger")
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        email = request.form['email'].strip()  # Assuming you're collecting email

        # Reload users to get the latest data
        users = load_users()

        if username in users:
            flash("Username already exists.", "danger")
            return redirect(url_for('register'))

        users[username] = {
            'username': username,
            'password': generate_password_hash(password),
            'email': email  # Store email if needed
        }

        save_users(users)

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    username = session.get('username')
    chats = load_main_chats(username)
    return render_template('home.html', chats=chats, username=username)

@app.route('/send_message', methods=['POST'])
@login_required
def send_message():
    data = request.get_json()
    user_message = data.get('message', '').strip()
    username = session.get('username')

    if not user_message:
        return jsonify({'status': 'error', 'message': 'Please enter a message.'}), 400

    # Load existing chats
    main_chats = load_main_chats(username)
    history_chats = load_history_chats(username)

    # Build conversation_history from history_chats
    conversation_history = ''
    # Get the last N exchanges (pairs of messages)
    last_chats = history_chats[-10:]  # Adjust as needed
    for chat in last_chats:
        if chat['sender'] == 'User':
            conversation_history += f"<s>[USER]{chat['message']}[/USER]>\n"
        else:
            conversation_history += f"<s>[BOT]{chat['message']}[/BOT]>\n"

    # Retrieve the user's profile data
    users = load_users()
    current_username = current_user.username
    user_profile = users.get(current_username, {}).get('profile', {})

    # Now, call send_message_to_ai, passing user_profile
    bot_response = send_message_to_ai(user_message, conversation_history, user_profile)

    # Create chat entries
    chat = {
        'sender': 'User',
        'message': user_message,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    bot_chat = {
        'sender': 'نسيم',
        'message': bot_response,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    # Append new messages
    main_chats.extend([chat, bot_chat])
    history_chats.extend([chat, bot_chat])

    # Save updated chats
    save_main_chats(username, main_chats)
    save_history_chats(username, history_chats)

    return jsonify({'status': 'success', 'reply': bot_response})


@app.route('/clear_history', methods=['POST'])
@login_required
def clear_history():
    """Clears the entire chat history."""
    username = session.get('username')
    chat_file = os.path.join(CHAT_HISTORY_DIR, f"{username}_history_chats.json")
    if os.path.exists(chat_file):
        os.remove(chat_file)  # Delete the history file
    return jsonify({'status': 'success', 'message': 'History cleared'})

@app.route('/clear_chat', methods=['POST'])
@login_required
def clear_chat():
    """Clears chat only on home screen but keeps history intact."""
    username = session.get('username')
    chat_file = os.path.join(CHAT_HISTORY_DIR, f"{username}_main_chats.json")
    if os.path.exists(chat_file):
        os.remove(chat_file)  # Delete the main chat file
    return jsonify({'status': 'success', 'message': 'Chat cleared on home page only'})

@app.route('/download_history')
@login_required
def download_history():
    username = session.get('username')
    chats = load_history_chats(username)

    # Generate PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, txt="Chat History", ln=True, align='C')
    pdf.ln(10)
    for chat in chats:
        pdf.multi_cell(0, 10, txt=f"{chat['timestamp']} - {chat['sender']}: {chat['message']}")
        pdf.ln(2)

    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=chat_history.pdf'
    return response

@app.route('/history')
@login_required
def history():
    username = session.get('username')
    chats = load_history_chats(username)
    return render_template('history.html', chats=chats)

@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html', username=session.get('username'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()

    # Reload users to get the latest data
    users = load_users()
    current_username = current_user.username

    # Handle form submission
    if request.method == 'POST' and form.validate_on_submit():
        # Collect data from the form
        user_profile = {
            'name': form.name.data,
            'age': form.age.data,
            'gender': form.gender.data,
            'blood_type': form.blood_type.data,
            'medical_history': form.medical_history.data
        }

        # Update the user's profile data
        if current_username in users:
            users[current_username]['profile'] = user_profile
            save_users(users)
            flash('Profile updated successfully!', 'success')
        else:
            flash('User not found.', 'danger')

        return redirect(url_for('profile'))

    # If it's a GET request, populate the form with existing data
    if current_username in users and 'profile' in users[current_username]:
        user_profile = users[current_username]['profile']
        form.name.data = user_profile.get('name', '')
        form.age.data = user_profile.get('age', '')
        form.gender.data = user_profile.get('gender', '')
        form.blood_type.data = user_profile.get('blood_type', '')
        form.medical_history.data = user_profile.get('medical_history', '')

    return render_template('profile.html', form=form)


@app.route('/symptom_tracker', methods=['GET', 'POST'])
def symptom_tracker():
    global symptoms
    symptoms = load_symptoms()  # Reload symptoms from the file each time

    if request.method == 'POST':
        symptom_text = request.form['symptom']
        if symptom_text:
            new_symptom = {
                'symptom': symptom_text,
                'date_logged': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            symptoms.append(new_symptom)
            save_symptoms(symptoms)  # Save updated symptoms to file
        return redirect(url_for('symptom_tracker'))

    return render_template('symptom_tracker.html', symptoms=symptoms)


# Add the clear_symptoms route
@app.route('/clear_symptoms', methods=['POST'])
def clear_symptoms():
    global symptoms
    symptoms = []  # Clear the in-memory list
    save_symptoms(symptoms)  # Clear the symptoms file
    return '', 204  # Return 204 No Content to indicate success

@app.route('/download_symptoms_pdf')
@login_required
def download_symptoms_pdf():
    # Load the user-specific chat history and symptom data
    username = session.get('username')
    chat_history = load_history_chats(username)  # Load actual chat history for the logged-in user
    global symptoms  # assuming symptoms is a global list of symptom dictionaries

    # Create a PDF object
    pdf = FPDF()
    pdf.add_page()

    # Add DejaVu font for Unicode support
    pdf.add_font("DejaVu", "", FONT_PATH, uni=True)
    pdf.set_font("DejaVu", size=12)

    # Add Chat History section
    pdf.cell(200, 10, txt="Chat History", ln=True, align='C')
    pdf.ln(10)

    for chat in chat_history:
        timestamp = chat.get('timestamp', 'Unknown Date')
        sender = chat.get('sender', 'Unknown Sender')
        message = chat.get('message', '')

        # Reshape and apply bidi transformation for Arabic text
        reshaped_message = arabic_reshaper.reshape(message)
        bidi_message = get_display(reshaped_message)

        # Reshape sender name if it's in Arabic
        reshaped_sender = arabic_reshaper.reshape(sender)
        bidi_sender = get_display(reshaped_sender)

        # Format the line with timestamp, sender, and message
        line = f"[{timestamp}] {bidi_sender}: {bidi_message}"
        pdf.multi_cell(0, 10, txt=line)
        pdf.ln(2)

    # Add a divider line or some space before the next section
    pdf.ln(10)
    pdf.cell(200, 10, txt="-----------------------", ln=True, align='C')
    pdf.ln(10)

    # Add Symptom Tracker section
    pdf.cell(200, 10, txt="Symptom Tracker Report", ln=True, align='C')
    pdf.ln(10)

    for symptom in symptoms:
        date_logged = symptom.get('date_logged', 'Unknown Date')
        symptom_text = symptom.get('symptom', 'No symptom provided')

        # Reshape and apply bidi transformation for Arabic text
        reshaped_symptom = arabic_reshaper.reshape(symptom_text)
        bidi_symptom = get_display(reshaped_symptom)

        # Format the line with date and symptom text
        pdf.multi_cell(0, 10, txt=f"{date_logged} - {bidi_symptom}")
        pdf.ln(2)

    # Generate PDF as a bytearray (no encoding needed)
    pdf_output = pdf.output(dest='S')

    # Send the PDF file as a response
    return send_file(io.BytesIO(pdf_output), as_attachment=True, download_name='combined_report.pdf', mimetype='application/pdf')


@app.route('/download_history_pdf')
@login_required
def download_history_pdf():
    username = session.get('username')
    chats = load_history_chats(username)
    global symptoms  # assuming symptoms is a global list of symptom dictionaries

    # Create a PDF object
    pdf = FPDF()
    pdf.add_page()

    # Add DejaVu font for Unicode support using the absolute path
    pdf.add_font("DejaVu", "", FONT_PATH, uni=True)
    pdf.set_font("DejaVu", size=12)

    # Add title for Chat History
    pdf.cell(200, 10, txt="Chat History", ln=True, align='C')
    pdf.ln(10)

    # List each chat message
    for chat in chats:
        timestamp = chat.get('timestamp', 'Unknown Date')
        sender = chat.get('sender', 'Unknown Sender')
        message = chat.get('message', '')

        # Reshape and apply bidi algorithm to Arabic text
        if any('\u0600' <= c <= '\u06FF' for c in message):  # Check if there are Arabic characters
            reshaped_message = arabic_reshaper.reshape(message)
            bidi_message = get_display(reshaped_message)
        else:
            bidi_message = message

        # Display sender name in the same way if it's in Arabic
        if any('\u0600' <= c <= '\u06FF' for c in sender):
            reshaped_sender = arabic_reshaper.reshape(sender)
            bidi_sender = get_display(reshaped_sender)
        else:
            bidi_sender = sender

        # Format the line with timestamp, sender, and message
        line = f"[{timestamp}] {bidi_sender}: {bidi_message}"
        pdf.multi_cell(0, 10, txt=line)
        pdf.ln(2)

    # Add a separator line before symptoms section
    pdf.ln(10)
    pdf.cell(200, 10, txt="Symptom Tracker", ln=True, align='C')
    pdf.ln(10)

    # List each symptom
    for symptom in symptoms:
        date_logged = symptom.get('date_logged', 'Unknown Date')
        symptom_text = symptom.get('symptom', 'No symptom provided')
        line = f"{date_logged} - {symptom_text}"
        pdf.multi_cell(0, 10, txt=line)
        pdf.ln(2)

    # Generate PDF as a bytearray without encoding
    pdf_output = pdf.output(dest='S')

    # Send the PDF file as a response
    return send_file(io.BytesIO(pdf_output), as_attachment=True, download_name='combined_history_and_symptoms.pdf', mimetype='application/pdf')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vaccine_tracker')
def vaccine_tracker():
    return render_template('vaccine_tracker.html')

# Route to check vaccines
@app.route('/check_vaccines', methods=['POST'])
def check_vaccines():
    # Define all vaccines
    ALL_VACCINES = [
        "Chickenpox (varicella)",
        "COVID-19",
        "Influenza (Flu)",
        # Add more vaccines as needed
    ]

    # Get list of taken vaccines from the request data
    data = request.get_json()
    taken_vaccines = data.get('taken_vaccines', [])

    # Identify missing vaccines
    missing_vaccines = [vaccine for vaccine in ALL_VACCINES if vaccine not in taken_vaccines]

    return jsonify({'missing_vaccines': missing_vaccines})
if __name__ == '__main__':
    app.run(debug=True)