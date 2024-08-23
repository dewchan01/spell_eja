from flask import jsonify, render_template, request, redirect, url_for
from app import app
import random
from gtts import gTTS
import os

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
    random.shuffle(words)
    return render_template('dictation.html', words=words)

@app.route('/play_word/<word>', methods=['GET'])
def play_word(word):
    global lang
    try:
        tts = gTTS(text=word, lang=lang, slow=False)
        tts.save(f"app/static/audio/{word}.mp3")
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