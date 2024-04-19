from flask import Flask, render_template, request, jsonify
import requests
import dragonmapper.hanzi
from deep_translator import GoogleTranslator

UPLOAD_FOLDER = './IMG/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def chinese_to_pinyin(word):
    return dragonmapper.hanzi.to_pinyin(word)

def translate_word(word):
    url = "https://api.mymemory.translated.net/get"
    params = {
        "q": word,
        "langpair": "en|zh-CN"
    }
    response = requests.get(url, params=params)
    translation_data = response.json()
    translated_text = translation_data["responseData"]["translatedText"]
    return translated_text

def translate_chinese_word(chinese_word):
    translated = GoogleTranslator(source='auto', target='en').translate(chinese_word)
    return translated, chinese_to_pinyin(chinese_word)


@app.route("/", methods=["GET", "POST"])
def translate_english():
    if request.method == "POST":
        word = request.form["word"]
        translated_text = translate_word(word)
        pinyin_text = chinese_to_pinyin(translated_text)
        return jsonify({'translated_text': translated_text, 'pinyin_text': pinyin_text})
    else:
        return render_template("index.html")

@app.route("/translate_chinese", methods=["POST"])
def translate_chinese():
    chinese_word = request.form["chinese_word"]
    translated_chinese_text, english_pronunciation = translate_chinese_word(chinese_word)
    return jsonify({'translated_chinese_text': translated_chinese_text, 'english_pronunciation': english_pronunciation})

if __name__ == "__main__":
    app.run(debug=False)

