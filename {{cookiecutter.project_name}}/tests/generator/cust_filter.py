# -*- coding: utf-8 -*-
# @author: songjie
# @email: songjie@shanshu.ai
# @date: 2020/08/25
#      SJ编程规范
# 命名：
#    1. 见名思意，变量的名字必须准确反映它的含义和内容
#    2. 遵循当前语言的变量命名规则
#    3. 不要对不同使用目的的变量使用同一个变量名
#    4. 同个项目不要使用不同名称表述同个东西
#    5. 函数/方法 使用动词+名词组合，其它使用名词组合
# 设计原则：
#    1. KISS原则： Keep it simple and stupid !
#    2. SOLID原则： S: 单一职责 O: 开闭原则 L: 迪米特法则 I: 接口隔离原则 D: 依赖倒置原则
#
from faker import Faker


def factoryboy_gen(text):
    fake = Faker(locale='zh_CN')
    if text in ["BIGINT", "INT", "INTEGER"]:
        return fake.pyint(min_value=0, max_value=9999, step=1)
    elif text in ["SMALLINT"]:
        return fake.pyint(min_value=0, max_value=9999, step=1)
    elif text in ["DECIMAL"]:
        return fake.pydecimal(left_digits=None, right_digits=None, positive=False, min_value=None, max_value=None)
    elif text in ["Float"]:
        fake.pyfloat(left_digits=None, right_digits=None, positive=False, min_value=None, max_value=None)        # Python浮点数
    elif text in ["TIMESTAMP", "DATETIME"]:
        return fake.date(pattern="%Y-%m-%d %H:%M:%S", end_datetime=None)
    elif text in ["DATE"]:
        return fake.date(pattern="%Y-%m-%d", end_datetime=None)
    elif text in ["TIME"]:
        return fake.date(pattern="%H:%M:%S", end_datetime=None)
    elif text in ["TEXT", "VARCHAR", "NVARCHAR", "NCHAR", "CHAR"]:
        return fake.pystr(min_chars=None, max_chars=20)
