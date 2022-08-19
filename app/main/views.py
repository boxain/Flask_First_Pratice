from werkzeug.exceptions import HTTPException
from flask import render_template,redirect,url_for
from . import main_bp

@main_bp.route("/" , methods=["GET"])
def index_page():
    return render_template("index.html")

@main_bp.app_errorhandler(401)
def handler_401(e):
    return redirect(url_for("user.login_page"))

@main_bp.app_errorhandler(HTTPException)
def handler(e):
    return render_template("error.html",code=e.code,name=e.name,error=e),e

'''
第二個是處理 401 錯誤的 handler，我們在這邊讓他重新導向到登入頁面。
最後一個 handler 處理所有錯誤，並且使用了 e.code、e.name 來把一些內容傳入，
他們分別是 HTTP status code 和該錯誤的說明，像是 Not Found 之類的。在最後，
我們把 e.code 當成回傳的 HTTP status code。
'''

