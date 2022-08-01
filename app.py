from flask import Flask

app = Flask(__name__)

@app.route('/Flask')
def flask():
    return 'Hello Flask!'

@app.route('/')
def test():
    return 'Hello MotherFuck!'

if __name__=='__main__':
    app.run(debug=True)


