from flask import Flask, request, jsonify
from flask_cors import CORS
from newspaper import Article

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


if __name__ == '__main__':
    app.run(debug=True)
