from flask import Flask

app = Flask(__name__)


@app.route('/api')
def api():
    return 'Hello world'
