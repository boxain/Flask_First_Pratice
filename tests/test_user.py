from flask import url_for
from tests.helper import TestModel

class TestLoginPage(TestModel):
    def setUp(self) -> None:
        super().setUp()
        self.route = url_for("user.login_page")
        self.user_data_bad_wrong_password = {"username":"user","password":"bad"}

    
    def test_get_with_no_auth(self):
        res = self.test_get()
        self.assertEqual(res.status_code,200)
        self.assertIn(b"Login",res.data)


    def test_get_with_auth(self):
        res = self.test_get("user")
        self.assertEqual(res.status_code,200)
        self.assertIn(b"Dashboard",res.data)


    
    def test_post_ok(self): 
        res = self.test_post(data=self.user_data) # 不確定是否要加Login的值
        self.assertEqual(res.status_code,200)
        self.assertIn(b"Dashboard", res.data)

    
    def test_post_bad_wrong_password(self):
        res = self.test_post(data=self.user_data_bad_wrong_password)
        self.assertEqual(res.status_code,200)
        self.assertIn(b"Wrong username or password.",res.data)


class RegisterPageTest(TestModel):
    def setUp(self) -> None:
        super().setUp()
        self.route = url_for("user.register_page")
        self.register_data_ok = {
            "username":"user2",
            "password":"useruser",
            "repeat_passwoed":"useruser",
            "email":"user@a.a",
        }

        self.register_data_bad_too_short_password = {
            "username":"user2",
            "password":"short",
            "repeat_password":"short",
            "emial":"user@a.a",
        }

    
    def test_get_with_no_auth(self):
        res = self.test_get()
        self.assertEqual(res.status_code,200)
        self.assertIn(b"Login",res.data)


    def test_get_with_auth(self):
        res = self.test_get(login="user")
        self.assertEqual(res.status_code,200)
        self.assertIn(b"Dashboard",res.data)


    def test_post_ok(self):
        res = self.test_post(data=self.register_data_ok)
        self.assertEqual(res.status_code,200)
        self.assertIn(b"Login",res.data)


    def test_post_bad_too_short_password(self):
        res = self.test_post(data=self.register_data_bad_too_short_password)
        self.assertEqual(res.status_code,200)
        self.assertIn(b"The password must contain at least 6 characters.",res.data) 

        