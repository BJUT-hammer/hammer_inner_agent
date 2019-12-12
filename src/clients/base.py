import requests
from bs4 import BeautifulSoup

from src.clients.constants import *
from src.exceptions import LoginException, ServerException


class BaseClient:
    """
    BJUT educational administration clients
    """

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

        request_data = dict(HIDDEN_LOGIN_DEFAULT_PARAMS)
        request_data[HIDDEN_LOGIN_PARAMS.get('username')] = self.ID
        request_data[HIDDEN_LOGIN_PARAMS.get('password')] = self.password

        res = self.session.post(HIDDEN_LOGIN_URL, data=request_data)
        assert res.status_code == 200

        if not _is_login_success(res):
            raise LoginException

        if not self.session.cookies.get("ASP.NET_SessionId"):
            raise ServerException

        self.is_login = True  # awful.. TODO: better way to check the login status