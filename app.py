from flask import Flask

app = Flask(__name__)

@app.route('/')
def helloIndex():
    return 'Hello World from Python Flask!...This is production cluster'

app.run(host='0.0.0.0', port=5000)
