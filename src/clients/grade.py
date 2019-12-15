from datetime import datetime

from bs4 import BeautifulSoup

from src.clients.base import BaseClient
from src.exceptions import ServerException


class GradeClient(BaseClient):
    """
    BJUT educational administration query grades client
    """
    URL = "http://gdjwgl.bjut.edu.cn/xscj_gc.aspx"
    PARAM = "xh"

    def __init__(self, ID, password):
        super(GradeClient, self).__init__(ID, password)
        self.grade_url = self.URL + '?' + self.PARAM + "=" + self.ID
        self.current = datetime.now()
        self.view_state = None

    @property
    def current_year(self):
        if self.current.month >= 9:
            return str(self.current.year) + "-" + str(self.current.year + 1)
        else:
            return str(self.current.year - 1) + "-" + str(self.current_year)

    @property
    def current_term(self):
        """
        todo: what is the term logic?
        :return:
        """
        if self.current.month >= 9:
            return 2
        else:
            return 1

    def _update_view_state(self):
        res = self.session.post(self.grade_url)
        assert res.status_code == 200
        soup = BeautifulSoup(res.content, 'lxml')
        self.__view_state = str(soup.input.get("value"))

    @property
    def view_state(self):
        """
        The view_state attribute
        :param value:
        :return:
        """
        if not self.is_login:  # update the view state if not login
            self.login()
            self._update_view_state()

        return self.__view_state

    @view_state.setter
    def view_state(self, value=None):
        """
        Set view_state attribute
        * Also, for the latter validation
        :param value: useless
        :return:
        """
        if not self.is_login:
            self.login()

        self._update_view_state()  # Set the view state

    def get_specified_term_course(self, year=None, term=None):
        """
        Get the per course grades with the specified term
        :param year:
        :param term:
        :return:
        """
        request_data = {
            "__VIEWSTATE": "",
            "ddlXN": "",
            "ddlXQ": "",
            "Button1": "%B0%B4%D1%A7%C6%DA%B2%E9%D1%AF"
        }

        if not year:
            year = self.current_year
        if not term:
            term = self.current_term

        view_state = self.view_state  # todo: cache view_state
        if not view_state:
            raise ServerException("Get VIEW_STATE failed.")

        # ...... todo: refactor
        request_data['__VIEWSTATE'] = view_state
        request_data['ddlXN'] = year
        request_data['ddlXQ'] = term

        res = self.session.post(self.grade_url, data=request_data)
        content = res.content
        return content

    def get_all_course(self):
        """
        Get the per course grades of all of the courses
        Use a tricky method
        :return:
        """

        year = 'hack'  # invalid year is ok to get the all of the score data
        return self.get_specified_term_course(year)