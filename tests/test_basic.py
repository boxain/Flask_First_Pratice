import unittest
from flask import url_for
from app import create_app


class TestBasic(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app("testing")
        self.client = self.app.test_client()  # 模擬客戶端工具
        '''
            較難懂
        '''
        self.app_context = self.app.app_context() 
        self.app_context.push() # 因沒有request 所以手動入棧


    def tearDown(self) -> None:
        if self.app_context:
            self.app_context.pop()

    '''
        確認app有沒有好好活著
    '''
    def test_app_is_alive(self): 
        response = self.client.get(url_for("main.index_page"))
        self.assertEqual(response.status_code,200)


    '''
        確認藍圖有沒有好好載入
        blueprints是dict型態
    '''
    def test_blueprint(self):
        self.assertNotEqual(self.app.blueprints.get("main",None),None)
        self.assertNotEqual(self.app.blueprints.get("user",None),None)
        self.assertNotEqual(self.app.blueprints.get("admin",None),None)

