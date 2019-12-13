from bs4 import BeautifulSoup

from src.constants import GBK
from src.exceptions import ServerException


class BaseFactory:
    def __init__(self, res):
        self.raw = res
        res = self.iconv(res)
        self.soup = BeautifulSoup(res, 'html.parser')

    @property
    def code(self):
        soup = BeautifulSoup(self.raw, 'html.parser')
        code = soup.html.get('lang')
        if not code:
            # todo: logger record
            code = GBK
        return code

    def iconv(self, res):
        """
        将该网页编码转为 UTF-8 编码
        :param res:
        :return:
        """
        try:
            res = res.decode(self.code, "ignore").encode('utf-8')
        except Exception:
            raise ServerException("Decode error.")
        return res