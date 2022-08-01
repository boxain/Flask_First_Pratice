from flask import Flask
from flask import render_template # 指定html模板
from flask import url_for # 網頁跳轉
from flask import redirect # 重新導向
from flask import request # 請求

app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        if request.values['send']=='送出':
            return render_template('index.html',name=request.values['user'])
    return render_template('index.html',name='')


@app.route('/second')
def test():
    return redirect(url_for('index')) 
    # 由於url_for只會回傳該參數的function路徑
    # 所以需要再藉由redirect重新導向


if __name__=='__main__':
    app.run(debug=True)


