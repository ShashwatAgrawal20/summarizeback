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

from mediawikiapi import MediaWikiAPI, exceptions

app = Flask(__name__)
CORS(app)
LANGUAGE = "english"


def get_summary(url=None, text=None, keyword=None, sentences_count=None):
    if url:
        parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
    elif text:
        parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
    else:
        mediawiki = MediaWikiAPI()
        try:
            wiki_url = mediawiki.page(keyword).url
        except exceptions.PageError:
            search_results = mediawiki.search(keyword)
            if not search_results:
                return jsonify({"error": "No search results found"}), 404
            wiki_url = mediawiki.page(search_results[0]).url

        parser = HtmlParser.from_url(wiki_url, Tokenizer(LANGUAGE))

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
