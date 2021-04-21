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
from marshmallow import fields, validate
from {{cookiecutter.app_name}}.models.dict_item import DictItem
from {{cookiecutter.app_name}}.extensions import ma, db


class DictItemSchema(ma.SQLAlchemySchema):
    id = fields.Int(
        required=False,
        allow_none=False,
        # validate=[validate.Length(min=1)],

        error_messages={'required': 'id主键不能为空', 'invalid': '主键不合法'},
        data_key='id')

    dict_code = fields.String(
        required=False,
        allow_none=True,
        # validate=[validate.Length(min=1)],

        error_messages={'required': 'dictCode字典编码不能为空', 'invalid': '字典编码不合法'},
        data_key='dictCode')

    item_code = fields.String(
        required=False,
        allow_none=True,
        # validate=[validate.Length(min=1)],

        error_messages={'required': 'itemCode项编码不能为空', 'invalid': '项编码不合法'},
        data_key='itemCode')

    item_value = fields.String(
        required=False,
        allow_none=True,
        # validate=[validate.Length(min=1)],

        error_messages={'required': 'itemValue项值不能为空', 'invalid': '项值不合法'},
        data_key='itemValue')

    sort_no = fields.Int(
        required=False,
        allow_none=True,
        # validate=[validate.Length(min=1)],

        error_messages={'required': 'sortNo排序不能为空', 'invalid': '排序不合法'},
        data_key='sortNo')

    item_desc = fields.String(
        required=False,
        allow_none=True,
        # validate=[validate.Length(min=1)],

        error_messages={'required': 'itemDesc描述不能为空', 'invalid': '描述不合法'},
        data_key='itemDesc')

    is_valid = fields.String(
        required=False,
        allow_none=True,
        # validate=[validate.Length(min=1)],

        error_messages={'required': 'isValid是否有效 Y启用 N不启用不能为空', 'invalid': '是否有效 Y启用 N不启用不合法'},
        data_key='isValid')

    org_code = fields.String(
        required=False,
        allow_none=False,
        validate=[validate.Length(min=1)],

        error_messages={'required': 'orgCode机构代码不能为空', 'invalid': '机构代码不合法'},
        data_key='orgCode')

    create_by = fields.String(
        required=False,
        allow_none=True,
        # validate=[validate.Length(min=1)],

        error_messages={'required': 'createBy创建人不能为空', 'invalid': '创建人不合法'},
        data_key='createBy')

    create_time = fields.DateTime(
        required=False,
        allow_none=True,
        # validate=[validate.Length(min=1)],
        format='%Y-%m-%d %H:%M:%S',
        error_messages={'required': 'createTime创建时间不能为空', 'invalid': '创建时间不合法'},
        data_key='createTime')

    update_by = fields.String(
        required=False,
        allow_none=True,
        # validate=[validate.Length(min=1)],

        error_messages={'required': 'updateBy更新人不能为空', 'invalid': '更新人不合法'},
        data_key='updateBy')

    update_time = fields.DateTime(
        required=False,
        allow_none=True,
        # validate=[validate.Length(min=1)],
        format='%Y-%m-%d %H:%M:%S',
        error_messages={'required': 'updateTime更新时间不能为空', 'invalid': '更新时间不合法'},
        data_key='updateTime')

    revision = fields.Int(
        required=False,
        allow_none=True,
        # validate=[validate.Length(min=1)],

        error_messages={'required': 'revision版本号不能为空', 'invalid': '版本号不合法'},
        data_key='revision')

    class Meta:
        model = DictItem
        load_instance = True
        sqla_session = db.session