from datetime import datetime

from {{cookiecutter.app_name}}.extensions import db


class Dict(db.Model):
    """字典表 model
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='主键')
    dict_name = db.Column(db.String(32), comment='字典名称')
    dict_code = db.Column(db.String(32), comment='字典编码')
    description = db.Column(db.String(128), comment='描述')
    is_valid = db.Column(db.SMALLINT, comment='是否有效;1启用 0不启用')
    created_time = db.Column(db.DateTime, comment='创建时间', default=datetime.now())
    updated_by = db.Column(db.String(32), comment='更新人')
    updated_time = db.Column(db.DateTime, comment='更新时间')

    __table_args__ = (
        db.UniqueConstraint('dict_code', name='dict_code_uk'),
    )

    def __init__(self, **kwargs):
        super(Dict, self).__init__(**kwargs)

    def __repr__(self):
        return "<Dict %s>" % self.username


class DictItem(db.Model):
    """字典明细 model
    """
    id = db.Column(db.Integer, autoincrement=True, comment='主键')
    dict_code = db.Column(db.String(32), primary_key=True, comment='字典编码')
    item_code = db.Column(db.String(32), primary_key=True, comment='项编码')
    item_name = db.Column(db.String(32), comment='项名称')
    sort_order = db.Column(db.SMALLINT, comment='排序')
    description = db.Column(db.String(128), comment='描述')
    is_valid = db.Column(db.SMALLINT, comment='是否有效;1启用 0不启用')
    updated_by = db.Column(db.String(32), comment='更新人')

    __table_args__ = (
        db.UniqueConstraint('dict_code', 'item_code', name='dict_item_code_uk'),
    )

    def __init__(self, **kwargs):
        super(DictItem, self).__init__(**kwargs)

    def __repr__(self):
        return "<DictItem %s>" % self.item_name
