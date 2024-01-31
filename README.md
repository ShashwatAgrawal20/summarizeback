# summarizeback

### Testing Text extraction locally
1. Activate the venv
2. Start the `flask` app -> `flask run`
3. Make a POST request to `/extract-text` endpoint.
```bash
curl -X POST -H "Content-Type: application/json" -d '{"url": "https://example.com"}' http://127.0.0.1:5000/extract-text
```
OR

Use the provided `test.html` to make your life easier.


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
