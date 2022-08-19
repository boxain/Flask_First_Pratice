from flask import url_for
from tests.helper import TestModel

class TestIndexPage(TestModel):
    def setUp(self) -> None:
        self.route = url_for("main.index_page") # 主頁面

    def test_get_with_no_auth(self):
        res = self.test_get() # TestResponse
        self.assertEqual(res.status_code,200) # 確認有連到線
        self.assertIn(b"Login",res.data) # 因為res.data是bytes,所以login前面要加b

    def test_get_with_auth(self):
        res = self.test_get(login="user")
        self.assertEqual(res.status_code,200) # 確認有連到線
        self.assertIn(b"Dashboard",res.data) 

'''
後面我們用了兩個測試，一個是在沒登入的情況下抓這個頁面，另一個是在有登入的情況下。
我們分別看他們有沒有回傳 200，然後後面我們再使用 assertIn 
來確定 "Login" 和 "Dashboard" 有沒有在回傳的 HTML 裡面 (res.data)，
我們會拿這個來當作判斷依據是因為
到時候網頁的 navbar 會根據有沒有登入來決定要用怎麼樣子的，
如果沒有登入當然就是顯示 login、register 等等，
有登入的話就是 dashboard、寫文章之類的按鈕，
這邊要注意的是，res.data 是一個 bytes 型別，
所以我們前面用的 assertIn 也要跟著他用 bytes 型別。
'''