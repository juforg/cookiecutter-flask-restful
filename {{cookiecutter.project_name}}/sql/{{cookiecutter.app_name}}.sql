create database {{cookiecutter.app_name}} default charset utf8mb4 collate utf8mb4_bin;
CREATE USER '{{cookiecutter.app_name}}'@'%' IDENTIFIED BY 'hmjNMC5ap49c';
grant all privileges  on {{cookiecutter.app_name}}.* to '{{cookiecutter.app_name}}'@'localhost' IDENTIFIED BY 'hmjNMC5ap49c';
flush privileges;
use {{cookiecutter.app_name}};
CREATE TABLE user(
    id INT NOT NULL AUTO_INCREMENT  COMMENT '主键' ,
    emp_code VARCHAR(10) NOT NULL   COMMENT '工号' ,
    emp_name VARCHAR(32)    COMMENT '员工姓名' ,
    emp_status TINYINT    COMMENT '状态' ,
    username VARCHAR(80)  COMMENT '用户名' ,
    email VARCHAR(80) COMMENT '邮箱' ,
    password VARCHAR(255)  COMMENT '密码' ,
    roles VARCHAR(32)    COMMENT '角色' ,
    active TINYINT    COMMENT '是否激活' ,
    avatar VARCHAR(128)    COMMENT '头像' ,
    PRIMARY KEY (emp_code)
) COMMENT = '用户表';
DROP TABLE token_blacklist;;/*SkipError*/
CREATE TABLE token_blacklist(
    id INT NOT NULL AUTO_INCREMENT  COMMENT '主键' ,
    jti VARCHAR(64) NOT NULL   COMMENT 'jti' ,
    token_type VARCHAR(32) NOT NULL   COMMENT '类型' ,
    user_id VARCHAR(32) NOT NULL   COMMENT '用户id' ,
    revoked TINYINT NOT NULL   COMMENT '是否' ,
    expires DATETIME NOT NULL   COMMENT '过期时间' ,
    PRIMARY KEY (id)
) COMMENT = '黑名单 ';;
CREATE TABLE dict(
    id INT NOT NULL AUTO_INCREMENT  COMMENT '主键' ,
    dict_name VARCHAR(32)    COMMENT '字典名称' ,
    dict_code VARCHAR(32)    COMMENT '字典编码' ,
    description VARCHAR(128)    COMMENT '描述' ,
    is_valid TINYINT   DEFAULT 1 COMMENT '是否有效 1启用 0不启用' ,
    created_time DATETIME   DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间' ,
    updated_by VARCHAR(32)    COMMENT '更新人' ,
    updated_time DATETIME   DEFAULT CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP COMMENT '更新时间' ,
    PRIMARY KEY (id)
) COMMENT = '字典表';
ALTER TABLE dict ADD UNIQUE dict_code_uk(dict_code);

CREATE TABLE dict_item(
    id INT NOT NULL AUTO_INCREMENT  COMMENT '主键' ,
    dict_code VARCHAR(32)    COMMENT '字典编码' ,
    item_code VARCHAR(32)    COMMENT '项编码' ,
    item_name VARCHAR(32)    COMMENT '项名称' ,
    sort_order INT    COMMENT '排序' ,
    description VARCHAR(128)    COMMENT '描述' ,
    is_valid TINYINT   DEFAULT 1 COMMENT '是否有效 1启用 0不启用' ,
    created_time DATETIME   DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间' ,
    updated_by VARCHAR(32)    COMMENT '更新人' ,
    updated_time DATETIME   DEFAULT CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP  COMMENT '更新时间' ,
    PRIMARY KEY (id)
) COMMENT = '字典明细';
ALTER TABLE dict_item ADD UNIQUE dict_item_code_uk(item_code,dict_code);