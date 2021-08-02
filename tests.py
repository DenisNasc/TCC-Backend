from flask_testing import TestCase
import unittest
import json

from app import create_app
from database.db import initialize_db
from config import TestConfig


class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app(TestConfig)

        app.config[
            "SQLALCHEMY_DATABASE_URI"
        ] = "sqlite:////home/denis/Documentos/Developer/tcc-denis-backend-v2/database/sqlite/test.sqlite"

        self.db = initialize_db(app)

        return app

    def setUp(self):
        self.db.create_all()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()


class UserTests(BaseTestCase):
    DEFAULT_SIGNUP_USER = {
        "name": "Laura",
        "password": "123",
        "email": "laura@gmail.com",
    }
    DEFAULT_LOGIN_USER = {
        "password": "123",
        "email": "laura@gmail.com",
    }

    def _signup_user(self, args=None):
        if not args:
            args = self.DEFAULT_SIGNUP_USER

        res = self.client.post("/v1/signup", json=args, follow_redirects=True)
        res_formated = json.loads(res.data.decode("UTF-8"))

        self.USER_ID = res_formated["userID"]
        return res, res_formated

    def _login_user(self, args=None):
        if not args:
            args = self.DEFAULT_LOGIN_USER

        res = self.client.post("/v1/login", json=args, follow_redirects=True)
        res_formated = json.loads(res.data.decode("UTF-8"))

        self.USER_ID = res_formated["userID"]
        return res, res_formated

    def test_signup_user(self):
        res, res_formated = self._signup_user()

        self.assert200(res)
        self.assertIn(
            "message",
            res_formated,
        )
        self.assertIn(
            "userID",
            res_formated,
        )

    def test_login_user(self):
        self._signup_user()
        res, res_formated = self._login_user()

        self.assert200(response=res)
        self.assertIn(
            "message",
            res_formated,
        )
        self.assertIn(
            "userID",
            res_formated,
        )

    def test_get_all_users_without_cookie(self):
        response = self.client.get("/v1/users", follow_redirects=True)

        self.assert401(response)

    def test_get_all_users(self):
        # APRENDER A COMO TESTAR ROTAS PROTEGIAS PELO JWT
        pass


if __name__ == "__main__":
    unittest.main()
