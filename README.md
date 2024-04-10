# summarizeback

### Setting up a Virtual Environment

**Note: It's recommended to create the virtual environment (venv) within the project directory. To do so, navigate to the project directory using the `cd` command and then proceed with the following instructions.**

#### Windows

```bash
python -m venv dev
dev\Scripts\activate
```

#### Linux
```bash
python -m venv dev
source dev/bin/activate
```

### Install dependencies after you have setup the Virtual Environment
```bash
pip install -r requirements.txt
```

**Note:-** if you get some error related to **nltk punkt** just run the python interpreter and run.
```python
import nltk
nltk.download('punkt')
```

### Testing summarization
1. Activate the venv
2. Start the `flask` app -> `flask run`
3. Make a POST request to `/summarize` endpoint.
You can send 4 params
1 -> url
2 -> raw text
3 -> keyword
4 -> length -> defaults to 15
> If both url, text and keyword are provided it will summarize the url content.
1. URL Summarization
```bash
curl -X POST -H "Content-Type: application/json" -d '{"url": "https://example.com"}' http://127.0.0.1:5000/summarize
```
2. Text Summarization
> Make sure while testing from the CLI you don't want the new line character in your json payload
```bash
curl -X POST -H "Content-Type: application/json" -d '{"text": "The Domain Name System (DNS) is a hierarchical and distributed naming system for computers, services, and other resources in the Internet or other Internet Protocol (IP) networks. It associates various information with domain names (identification strings) assigned to each of the associated entities. Most prominently, it translates readily memorized domain names to the numerical IP addresses needed for locating and identifying computer services and devices with the underlying network protocols.[1] The Domain Name System has been an essential component of the functionality of the Internet since 1985.", "length": "3"}' http://127.0.0.1:5000/summarize
```
3. Keyword Summarization
```bash
curl -X POST -H "Content-Type: application/json" -d '{"keyword":"gcc compiler", "length": "30"}' http://127.0.0.1:5000/summarize
```
OR
Use the provided `test.html` to make your life easier.
