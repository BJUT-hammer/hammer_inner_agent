HIDDEN_LOGIN_URL = "http://gdjwgl.bjut.edu.cn/default_vsso.aspx"
HIDDEN_LOGIN_PARAMS = {
    "username": "TextBox1",
    "password": "TextBox2",
}
HIDDEN_LOGIN_DEFAULT_PARAMS = {  # 直接拼接到请求参数里
    "RadioButtonList1_2": "%D1%A7%C9%FA",  # 学生 gbk 编码
    "Button1": ""
}
SESSION_COOKIE_PARAM = "ASP.NET_SessionId"

QUERY_SCORE_URL = "http://gdjwgl.bjut.edu.cn/xscj_gc.aspx"
QUERY_SCORE_URL_PARAM = "xh"
QUERY_SCORE_DEFAULT_PARAMS = {
    "__EVENTTARGET": "",
    "__EVENTARGUMENT": "",
    "hidLanguage": "",
    "ddl_kcxz": "",
    "btn_xq": "%D1%A7%C6%DA%B3%C9%BC%A8"
}
QUERY_SCORE_PARAMS = {
    "view_state": "__VIEWSTATE",
    "school_year": "ddlXN",
    "term": "ddlXQ",
}
QUERY_SCORE_TERM_PARAM = {
    "btn_xq": "%D1%A7%C6%DA%B3%C9%BC%A8"  # 查询学期成绩 gbk 编码
}
QUERY_SCORE_TOTAL_PARAM = {
    "btn_zg": "%BF%CE%B3%CC%D7%EE%B8%DF%B3%C9%BC%A8"  # 查询总成绩 gbk 编码
}