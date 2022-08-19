import unittest
from flask import url_for
from app import create_app
from app.database import db , add_user

class TestModel(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.user_data = {"username":"user","password":"user"}
        self.admin_data = {"username":"admin","password":"admin"}
        generate_test_data()
    
    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all() # 刪除所有資料表
        if self.app_context is not None:
            self.app_context.pop()

    def test_user_login(self):
        return self.client.post(url_for("user.login_page"),data=self.user_data)

    def test_admin_login(self):
        return self.client.post(url_for("user.login_page"),data=self.admin_data)

    def test_login(self,login):
        if login == "user":
            self.test_user_login()
        if login == "admin":
            self.test_admin_login()
    
    def test_get(self,login=False):
        self.test_login(login)
        # 未登入回傳頁面
        res = self.client.get(self.route,follow_redirects=True)
        return res

    def test_post(self,login=False,data=None):
        self.login(login)
        # 未登入回傳頁面
        res = self.client.post(self.route,data=data,follow_redirects=True)
        return res

    
def generate_test_data():
    db.create_all()
    add_user("user","user","user@user.com")
    add_user("admin","admin","admin@admin.com",is_admin=True)


'''

接下來我們自己定義了 get 和 post 兩個函式，讓它包含登入的功能，
登入有很多種寫法，但有時候並沒有那麼直觀，
可能會遇到明明登入了但後面發請求的時候又變成沒登入，
這常常都是因為 context 不對。post 的部分跟剛剛一樣都使用 data 參數來把資料傳送給後端。
我們還用到了一個叫做 follow_redirects 的參數，
如果不讓他 follow 的話，那 status_code 就會變成 302，
然後我們看到的資料也都是重新導向頁面的資料，
而這通常不是我們樂見的 (除非我們只想確定他有重新導向)，
因此在此處我們加上這個參數。

'''


