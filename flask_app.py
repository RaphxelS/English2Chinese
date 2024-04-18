from flask import Flask, render_template, request
import requests
import dragonmapper.hanzi

app = Flask(__name__)

def english_to_pinyin(word):
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

@app.route("/", methods=["GET", "POST"])
def index():
    translated_text = None
    pinyin_text = None
    if request.method == "POST":
        word = request.form["word"]
        translated_text = translate_word(word)
        pinyin_text = english_to_pinyin(translated_text)
    return render_template("index.html", translated_text=translated_text, pinyin_text=pinyin_text)

if __name__ == "__main__":
    app.run(debug=True)

