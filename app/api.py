from flask import jsonify, render_template, request, redirect, url_for
from pypinyin import Style, pinyin
from app import app
from gtts import gTTS
from PIL import Image

import os
import cv2
import pytesseract

words = []
lang = None

def submit_words(words_list, language):
    global words, lang
    words = [word.strip() for word in words_list if word.strip()]
    lang = language
    return 'Words submitted'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_words', methods=['POST'])
def submit_words_route():
    words_list = request.form['words'].split('\n')
    language = request.form['lang']
    submit_words(words_list, language)
    return redirect(url_for('dictation_page'))

@app.route('/dictation_page.html')
def dictation_page():
    global words
    return render_template('dictation.html', words=words)

@app.route('/play_word/<string:word>/<string:lang>', methods=['GET'])
def play_word(word, lang):
    print("User typed: ", word, lang)
    try:
        tts = gTTS(text=word, lang=lang, slow=False)
        tts.save(f"app/static/audio/{word}_{lang}.mp3")
        return jsonify({'status': 'success'})
    except Exception as e:
        print(e)
        return jsonify({'status': 'error'}), 500

@app.route('/delete_audios.json', methods=['GET'])  # Ensure correct extension
def delete_audios():
    audio_dir = 'app/static/audio'
    if os.path.exists(audio_dir):
        for file in os.listdir(audio_dir):
            os.remove(os.path.join(audio_dir, file))
    return jsonify({'status': 'success'})

@app.route('/get_langs.json', methods=['GET'])
def get_langs():
    return jsonify({'langs': lang})

@app.route('/dict.html')
def dict():
    return render_template('dict.html',words=words)

@app.route('/convert_pinyin', methods=['GET'])
def convert_pinyin():
    data = request.args.get('data')
    pinyin_result = pinyin(data)
    pinyin_text = ' '.join([''.join(item) for item in pinyin_result])
    return jsonify({'pinyin': pinyin_text})

@app.route('/ocr', methods=['POST'])
def ocr_api():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided\n没有提供图像文件'}), 400

    image_file = request.files['image']
    image_path = './app/static/images/uploaded_image.jpg'
    image_file.save(image_path)
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)    
    text = pytesseract.image_to_string(Image.fromarray(gray), lang='chi_sim')
    os.remove(image_path)
    
    return jsonify({'text': text})

