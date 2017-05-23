# py-browser-recognition

Inspired by [Chris Young's](https://github.com/chris--young) proof-of-concept [browser-recognition](https://github.com/chris--young/browser-recognition) app.

Transmuted into Python.

Checkout Chris's [README](https://github.com/chris--young/browser-recognition/blob/master/README.md) to see exactly what it does.

#### Setup
> Requires Python2.7 or newer and uses Flask to serve webapp

1. `pip install virtualenv`
2. `virtualenv .venv`
3. `source .venv/bin/activate`
4. `pip install Flask` or `pip install -r requirements.txt`
5. `export FLASK_APP=py-browser-recognition.py`
6. `flask run`