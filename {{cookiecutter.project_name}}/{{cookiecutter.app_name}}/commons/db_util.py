# -*- coding: utf-8 -*-
import time

from pandas import DataFrame
import numpy
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker, scoped_session

from {{cookiecutter.app_name}}.extensions import db
from contextlib import contextmanager
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class DbUtil:
    session = None

    def get_session(self, bind='{{cookiecutter.app_name}}', autocommit=True):
        """
        使用了scoped_session 默认情况下，创建的session都是Thread-Local Scope
        :param bind:
        :return:
        """
        engine = db.get_engine(app=db.get_app(), bind=bind)
        session_factory = sessionmaker(bind=engine, autocommit=autocommit)
        _session = scoped_session(session_factory)
        self.session = _session()
        return self.session

    @contextmanager
    def auto_commit(self, bind='{{cookiecutter.app_name}}'):

        try:
            self.session = self.get_session(bind=bind)
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()

    """
       用于执行一次查询的数据库查询操作封装
    """

    def update(self, sql='', params={}):
        session = self.session
        if sql:
            stmt = text(sql)
            if params:
                session.execute(stmt, params)
            else:
                session.execute(stmt)
        else:
            print("SQL为空!")

    def select(self, sql='', params={}):
        res_list = []
        session = self.session
        if sql:
            stmt = text(sql)
            if params:
                for record in session.execute(stmt, params):
                    # print(type(record))
                    row_dict = dict((zip(record.keys(), record)))
                    res_list.append(row_dict)
                print(res_list)
                return res_list
            else:
                for record in session.execute(stmt):
                    # print(type(record))
                    row_dict = dict((zip(record.keys(), record)))
                    res_list.append(row_dict)
                print(res_list)
                return res_list
        else:
            print("SQL为空!")

    def __del__(self):
        if self.session:
            self.session.close()

def full_insert(session, schema_type, data_dict_list, model_type, request_id: str, is_src: bool, **kwargs):
    start = time.time()
    query = session.query(model_type).filter_by(**kwargs)
    if hasattr(model_type, "request_id"):
        query = query.filter_by(request_id == request_id)
    count = query.delete()
    logger.info("数据[%s]全量删除,request_id:[%s],kwargs:[%s]完成, 删除:%s,[performance-DD]耗时:[%s]", model_type.__tablename__, request_id, kwargs.__str__(), count, time.time() - start)
    return batch_insert(session, schema_type, data_dict_list, model_type, request_id, is_src)


def batch_insert(session, schema_type, data_dict_list, model_type, request_id: str, is_src: bool):
    """
    全量更新
    :param session:
    :param schema_type: marshmallow 类型不需要带db
    :param data_dict_list: 字典list
    :param model_type: 数据库模型类
    :param request_id:
    :param is_src: 是否需要用重新映射
    :param kwargs: 删除数据时的参数信息， 如material接口传入customer_id=*** 其他接口传输 warehouse_id=***
    :return:
    """
    start = time.time()
    step = 1000
    ni = 0
    while data_dict_list:
        tmp_data = data_dict_list[ni * step:(ni + 1) * step]
        if not tmp_data:
            break
        if is_src:
            schema = schema_type(many=True, unknown=True)
            tmp_data = schema.load(tmp_data)
        session.bulk_insert_mappings(model_type, tmp_data)
        ni += 1

    logger.info("数据全量保存:,request_id:[%s],数据量:[%s],[performance-SD]耗时:[%s]", request_id, len(data_dict_list), time.time() - start)
    return len(data_dict_list)


def increment_update(session, schema_type, data_dict_list, is_src: bool, request_id: str, **kwargs):
    """
    :param session: 数据库连接对象
    :param schema_type:  marshmallow 类型需要带db
    :param data_dict_list: 字典
    :param is_src: 是否需要重新加载并映射
    :param request_id: 请求ID
    :param kwargs:
    :return:
    """
    start = time.time()
    schema = schema_type(many=True, unknown=True)
    step = 200
    ni = 0
    while data_dict_list:
        tmp_data = data_dict_list[ni * step:(ni + 1) * step]
        if not tmp_data: break
        start2 = time.time()
        if is_src:
            main_data = schema.load(tmp_data)
        else:
            dumped_json = schema.dump(tmp_data)
            main_data = schema.load(dumped_json)
        logger.debug("[performance-serialize]数据量:[%s],耗时:[%s]", len(tmp_data), time.time() - start2)
        start3 = time.time()
        session.bulk_save_objects(main_data)
        logger.debug("增量更新:[performance-SAVE]耗时:[%s]", time.time() - start3)
        ni += 1

    logger.info("数据[%s]增量更新:,request_id:[%s],kwargs:[%s],数据量:[%s],[performance-UD]耗时:[%s]", schema_type.__name__, request_id, kwargs.__str__(), len(data_dict_list),
                time.time() - start)
    return len(data_dict_list)


def process_df_to_db(data_df: DataFrame, keys: list = None):
    """
    处理df的一些字段类型，使能够用sqlalchemy 保存数据库
    :param keys: 指定哪些列需要处理
    :param data_df:
    :return:
    """
    records = data_df.to_dict(orient='records')
    for record in records:
        for key in keys if keys else record.keys():
            if isinstance(record[key], pd.Timestamp):
                record[key] = record[key].to_pydatetime()
            elif pd.isnull(record[key]):
                record[key] = None
            elif isinstance(record[key], numpy.float64):
                record[key] = record[key].astype(float)
    return records


type_dict = {
    "BIGINT": "Int",
    "BIGINTEGER": "Int",
    "INT": "Int",
    "INTEGER": "Int",
    "SMALLINT": "Int",
    "TINYINT": "Int",
    "DECIMAL": "Float",
    "FLOAT": "Float",
    "TIMESTAMP": "DateTime",
    "DATETIME": "DateTime",
    "DATE": "Date",
    "TIME": "Time",
    "TEXT": "String",
    "STRING": "String",
    "VARCHAR": "String",
    "NVARCHAR": "String",
    "NCHAR": "String",
    "CHAR": "String",
    "BIT": "Boolean",
    "BOOLEAN": "Boolean",
}


def dbtype_transfer(obj:str):
    return type_dict.get(obj.upper())
