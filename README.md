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
You can send 2 params
1 -> url
2 -> length -> defaults to 15
```bash
curl -X POST -H "Content-Type: application/json" -d '{"url": "https://example.com"}' http://127.0.0.1:5000/summarize
```
OR
Use the provided `test.html` to make your life easier.
