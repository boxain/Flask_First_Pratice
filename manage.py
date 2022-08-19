from os import getenv
from unicodedata import name # 取得環境變數
from app import create_app , db
from app.database import init , reset , add_user 
from dotenv import load_dotenv # 讀取環境變數套件
from flask_migrate import Migrate # 資料庫版本套件
import unittest # 測試套件
from app.database.helper import add_post

load_dotenv()


app = create_app(getenv("FLASK_ENV"))

# models.py更動後才能建立新的版本
migrate = Migrate(app,db,render_as_batch=True)
'''
render_as_batch 的參數，會加入他是因為我們開發中先使用 sqlite，
但他遇到刪除欄位的時候會爆炸，加上這個參數之後他就會換個方式，
會變成把本來的資料庫砍掉然後重建，再把舊的資料複製過去新的，
所以就可以避免掉 sqlite 不讓我們刪除的問題
'''

@app.shell_context_processor
def  make_shell_context():
    return globals()


@app.cli.command(name="init_db")
def init_db():
    init()


@app.cli.command(name="reset_db")
def reset_db():
    reset()


@app.cli.command(name="create_user")
def create_user():
    username = input("Username: ")
    password = input("Password: ")
    email = input("Email: ")
    is_admin = True if input("Is admin or not (y or n): ") == "y" else False
    if add_user(username=username,password=password,email=email,is_admin=is_admin):
        print("OK")
    else:
        print("Failed")


@app.cli.command(name="create_post")
def create_post():
    author_id = 3
    title = input("Title: ")
    description = input("Description: ")
    content = input("content: ")
    
    if add_post(author_id,title,description,content):
        print("OK")
    else:
        print("Failed")


# 未試過
@app.cli.command()
def test():
    
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestResult(stream=None,verbosity=2,descriptions=None).run(tests)
    



