from os import getenv
from os import urandom

class Config:
    # Flask-Mail
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 456
    MAIL_USE_SSL = True
    MAIL_USERNAME = getenv("MAIL_USERNAME")
    MAIL_PASSWORD = getenv("MAIL_PASSWORD")
    # Flask-SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Testing(Config):
    # Flask
    ENV = "TESTING"
    TESTING = True
    SECRET_KEY = "cyn54g544mxng"
    SERVER_NAME = "localhost"
    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory"
    # Flask-WTF
    WTF_CSRF_ENABLED = False

class Development(Config):
    # Flask
    ENV = "DEVELOPMENT"
    DEBUG = True
    SECRET_KEY = "cyn54g544mxng"
    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"

class Production(Config):
    # Flask 
    ENV = "PRODUCTION"
    SECRET_KEY = urandom(32)
    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URI")

'''
ENV 就是代表環境 (environment)。有些其他的環境變數也可能會被影響，像是馬上要講到的 DEBUG。

DEBUG 是指示 flask 要不要開起 debug 工具用的，這些工具之前有提過了。如果 ENV=development，那 DEBUG 會自動設為 True。

SECRET_KEY 之前也提過，是用來處理一些登入、session 相關的事情用的。理論上我們會用 urandom 來生成 (如 production)，
但因為他如果改變的話會讓舊的 session 都失效，開發的時候要一直重新登入很煩，所以就讓它靜態。

TESTING 會讓 flask 開啟一些測試用的功能，而且有些套件的功能可能會改變，像是 Flask-Mail 在 TESTING=True 的時候就不會真的寄信出去，
而是會打在 console。

SERVER_NAME 在這裡是專門給測試用的，因為他跟平常使用的時候會有不一樣的狀態，所以會導致 url_for 無法使用。

SQLALCHEMY_DATABASE_URI 是用來指定資料庫位置的設定，像我們開發的時候用 sqlite，就把檔案放在同一個目錄；測試的時候資料量不大，
就把它放在記憶體就好；真正上線的時候就看環境要給甚麼，如果換一個資料庫的話就會把前面的 sqlite: 改掉。要特別注意一下他有三個 /，
而放在記憶體的話前後有冒號。

前面有提到 flask-wtf 可以處理 CSRF 的攻擊，他用的就是 csrf_token，而 WTF_CSRF_ENABLED 就是用來設定要不要打開 csrf_token 的設定。
因為在測試的時候，我們不會像正常在使用一樣實際按下送出，而是直接傳資料到後端，所以就會被 csrf_token 擋下來。因為如此，我們在測試的時候會把它關掉，
讓測試順利一點，反正測試不會攻擊我們。

最後我們還需要加入一個小小的 dict，這樣到時候製造 app 的時候才有對照表，我們把環境的名稱對到他們分別要用到的設定檔，這個東西會在明天使用到。

'''

configs = {
    "development":Development,
    "testing":Testing,
    "production":Production
}