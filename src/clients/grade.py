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
    DEFAULT_DATA = {
        "Button1": "%B0%B4%D1%A7%C6%DA%B2%E9%D1%AF"
    }
    DATA = {
        "__VIEWSTATE": "",
        "ddlXN": "",
        "ddlXQ": "",
    }
    TERM_GBK = {
        "btn_xq": "%D1%A7%C6%DA%B3%C9%BC%A8"  # 查询学期成绩 gbk 编码
    }
    TOTAL_GBK = {
        "btn_zg": "%BF%CE%B3%CC%D7%EE%B8%DF%B3%C9%BC%A8"  # 查询总成绩 gbk 编码
    }

    def __init__(self, ID, password):
        super(GradeClient, self).__init__(ID, password)
        self.grade_url = self.URL + '?' + self.PARAM + "=" + self.ID
        self.current = datetime.now()

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

    @property
    def view_state(self):
        if not self.is_login:
            self.login()

        res = self.session.post(self.grade_url)
        assert res.status_code == 200
        soup = BeautifulSoup(res.content, 'lxml')
        return str(soup.input.get("value"))

    def get_specified_term_course(self, year=None, term=None):
        """
        获得指定一学期课程数据
        :param year:
        :param term:
        :return:
        """
        if not year:
            year = self.current_year
        if not term:
            term = self.current_term

        view_state = self.view_state  # todo: cache view_state
        if not view_state:
            raise ServerException("Get VIEW_STATE failed.")

        request_data = self.DEFAULT_DATA
        request_data.update(self.DATA)
        request_data.update(self.TERM_GBK)

        # ...... socky todo: refactor
        request_data['__VIEWSTATE'] = view_state
        request_data['ddlXN'] = year
        request_data['ddlXQ'] = term

        res = self.session.post(self.grade_url, data=request_data)
        content = res.content
        return content
