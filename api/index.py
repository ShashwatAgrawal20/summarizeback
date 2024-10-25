from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.plaintext import PlaintextParser
from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words


import nltk
import os


from flask import Flask, request, jsonify
from flask_cors import CORS

from mediawikiapi import MediaWikiAPI, exceptions

app = Flask(__name__)
CORS(app)
LANGUAGE = "english"

current_dir = os.path.dirname(os.path.abspath(__file__))
nltk_data_dir = os.path.join(current_dir, 'nltk_data')
nltk.data.path.append(nltk_data_dir)


def get_summary(url=None, text=None, keyword=None, sentences_count=None):
    if url:
        parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
    elif text:
        parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
    elif keyword:
        mediawiki = MediaWikiAPI()
        try:
            page = mediawiki.page(keyword, auto_suggest=False)
            parser = PlaintextParser.from_string(
                page.content, Tokenizer(LANGUAGE))
        except exceptions.PageError:
            search_results = mediawiki.search(keyword)
            if not search_results:
                return jsonify({"error": "No search results found"}), 404
            page = mediawiki.page(search_results[0], auto_suggest=False)
            parser = PlaintextParser.from_string(
                page.content, Tokenizer(LANGUAGE))
    else:
        return jsonify({"error": "URL, text, or keyword is required"}), 400

    stemmer = Stemmer(LANGUAGE)
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    summarized_text = ""
    for sentence in summarizer(parser.document, sentences_count):
        summarized_text += str(sentence) + " "
    return jsonify({"summarized_text": summarized_text})


@app.route("/summarize", methods=["POST"])
def main():
    try:
        data = request.get_json()
        length = data.get("length") or 15
        url = data.get("url")
        raw_text = data.get("text")
        keyword = data.get("keyword")

        if not url and not raw_text and not keyword:
            return jsonify({"error": "URL, text or keyword is required"}), 400

        summarized_text = get_summary(
            url=url, text=raw_text, keyword=keyword, sentences_count=length)

        return summarized_text

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/ping')
def home():
    return 'pong!'


if __name__ == "__main__":
    app.run()
