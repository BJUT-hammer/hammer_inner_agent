import requests
from bs4 import BeautifulSoup

from src.exceptions import LoginException, ServerException


class BaseClient:
    """
    BJUT educational administration clients
    """
    LOGIN_URL = "http://gdjwgl.bjut.edu.cn/default_vsso.aspx"
    LOGIN_DATA = {
        "username": "TextBox1",
        "password": "TextBox2",
    }
    LOGIN_DEFAULT_DATA = {  # 直接拼接到请求参数里
        "RadioButtonList1_2": "%D1%A7%C9%FA",  # 学生 gbk 编码
        "Button1": ""
    }
    SESSION_COOKIE_PARAM = "ASP.NET_SessionId"

    def __init__(self, ID, password):
        self.ID = ID
        self.password = password
        self.session = requests.session()
        self.is_login = False

    def login(self):
        """
        login with hidden url and set cookie
        :return:
        """
        def _is_login_success(res):
            soup = BeautifulSoup(res.content, 'html.parser')
            if "ERROR" in str(soup.title):
                return False
            return True

        request_data = dict(self.LOGIN_DEFAULT_DATA)
        request_data[self.LOGIN_DATA.get('username')] = self.ID
        request_data[self.LOGIN_DATA.get('password')] = self.password

        res = self.session.post(self.LOGIN_URL, data=request_data)
        assert res.status_code == 200

        if not _is_login_success(res):
            raise LoginException

        if not self.session.cookies.get("ASP.NET_SessionId"):
            raise ServerException

        self.is_login = True  # awful.. TODO: better way to check the login status