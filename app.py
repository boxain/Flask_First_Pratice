from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hellow'

@app.route('/test')
def test():
    return 'This is test'

if __name__=='__main__':
    app.run()


