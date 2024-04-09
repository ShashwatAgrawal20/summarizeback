from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.plaintext import PlaintextParser
from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
LANGUAGE = "english"

'''
I am aware of the code duplication for `text and url` summarization,
it was intentional as if I don't do that and try to make the code more
generic then the HTMLParser content has to be manually parsed in text
which is more computationally heavy.
'''


def get_url_summary(url, sentences_count):
    parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    summarized_text = ""
    for sentence in summarizer(parser.document, sentences_count):
        summarized_text += str(sentence) + " "
    return summarized_text


def get_text_summary(text, sentences_count):
    parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    summarized_text = ""
    for sentence in summarizer(parser.document, sentences_count):
        summarized_text += str(sentence) + " "
    return summarized_text


@app.route("/summarize", methods=["POST"])
def main():
    try:
        data = request.get_json()
        length = data.get("length") or 15
        url = data.get("url")
        raw_text = data.get("text")

        if not url and not raw_text:
            return jsonify({"error": "You have to provide Something"}), 400
        if url:
            summarized_text = get_url_summary(url, length)
        else:
            summarized_text = get_text_summary(raw_text, length)

        return jsonify({"summarized_text": summarized_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
