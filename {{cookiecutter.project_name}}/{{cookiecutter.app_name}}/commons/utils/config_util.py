# -*- coding: utf-8 -*-
# @author: songjie
# @email: songjie@shanshu.ai
# @date: 2020/08/27
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
from configparser import ConfigParser


def ini2dict(config: ConfigParser):
    options = []
    for sec in config.sections():
        sec_dict = {'section_name': sec}
        for item in config.items(sec):
            sec_dict[item[0]] = item[1]
        options.append(sec_dict)
    return options


