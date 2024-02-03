from flask import Flask, request, jsonify
from flask_cors import CORS
from newspaper import Article
from transformers import pipeline
from urllib.parse import urlparse

app = Flask(__name__)
CORS(app)


def extract_text_from_url(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        text_content = article.text
        return text_content
    except Exception as e:
        return f"Error extracting text: {str(e)}"


@app.route('/extract-text', methods=['POST'])
def extract_text():
    try:
        data = request.get_json()
        url = data.get('url')

        if not url:
            return jsonify(
                {'error': 'Please provide a valid URL in the request body'}),
            400

        text_content = extract_text_from_url(url)
        return jsonify({'text_content': text_content})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
    
def summarize_text_from_url(url):
    try:
        if is_valid_url(url):
            urltext = extract_text_from_url(url)
        else:
         urltext = url

        summarizer = pipeline("summarization")
        text = urltext
        summary = summarizer(text, max_length=1000, min_length=100, length_penalty=2.0)
        summarycontent = summary[0]['summary_text']
        return summarycontent
    except Exception as e:
            return f"Error summarizing text: {str(e)}"


@app.route('/summarize-text', methods=['POST'])
def summarize_text():
    try:
        data = request.get_json()
        url = data.get('url')

        if not url:
            return jsonify(
                {'error': 'Please provide a valid text content in the request body'}),
            400

        text_content = summarize_text_from_url(url)
        return jsonify({'text_content': text_content})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
