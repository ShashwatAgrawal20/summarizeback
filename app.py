from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

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


def get_summary(url, sentences_count):
    parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
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
        url = data.get("url")
        length = data.get("length") or 15

        if not url:
            return jsonify(
                {"error": "Please provide a valid URL in the request body"}),
            400

        summarized_text = get_summary(url, length)
        return jsonify({"summarized_text": summarized_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
