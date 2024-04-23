from flask import Flask, render_template, request, jsonify
import dragonmapper.hanzi
from deep_translator import GoogleTranslator
import os
import easyocr

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
    translated_text = GoogleTranslator(source='auto', target='zh-CN').translate(word)
    return translated_text

def translate_chinese_word(chinese_word):
    translated = GoogleTranslator(source='auto', target='en').translate(chinese_word)
    return translated, chinese_to_pinyin(chinese_word)

def translate_img(img_path):
    reader = easyocr.Reader(['ch_sim','en'])
    results = reader.readtext(img_path, detail = 0)
    translation = ""
    og_text = ""
    for result in results:
        if (result != None):
            og_text += result
            translation += GoogleTranslator(source='auto', target='en').translate(result)
            translation += '\n'
    print(translation)
    os.remove(img_path)
    return translation, og_text


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

@app.route("/upload_image", methods=["POST"])
def upload_image():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = (file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        trans_img, og_text = translate_img(UPLOAD_FOLDER + filename)
        return jsonify({'translated_text': trans_img, 'chinese_text': og_text})

if __name__ == "__main__":
    app.run(debug=False)

