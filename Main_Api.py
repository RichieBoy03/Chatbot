import sqlite3
import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from googletrans import Translator

api_key = os.getenv("API_KEY")
if api_key:
    print(f"API Key: {api_key}")
else:
    print("API Key is not set.")

genai.configure(api_key=api_key)

generation_config = genai.types.GenerationConfig(
    temperature=0.7,
    top_p=0.9,
    max_output_tokens=500
)

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config
)

translator = Translator()
app = Flask(__name__)

def connect_to_database():
    return sqlite3.connect("college.db")

def get_answer_from_db(user_input):
    conn = connect_to_database()
    cursor = conn.cursor()
    lower_input = user_input.lower()

    cursor.execute("SELECT answer FROM college_queries WHERE question = ?", (user_input,))
    result = cursor.fetchone()
    if result:
        conn.close()
        return result[0]

    courses = ["bca", "bcom", "bba", "bsc", "mca", "mba"]
    course_found = None
    for course in courses:
        if course in lower_input:
            course_found = course.upper()
            break

    keywords = ["fee", "fees", "structure", "cost", "charge", "tuition", "semester", "hostel"]
    if course_found:
        for keyword in keywords:
            if keyword in lower_input:
                cursor.execute(
                    "SELECT answer FROM college_queries WHERE question LIKE ? AND question LIKE ?",
                    (f"%{course_found}%", f"%{keyword}%")
                )
                result = cursor.fetchone()
                if result:
                    conn.close()
                    return result[0]

    for keyword in keywords:
        if keyword in lower_input:
            cursor.execute("SELECT answer FROM college_queries WHERE question LIKE ?", (f"%{keyword}%",))
            results = cursor.fetchall()
            if results:
                conn.close()
                return "\n".join([row[0] for row in results])

    cursor.execute(
        "SELECT answer FROM college_queries WHERE question LIKE ? OR answer LIKE ?",
        (f"%{user_input}%", f"%{user_input}%")
    )
    results = cursor.fetchall()
    if results:
        conn.close()
        return "\n".join([row[0] for row in results])

    conn.close()
    return None

def preprocess_input(user_input):
    return user_input.strip()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/home.html")
def home_html():
    return render_template("home.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("query")
    language = request.json.get("language", "en")

    if user_input.lower() in ["exit", "quit"]:
        return jsonify({"response": "Thank You For Chatting With Me. Goodbye!"})
    
    user_input = preprocess_input(user_input)
    translated_input = translator.translate(user_input, src=language, dest="en").text

    db_response = get_answer_from_db(translated_input)
    if db_response:
        translated_response = translator.translate(db_response, src="en", dest=language).text
        return jsonify({"response": translated_response})

    try:
        ai_response = model.generate_content(translated_input)
        translated_response = translator.translate(ai_response.text, src="en", dest=language).text
        return jsonify({"response": translated_response})
    except Exception as e:
        print(f"Error generating response: {e}")
        return jsonify({"response": "An error occurred while connecting to the bot. Please try again later."})

@app.route("/ui")
def ui():
    return render_template("ui.html")

@app.route("/future_enhancements")
def future_enhancements():
    return render_template("future_enhancements.html")

@app.route("/Support")
def support_capital():
    return render_template("Support.html")

@app.route("/support")
def support_lower():
    return render_template("Support.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/services")
def services():
    return render_template("services.html")

if __name__ == "__main__":
    app.run(debug=True)
