# -*- coding: utf-8 -*-

from enum import Enum, unique

"""状态码枚举类
usage：
    结构为：错误枚举名-错误码code-错误说明message
    # 打印状态码信息
    code = Status.OK.get_code()
    print("code:", code)
    # 打印状态码说明信息
    msg = Status.OK.get_msg()
    print("msg:", msg)
"""


class C:
    code: str
    message: str

    def __init__(self, code, message):
        self.code = code
        self.message = message

    def dict(self):
        return {"code": self.code, "message": self.message}


class ReturnCode:
    """
    2开头 请求成功，3开头权限问题 4开头参数问题 5开头系统bug 6开头业务异常
    """
    OK = C(200000, "成功").dict()
    SUCCESS = C(200001, "成功").dict()
    LOGIN_EXPIRED = C(300001, "登录过期").dict()
    INVALID_TOKEN = C(300002, "令牌无效").dict()
    INVALID_SIGNATURE = C(300003, "签名无效").dict()
    PARAM_IS_NULL = C(400001, "请求参数为空").dict()
    JSON_PARSE_FAIL = C(4000002, "JSON转换失败").dict()
    PARAM_ILLEGAL = C(4000003, "请求参数非法").dict()
    PAGE_NOT_FOUND = C(4000004, "页面不存在").dict()
    METHOD_NOT_ALLOWED = C(4000005, "方法不允许").dict()
    REPEATED_COMMIT = C(4000006, "重复提交").dict()
    USER_NOT_FOUND = C(4000007, "用户不存在").dict()
    NAME_PWD_INVALID = C(4000008, "用户名或密码错误").dict()
    SQL_ERROR = C(5000006, "数据库异常").dict()
    NETWORK_ERROR = C(5000015, "网络异常").dict()
    UNKNOWN_ERROR = C(5000099, "未知异常").dict()
    NOT_FOUND = C(6000007, "无记录").dict()
    ALREADY_EXIST = C(6000008, "已存在").dict()

    def code(self):
        """
        根据枚举名称取状态码code
        :return: 状态码code
        """
        return list(self.value.keys())[0]

    def msg(self):
        """
        根据枚举名称取状态说明message
        :return: 状态说明message
        """
        return list(self.value.values())[0]
