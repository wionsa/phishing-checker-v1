from flask import Flask, request, render_template
import requests
import os
from dotenv import load_dotenv
import g4f
from g4f.client import Client
from flask_cors import CORS
import re
import markdown

app = Flask(__name__)
CORS(app)

load_dotenv()
VirusTotal_API_KEY = os.getenv("VT_API_KEY")

@app.route('/')
def home():
    return "Server work correct!"

@app.route('/index')
def index():
    return render_template('index.html')

def load_whitelist(path="data/whitelist.txt"):
    try:
        if not os.path.exists("data"):
            os.makedirs("data")
        with open(path, "r") as f:
            return set(line.strip().lower() for line in f if line.strip())
    except FileNotFoundError:
        return set()

def analyze_virustotal_url(url):
    try:
        url_scan = requests.post(
            "https://www.virustotal.com/api/v3/urls",
            headers={"x-apikey": VirusTotal_API_KEY},
            data={"url": url}
        ).json()
        url_id = url_scan["data"]["id"]
        url_analysis = requests.get(
            f"https://www.virustotal.com/api/v3/analyses/{url_id}",
            headers={"x-apikey": VirusTotal_API_KEY}
        ).json()
        stats = url_analysis["data"]["attributes"]["stats"]
        malicious = stats.get("malicious", 0)
        suspicious = stats.get("suspicious", 0)
        if malicious > 0 or suspicious > 0:
            return f"URL містить шкідливі ознаки: шкідливих — {malicious}, підозрілих — {suspicious}"
        return "URL не містить шкідливих ознак"
    except Exception as e:
        return f"Помилка при перевірці URL: {str(e)}"

def analyze_virustotal_file(file):
    try:
        file_scan = requests.post(
            "https://www.virustotal.com/api/v3/files",
            headers={"x-apikey": VirusTotal_API_KEY},
            files={"file": (file.filename, file.stream, file.mimetype)}
        ).json()
        file_id = file_scan["data"]["id"]
        file_analysis = requests.get(
            f"https://www.virustotal.com/api/v3/analyses/{file_id}",
            headers={"x-apikey": VirusTotal_API_KEY}
        ).json()
        stats = file_analysis["data"]["attributes"]["stats"]
        malicious = stats.get("malicious", 0)
        suspicious = stats.get("suspicious", 0)
        if malicious > 0 or suspicious > 0:
            return f"Файл містить шкідливі ознаки: {malicious} шт."
        return "Файл не містить шкідливих ознак"
    except Exception as e:
        return f"Помилка при перевірці файлу: {str(e)}"

def get_ai_analysis(text):
    prompt = (
        f"Ти автоматичний детектор фішингу. Проаналізуй цей текст на ознаки шахрайства, "
        f"тиску чи підозрілих вимог. Надай детальний висновок українською мовою. Текст:\n\n{text}"
    )
    
    # 1. Списки для перебору (від найнадійніших до запасних)
    test_models = ["gpt-4o", "gpt-4", "gpt-3.5-turbo", "claude-3-haiku", "llama-3.1-70b"]
    
    # Використовуємо автоматичний вибір провайдера через Client, 
    # але з обмеженням за часом (timeout)
    client = Client()

    print(f"Починаю пошук робочої моделі ШІ...")

    # 2. Пробуємо спочатку топові моделі
    for model_name in test_models:
        try:
            print(f"Спроба з моделлю: {model_name}...")
            
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                # Можна додати конкретних провайдерів, якщо хочеш звузити пошук:
                # provider=g4f.Provider.Blackbox 
            )
            
            res_text = response.choices[0].message.content
            
            if res_text and len(res_text) > 50: # Перевірка, що це не помилка "Model not found"
                print(f"Успішно отримано відповідь (модель: {model_name})!")
                return markdown.markdown(res_text)
                
        except Exception as e:
            print(f"Модель {model_name} не спрацювала: {str(e)[:50]}...")
            continue

    # 3. Якщо конкретні моделі не підійшли, пробуємо "автоматичний" режим без вказання моделі
    try:
        print("Спроба автоматичного підбору провайдера та моделі...")
        response = client.chat.completions.create(
            model="", # Порожня модель змушує g4f обрати найкращий варіант за замовчуванням
            messages=[{"role": "user", "content": prompt}]
        )
        res_text = response.choices[0].message.content
        if res_text:
            return markdown.markdown(res_text)
    except:
        pass

    return "❌ На жаль, усі ШІ-провайдери зараз перевантажені. Спробуйте ще раз через 30 секунд."

@app.route('/analyze', methods=['POST'])
def analyze():
    if request.is_json:
        data = request.get_json()
        url = data.get('url')
        text = data.get('text', '')
        email = data.get('email')
    else:
        url = request.form.get('url')
        text = request.form.get('text', '')
        email = request.form.get('email')
    file = request.files.get('file')

    results = {}

    # 1. Email Check
    whitelist = load_whitelist()
    results["email_check"] = (
        "Адреса безпечна (у білому списку)" 
        if email and email.strip().lower() in whitelist 
        else "Адреса відсутня у білому списку"
    )

    # 2. GPT Analysis
    results['text_check'] = get_ai_analysis(text)

    # 3. URL Check
    results["url_check"] = analyze_virustotal_url(url) if url else "URL не вказано"

    # 4. File Check
    results["file_check"] = analyze_virustotal_file(file) if file and file.filename else "Файл не завантажено"

    return render_template('result.html', results=results)

if __name__ == '__main__':
    cert_path = 'ssl/server.crt'
    key_path = 'ssl/server.key'
    
    if os.path.exists(cert_path) and os.path.exists(key_path):
        app.run(host='0.0.0.0', port=5555, ssl_context=(cert_path, key_path))
    else:
        print("SSL сертифікати не знайдено, запуск у звичайному режимі...")
        app.run(host='0.0.0.0', port=5555)
