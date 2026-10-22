import os
from flask import Flask, render_template, request, session, redirect, url_for, jsonify

app = Flask(__name__)
app.secret_key = "love-secret-key-2024"

QUESTIONS = [
    {"id": "q1", "text": "Когда мы начали встречаться?", "options": ["15 марта", "28 сентября", "14 декабря"],
     "correct": "14 декабря"},
    {"id": "q2", "text": "Какое моё любимое прозвище для тебя?", "options": ["Заяц", "Любимый", "Котёнок"],
     "correct": "Котёнок"},
    {"id": "q3", "text": "Моё любимое развлечение?",
     "options": ["Сидеть в ТикТоке", "Сидеть в Ютубе", "Кататься с тобой на мопеде"],
     "correct": "Кататься с тобой на мопеде"},
    {"id": "q4", "text": "Моя любимая еда?", "options": ["Пицца", "Суши", "Много мясаааа"], "correct": "Много мясаааа"},
    {"id": "q5", "text": "Моё любимое животное?", "options": ["Котёнок", "Собака", "Дождевые черви"],
     "correct": "Котёнок"},
    {"id": "q6", "text": "Сколько мы вместе?", "options": ["1 год", "3 дня", "10 месяцев"], "correct": "10 месяцев"},
    {"id": "q7", "text": "Что я люблю, когда ты делаешь?", "options": ["Ругаешься", "Грустная", "Мило улыбаешься"],
     "correct": "Мило улыбаешься"},
    {"id": "q8", "text": "Где я хочу жить?", "options": ["Питер", "Украина", "Ялта"], "correct": "Ялта"},
    {"id": "q9", "text": "С кем я хочу жить в Ялте?", "options": ["С папой", "С котом", "С тобой вместе, Машуль"],
     "correct": "С тобой вместе, Машуль"},
    {"id": "q10", "text": "Кого я люблю больше всего на свете?", "options": ["Тебя", "Только тебя", "Конечно же тебя"],
     "correct": None},
]

LETTER_TEXT = """моя маленькая принцесса я очень сильно тебя люблю киса моя это письмо для тебя чтобы поднять тебе настроение а фоточки снизу это лишь маленькие фрагменты нашей маленькой истории которая будет еще продолжаться дальше я люблю тебя безумно сильно машуль ты у меня самая красивая на всем свете ты изумительная божественно милая твои глазки очеровательны когда я в них смотрю я тону в них я уверен что ты пока читаешь это письмо улыбаешься я думаю что ты похвастаешься перед своими подругами какой я у тебя прекрасный парень и сделал для тебя такой сайтик с нашей маленькой историей я очень хочу чтобы мы больше не ссорились а жили вместе дружно и говорили друг другу только теплые и милые слова я очень тебя люблю и хочу скорее приехать и провести все время вместе я скучаю по тебе и очень сильно тебя люблю машуль хорошего дня тебе моя маленькая принцесса"""


@app.route("/")
def welcome():
    session.clear()
    return render_template("index.html", page="welcome")


@app.route("/letter")
def letter():
    return render_template("index.html", page="letter")


@app.route("/survey")
def survey():
    return render_template("index.html", page="survey", questions=QUESTIONS)


@app.route("/api/check", methods=["POST"])
def api_check():
    data = request.get_json()
    qid = data.get("id")
    answer = data.get("answer")
    question = next((q for q in QUESTIONS if q["id"] == qid), None)
    if not question:
        return jsonify({"ok": False, "error": "unknown question"}), 400
    is_correct = question["correct"] is None or answer == question["correct"]
    return jsonify({"ok": True, "correct": is_correct})


@app.route("/confession")
def confession():
    photos_dir = os.path.join(app.static_folder, 'photos')
    photo_urls = []

    if os.path.exists(photos_dir):
        files = sorted(os.listdir(photos_dir))
        for filename in files:
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')) and not filename.startswith('.'):
                photo_urls.append(url_for("static", filename=f"photos/{filename}"))

    return render_template("index.html", page="confession", photos=photo_urls, letter=LETTER_TEXT.strip())


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)