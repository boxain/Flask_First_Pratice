from flask import url_for
from tests.helper import TestModel


class TestDashboardPage(TestModel):
    def setUp(self) -> None:
        super().setUp()
        self.route = url_for("admin.admin_dashboard_posts_page")

    def test_get_with_no_auth(self):
        res = self.test_get()
        self.assertEqual(res.status_code,200)
        self.assertIn(b"Login",res.data)

    def test_get_with_auth(self):
        res = self.test_get(login="user")
        self.assertEqual(res.status_code,403)

    def test_get_with_auth(self):
        res = self.test_get(login="admin")
        self.assertEqual(res.status_code,200)
        self.assertIn(b"Admin Dashboard",res.data)


class TestManageUserPage(TestModel):
    def setUp(self) -> None:
        super().setUp()
        self.route = url_for("admin.manage_user_page")
        self.data_ok = {
            "username":"user3",
            "password":"password",
            "email":"user3@a.a",
            "is_admin":False,
        }
        self.data_bad_empty_filed = {"username":"user3"}

    def test_get_with_no_auth(self):
        res = self.test_get()
        self.assertEqual(res.status_code,200)
        self.assertIn(b"Login",res.data)

    def test_get_with_user_auth(self):
        res = self.test_get(login="user")
        self.assertEqual(res.status_code,403)

    def test_get_with_admin_auth(self):
        res = self.test_get(login="admin")
        self.assertEqual(res.status_code,200)

    # 可能會出錯
    def test_post_ok(self):
        res = self.test_post(login="admin",data=self.data_ok)
        self.assertEqual(res.status_code,200)
        self.assertIn(b"Add user successfully.",res.data)

    def test_post_bad_empty_field(self):
        res = self.test_post(login="admin",data=self.data_bad_empty_filed)
        self.assertEqual(res.status_code,200)
        self.assertIn(b"This field is required.",res.data)