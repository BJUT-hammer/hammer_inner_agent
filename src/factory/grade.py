from copy import copy

from bs4.element import NavigableString

from src.factory.base import BaseFactory


class GradeFactory(BaseFactory):
    """
    Build:
    * a total course grade list
    * a specified course grade list
    """
    COURSE_GRADE_TABLE_INDEX = 0   # the first table is the course grade table
    COURSE_GRADE_SCHEMA = {
        '学年': '',
        '学期': '',
        '课程代码': '',
        '课程名称': '',
        '课程性质': '',
        '课程归属': '',
        '学分': '',
        '绩点': '',
        '成绩': '',
        '辅修标记': '',
        '补考成绩': '',
        '重修成绩': '',
        '学院名称': '',
        '备注': '',
        '重修标记': '',
        '课程英文名称': '',
    }
    COURSE_GRADE_INDEX = {key: 0 for key in COURSE_GRADE_SCHEMA}  # record the index from gdjw
    @property
    def course_grade_table(self):
        tables = self.soup.find_all('table')
        return tables[self.COURSE_GRADE_TABLE_INDEX]

    def _parse_item(self, data):
        """
        Parse a row of table
        :param data:
        :return:
        """
        print(data)
        res = []
        for info in data:
            if not info:
                res.append("")
            elif isinstance(info, NavigableString):
                continue
            else:
                contents = info.contents
                if not contents:
                    res.append("")
                else:
                    res.append(contents[0])
        return res

    def parse_table_head(self, course):
        """
        Parse table head
        """
        head_list = self._parse_item(course)
        print("head_list", head_list)
        for index, info in enumerate(head_list):
            if info in self.COURSE_GRADE_SCHEMA:
                self.COURSE_GRADE_INDEX[info] = int(index)
            else:
                pass
                # todo: logger
                # print(info)

    def parse_table_data(self, course):
        """
        Parse table data
        :return:
        """
        print('map:', self.COURSE_GRADE_INDEX)
        data_list = self._parse_item(course)
        print('data_list', data_list)
        res = copy(self.COURSE_GRADE_SCHEMA)
        for key, index in self.COURSE_GRADE_INDEX.items():
            res[key] = data_list[index]
        return res

    def parse_one_course(self, course):
        classes = course.attrs.get('class')
        if classes and ('datelisthead' in classes):
            self.parse_table_head(course)
            return
        else:
            return self.parse_table_data(course)

    def parse_course(self):
        course_grade_list = []
        for course in self.course_grade_table:
            if isinstance(course, NavigableString):  # skip the pure string element, maybe it is '\n', ...
                continue
            res = self.parse_one_course(course)
            if res:
                course_grade_list.append(res)
        return course_grade_list