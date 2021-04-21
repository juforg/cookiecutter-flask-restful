# coding: utf-8
from {{cookiecutter.app_name}}.extensions import db


class DictItem(db.Model):

    __tablename__ = 'ts_dict_item'

    id = db.Column(db.Integer, primary_key=True, info='主键')
    dict_code = db.Column(db.String(30, 'utf8mb4_bin'), info='字典编码')
    item_code = db.Column(db.String(30, 'utf8mb4_bin'), info='项编码')
    item_value = db.Column(db.String(64, 'utf8mb4_bin'), info='项值')
    sort_no = db.Column(db.Integer, info='排序')
    item_desc = db.Column(db.String(128, 'utf8mb4_bin'), info='描述')
    is_valid = db.Column(db.String(1, 'utf8mb4_bin'), server_default=db.FetchedValue(), info='是否有效 Y启用 N不启用')
    org_code = db.Column(db.String(30, 'utf8mb4_bin'), nullable=False, info='机构代码')
    create_by = db.Column(db.String(30, 'utf8mb4_bin'), info='创建人')
    create_time = db.Column(db.DateTime, server_default=db.FetchedValue(), info='创建时间')
    update_by = db.Column(db.String(30, 'utf8mb4_bin'), info='更新人')
    update_time = db.Column(db.DateTime, server_default=db.FetchedValue(), info='更新时间')
    revision = db.Column(db.Integer, server_default=db.FetchedValue(), info='版本号')

    __table_args__ = (
        db.UniqueConstraint('dict_code', 'item_code', name='dict_item_code_uk'),
    )

    def __init__(self, **kwargs):
        super(DictItem, self).__init__(**kwargs)

    def __repr__(self):
        return "<DictItem %s>" % self.item_name