import socket
from flask import Flask, request, send_from_directory, redirect, render_template, flash, url_for, jsonify, \
    make_response, abort

from googletrans import Translator
# from .eng_to_kamayo_word_translator_predict import EngToKamayoTranslator
# from .kamayo_to_eng_word_translator_predict import KamayoToEngTranslator
# from .kamayo_to_ceb_word_translator_predict import KamayoToCebTranslator
# from .ceb_to_kamayo_word_translator_predict import CebToKamayoTranslator
from eng_to_kamayo_word_translator_predict import EngToKamayoTranslator
from kamayo_to_eng_word_translator_predict import KamayoToEngTranslator
from kamayo_to_ceb_word_translator_predict import KamayoToCebTranslator
from ceb_to_kamayo_word_translator_predict import CebToKamayoTranslator

app = Flask(__name__)
app.config.from_object(__name__)  # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


eng_to_kamayo_w = EngToKamayoTranslator()
kamayo_to_eng_w = KamayoToEngTranslator()
kamayo_to_ceb_w = KamayoToCebTranslator()
ceb_to_kamayo_w = CebToKamayoTranslator()
translator = Translator()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return 'About Us'


@app.route('/eng_to_fra_word_translator', methods=['POST', 'GET'])
def eng_to_fra_word_translator():
    if request.method == 'POST':
        if 'sentence' not in request.form:
            flash('No sentence post')
            redirect(request.url)
        elif request.form['sentence'] == '':
            flash('No sentence')
            redirect(request.url)
        else:
            sent = request.form['sentence']
            translated = ceb_to_kamayo_w.translate_lang(sent)
            return render_template('eng_to_fra_word_translator_result.html', sentence=sent,
                                   translated=translated)
    return render_template('eng_to_fra_word_translator.html')


@app.route('/translate', methods=['POST', 'GET'])
def translate_eng():
    if request.method == 'POST':
    #     print(request.form['sentence'])
    #     if not request.json or 'sentence' not in request.json or 'level' not in request.json or 'target_lang' not in request.json:
    #         abort(400)
    #     sentence = request.json['sentence']
    #     level = request.json['level']
    #     target_lang = request.json['target_lang']
    # else:
    #     sentence = request.args.get('sentence')
    #     level = request.args.get('level')
    #     target_lang = request.args.get('target_lang')
        target_lang = request.json['target_lang']
        sentence = request.json['sentence']
        level = request.json['level']
        target_text = sentence

    if level == 'word' and target_lang == 'kamayo':
        cebu_translated = kamayo_to_ceb_w.translate_lang(sentence)
        english_translated = kamayo_to_eng_w.translate_lang(sentence)

        return jsonify({
            'sentence': sentence,
            'first_output' : cebu_translated + '|cebu',
            'second_output' : english_translated + '|english',
        })

    elif level == 'word' and target_lang == 'english':
        # target_text = kamayo_to_eng_w.translate_lang(sentence)
        kamayo_translated = eng_to_kamayo_w.translate_lang(sentence)
        cebu_result = translator.translate(sentence,src='en', dest='ceb')
        cebu_translated = cebu_result.text

        return jsonify({
            'sentence': sentence,
            'first_output' : cebu_translated + '|cebu',
            'second_output' : kamayo_translated + '|kamayo',
        })

    elif level == 'word' and target_lang == 'ceb':
        kamayo_translated = ceb_to_kamayo_w.translate_lang(sentence)
        english_result = translator.translate(sentence, src='ceb', dest='en')
        english_translated = english_result.text

        return jsonify({
            'sentence': sentence,
            'first_output' : english_translated + '|english',
            'second_output' : kamayo_translated + '|kamayo',
        })

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def main():
    hostname = socket.gethostname()
    IP = socket.gethostbyname(hostname)
    app.run(IP)


if __name__ == '__main__':
    main()
