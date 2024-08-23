from flask import Flask, jsonify, render_template, request, redirect, url_for
import random
import os
from gtts import gTTS

words = []
lang = None

def submit_words(words_list, language):
    global words, lang
    words = [word.strip() for word in words_list if word.strip()]
    lang = language
    return 'Words submitted'

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/submit_words', methods=['POST'])
    def submit_words_route():
        words_list = request.form['words'].split('\n')
        print(words_list)
        language = request.form['lang']
        submit_words(words_list, language)
        return redirect(url_for('dictation_page'))

    @app.route('/dictation_page')
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
        
    @app.route('/delete_audios', methods=['GET'])
    def delete_audios():
        for file in os.listdir('app/static/audio'):
            os.remove(f'app/static/audio/{file}')
        return jsonify({'status': 'success'})
    
    return app
