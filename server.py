import os
import time
import torch
from torch.quantization import quantize_dynamic
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

torch.set_num_threads(6)
torch.backends.quantized.engine = 'qnnpack'  # or 'fbgemm' if you are using x86_64

languages = [ ['Afrikaans', 'af'], ['Albanian', 'sq'], ['Amharic', 'am'], ['Arabic', 'ar'], ['Armenian', 'hy'], ['Asturian', 'ast'], ['Azerbaijani', 'az'], ['Bashkir', 'ba'], ['Belarusian', 'be'], ['Bengali', 'bn'], ['Bosnian', 'bs'], ['Breton', 'br'], ['Bulgarian', 'bg'], ['Burmese', 'my'], ['Catalan', 'ca'], ['Cebuano', 'ceb'], ['Central Khmer', 'km'], ['Chinese', 'zh'], ['Croatian', 'hr'], ['Czech', 'cs'], ['Danish', 'da'], ['Dutch', 'nl'], ['English', 'en'], ['Estonian', 'et'], ['Finnish', 'fi'], ['French', 'fr'], ['Fulah', 'ff'], ['Gaelic', 'gd'], ['Galician', 'gl'], ['Ganda', 'lg'], ['Georgian', 'ka'], ['German', 'de'], ['Greeek', 'el'], ['Gujarati', 'gu'], ['Haitian', 'ht'], ['Hausa', 'ha'], ['Hebrew', 'he'], ['Hindi', 'hi'], ['Hungarian', 'hu'], ['Icelandic', 'is'], ['Igbo', 'ig'], ['Iloko', 'ilo'], ['Indonesian', 'id'], ['Irish', 'ga'], ['Italian', 'it'], ['Japanese', 'ja'], ['Javanese', 'jv'], ['Kannada', 'kn'], ['Kazakh', 'kk'], ['Korean', 'ko'], ['Lao', 'lo'], ['Latvian', 'lv'], ['Lingala', 'ln'], ['Lithuanian', 'lt'], ['Luxembourgish', 'lb'], ['Macedonian', 'mk'], ['Malagasy', 'mg'], ['Malay', 'ms'], ['Malayalam', 'ml'], ['Marathi', 'mr'], ['Mongolian', 'mn'], ['Nepali', 'ne'], ['Northern Sotho', 'ns'], ['Norwegian', 'no'], ['Occitan (post 1500)', 'oc'], ['Oriya', 'or'], ['Panjabi', 'pa'], ['Persian', 'fa'], ['Polish', 'pl'], ['Portuguese', 'pt'], ['Pushto', 'ps'], ['Romanian', 'ro'], ['Russian', 'ru'], ['Serbian', 'sr'], ['Sindhi', 'sd'], ['Sinhala', 'si'], ['Slovak', 'sk'], ['Slovenian', 'sl'], ['Somali', 'so'], ['Spanish', 'es'], ['Sundanese', 'su'], ['Swahili', 'sw'], ['Swati', 'ss'], ['Swedish', 'sv'], ['Tagalog', 'tl'], ['Tamil', 'ta'], ['Thai', 'th'], ['Tswana', 'tn'], ['Turkish', 'tr'], ['Ukrainian', 'uk'], ['Urdu', 'ur'], ['Uzbek', 'uz'], ['Vietnamese', 'vi'], ['Welsh', 'cy'], ['Western Frisian', 'fy'], ['Wolof', 'wo'], ['Xhosa', 'xh'], ['Yiddish', 'yi'], ['Yoruba', 'yo'], ['Zulu', 'zu'] ]

m2m_model = "m2m100_1.2B"
#m2m_model = "m2m100_418M"

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

class LanguageModel:
    def __init__(self):
        self.model = M2M100ForConditionalGeneration.from_pretrained(m2m_model)
        self.model = quantize_dynamic(self.model, {torch.nn.Linear}, dtype=torch.qint8)
        self.tokenizer = M2M100Tokenizer.from_pretrained(m2m_model)

    def translate(self, src, out, text):
        self.tokenizer.src_lang = src
        encoded_input = self.tokenizer(text, return_tensors="pt")
        generated_tokens = self.model.generate(**encoded_input, forced_bos_token_id=self.tokenizer.get_lang_id(out))
        return self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]

print("*** Loading Model...", flush=True, end="")
app.language_model = LanguageModel()
print("READY", flush=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', src_lang='en', out_lang='en', text='', translated_text='', elapsed=0, languages=languages)
    elif request.method == 'POST':
        start_time = time.time()
        src_lang = request.form.get('src_lang')
        out_lang = request.form.get('out_lang')
        text = request.form.get('text')
        translated_text = app.language_model.translate(src_lang, out_lang, text)
        elapsed = int(time.time() - start_time)
        return render_template('index.html',src_lang=src_lang, out_lang=out_lang, text=text, elapsed=elapsed, translated_text=translated_text, languages=languages)

@app.route('/api/translate.json', methods=['POST'])
def api_translate():
    data = request.get_json()
    src_lang = data.get('src_lang')
    out_lang = data.get('out_lang')
    text = data.get('text')
    
    if not src_lang or not out_lang or not text:
        return jsonify({"error": "Missing required parameters"}), 400

    translated_text = app.language_model.translate(src_lang, out_lang, text)
    return jsonify({"translation": translated_text})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8015)
