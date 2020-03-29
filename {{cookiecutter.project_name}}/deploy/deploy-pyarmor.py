# -*- coding: utf-8 -*-

#  -*- coding: utf-8 -*-
#
#   Copyright (c) ©2019, Cardinal Operations and/or its affiliates. All rights reserved.
#   CARDINAL OPERATIONS PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.
#

# !/usr/bin/env python
import datetime
import logging

import paramiko
from retry import retry
import pysftp
import sys
import os
from pick import pick

logger = logging.getLogger(__name__)


class Config:
    env_file_name: str

    def __init__(self, env_file_name):
        self.env_file_name = env_file_name


ss_{{cookiecutter.app_name}}_test_config_dict1 = {
    'server_ip': '127.0.0.1',
    'server_name': '{{cookiecutter.app_name}}test',
    'username': 'admin',
    'base_path': '/home/sysop/docker/{{cookiecutter.app_name}}/',
    'env_file_name': 'flask{{cookiecutter.app_name}}testenv',
    'config_base_path': 'ss-{{cookiecutter.app_name}}-test-01'
}

ss_{{cookiecutter.app_name}}_pro_config_dict1 = {
    'server_ip': '127.0.0.1',
    'server_name': 'admin',
    'username': '{{cookiecutter.app_name}}ai',
    'base_path': '/home/{{cookiecutter.app_name}}ai/docker/',
    'env_file_name': 'flask{{cookiecutter.app_name}}proenv',
    'config_base_path': '{{cookiecutter.project_name}}-server-01'
}

server_config = ss_{{cookiecutter.app_name}}_test_config_dict1


def sftp_transfer_callback(x, y):
    total_count = 100
    cur_count = int(x / y * total_count)
    show_count = int(cur_count / 2)
    leftover_count = int(total_count / 2 - show_count)
    # print(str_arrs[cur_count % 3] + '{}/40:'.format(cur_count) + '#' * cur_count + '\r')
    sys.stdout.write('\r{}/{}:'.format(cur_count, total_count) + '#' * show_count + '-' * leftover_count)
    sys.stdout.flush()


@retry(tries=4, delay=5)
def sftp_upload_file(server_ip, local_path, server_path, is_dir=False):
    with pysftp.Connection(host=server_ip, username=username,
                           private_key=os.path.expanduser('~/.ssh/id_rsa')) as sftp:
        print("Connection succesfully stablished ... ")
        print(local_path)
        print(server_path)
        if is_dir:
            sftp.makedirs(server_path)
        else:
            parent_path = os.path.dirname(server_path)
            sftp.makedirs(parent_path)
        if is_dir:
            sftp.put_r(localpath=local_path, remotepath=server_path)
        else:
            sftp.put(localpath=local_path, remotepath=server_path,
                     callback=sftp_transfer_callback)


def output(file):
    try:
        while True:
            text_line = file.readline()
            if text_line:
                print(text_line, end='')
            else:
                break
    finally:
        file.close()


def get_config_full_base_path(config_base_path):
    return os.path.join(os.getcwd(), config_base_path)


def get_base_image_full_path():
    return os.path.join(os.getcwd(), '{{cookiecutter.project_name}}_base_image')


def get_nginx_config_full_base_path(config_base_path):
    return os.path.join(os.getcwd(), get_config_full_base_path(config_base_path), 'nginx')


def get_docker_compose_yml_path(config_base_path):
    return get_config_full_base_path(config_base_path) + '/docker-compose.yml'


def get_env_file_full_path(config_base_path, env_file_name):
    return get_config_full_base_path(config_base_path) + '/' + env_file_name


def get_docker_entry_point_full_path(config_base_path, entry_point_file_name):
    return get_config_full_base_path(config_base_path) + '/' + entry_point_file_name


config_list = list()


def build_and_package():
    pyarmor_cmd = 'pyarmor obfuscate --exclude ' \
                  + algo_exclude_path + ' --recursive --output ' + algo_bin_path + ' ' \
                  + algo_src_path + '/__init__.py --platform linux64'
    print(pyarmor_cmd)
    os.system(pyarmor_cmd)
    ## 3 编译前端
    fe_npm_cmd = 'cd ' + fe_src_path
    fe_npm_cmd +=';npm run build:stage' if fe_build_test else ';npm run build:prod'
    fe_npm_cmd +='; gitbook build src/docs dist/docs'
    print(fe_npm_cmd)
    os.system(fe_npm_cmd)
    fe_mv_cmd = 'mv ' + fe_src_path + '/dist/* ' + fe_bin_path
    print(fe_mv_cmd)
    os.system(fe_mv_cmd)
    fe_tar_cmd = 'cd ' + fe_bin_path + '; tar -zcvf ../../{{cookiecutter.app_name}}-fe.tar.gz static index.html favicon.ico docs'
    print(fe_tar_cmd)
    os.system(fe_tar_cmd)
    # 4 打包后端
    dirs = ['{{cookiecutter.app_name}}']
    files = [
        'setup.py',
        'logging.yml',
        'requirements.txt',
    ]
    all_files = []
    all_files.extend(dirs)
    all_files.extend(files)
    print(all_files)
    for dir in dirs:
        os.system('cp -r ' + os.path.join(be_server_src_path, dir) + ' ' + bin_path)
    for f in files:
        os.system('cp ' + os.path.join(be_server_src_path, f) + ' ' + bin_path)
    print(bin_path)
    all_files.append('model')
    # all_files.append('fe')
    tar_filenames = ' '.join(all_files)
    tar_cmd = 'cd ' + bin_path + '; tar -zcvf ../{{cookiecutter.app_name}}.tar.gz ' + tar_filenames
    print(tar_cmd)
    os.system(tar_cmd)


def upload():
    sftp_upload_file(server_ip, get_docker_compose_yml_path(config_base_path), remote_path + 'docker-compose.yml')
    sftp_upload_file(server_ip, get_nginx_config_full_base_path(config_base_path), remote_path + 'nginx', True)
    sftp_upload_file(server_ip, os.path.join(project_dir, 'deploy/Dockerfile'), remote_path + 'Dockerfile')
    sftp_upload_file(server_ip, get_env_file_full_path(config_base_path, env_file_name), remote_path + env_file_name)
    sftp_upload_file(server_ip, get_base_image_full_path(), remote_path + '{{cookiecutter.project_name}}_base_image', True)
    sftp_upload_file(server_ip, be_zip_file_path, remote_path + '{{cookiecutter.app_name}}.tar.gz')
    sftp_upload_file(server_ip, fe_zip_file_path, remote_path + 'nginx/{{cookiecutter.app_name}}-fe.tar.gz')


def remote_build():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server_ip, 22, username, key_filename=os.path.expanduser('~') + '/.ssh/id_rsa')
    if rebuild_base_image:
        stdin, stdout, stderr = ssh.exec_command('cd ' + base_path + '/{{cookiecutter.project_name}}_base_image; docker build -t {{cookiecutter.app_name}}-base .')
        output(stdout)
        output(stderr)
    docker_command = 'cd ' + base_path + '; \
                            ' + 'ENV_FILE_NAME=' + env_file_name + ' ' + '/usr/bin/docker-compose build --build-arg USER_ID=$(id -u) {{cookiecutter.app_name}}-be; \
                            ' + 'ENV_FILE_NAME=' + env_file_name + ' ' + '/usr/bin/docker-compose build --build-arg USER_ID=$(id -u) {{cookiecutter.app_name}}-fe; \
                            ' + 'USER_ID=$(id -u) ENV_FILE_NAME=' + env_file_name + ' ' + '/usr/bin/docker-compose up -d ;'
    print(docker_command)
    stdin, stdout, stderr = ssh.exec_command(docker_command)

    output(stdout)
    output(stderr)
    ssh.exec_command('docker rm $(docker ps -a|grep Exited| awk \'{print $1}\')')
    stdin, stdout, stderr = ssh.exec_command("docker rmi $(docker images | grep 'none' | awk '{print $3}');")
    output(stdout)
    output(stderr)
    stdin, stdout, stderr = ssh.exec_command(
        "docker exec -uroot {{cookiecutter.app_name}}-be  chown -R app:app /opt/{{cookiecutter.app_name}};")
    output(stdout)
    output(stderr)
    stdin, stdout, stderr = ssh.exec_command(
        "docker exec -uroot {{cookiecutter.app_name}}-timing  chown -R app:app /opt/{{cookiecutter.app_name}};")
    output(stdout)
    output(stderr)
    pass


def clean_all():
    os.system('rm -rf ' + dist_path + '/*')


def clean_other():
    os.system('rm -rf ' + bin_path + '/*')
    os.system('rm -f ' + be_zip_file_path)
    print(be_zip_file_path)
    os.system('rm -f ' + fe_zip_file_path)
    print(fe_zip_file_path)
    os.system('rm -rf ' + {{cookiecutter.app_name}}_package_dic_path)
    print({{cookiecutter.app_name}}_package_dic_path)


def package_script():
    os.system('mkdir -p ' + os.path.join({{cookiecutter.app_name}}_package_dic_path, 'nginx'))
    os.system('mkdir -p ' + os.path.join({{cookiecutter.app_name}}_package_dic_path, 'sql'))
    cp_cmd = 'cp -R ' + be_zip_file_path + ' ' + {{cookiecutter.app_name}}_package_dic_path
    os.system(cp_cmd)
    cp_cmd = 'cp -R ' + fe_zip_file_path + ' ' + os.path.join({{cookiecutter.app_name}}_package_dic_path, 'nginx')
    os.system(cp_cmd)
    cp_cmd = 'cp -R ' + get_docker_compose_yml_path(config_base_path) + ' ' + {{cookiecutter.app_name}}_package_dic_path
    os.system(cp_cmd)
    cp_cmd = 'cp -R ' + get_nginx_config_full_base_path(config_base_path) + ' ' + {{cookiecutter.app_name}}_package_dic_path
    os.system(cp_cmd)
    cp_cmd = 'cp -R ' + os.path.join(project_dir, 'deploy/Dockerfile') + ' ' + {{cookiecutter.app_name}}_package_dic_path
    os.system(cp_cmd)
    cp_cmd = 'cp -R ' + get_env_file_full_path(config_base_path, env_file_name) + ' ' + {{cookiecutter.app_name}}_package_dic_path
    os.system(cp_cmd)
    cp_cmd = 'cp -R ' + get_env_file_full_path(config_base_path, 'deploy.sh') + ' ' + {{cookiecutter.app_name}}_package_dic_path
    os.system(cp_cmd)
    cp_cmd = 'cp -R ' + get_base_image_full_path() + ' ' + os.path.join({{cookiecutter.app_name}}_package_dic_path, '{{cookiecutter.project_name}}_base_image')
    os.system(cp_cmd)
    cp_cmd = 'cp -R ' + os.path.join(project_dir, 'sql/{{cookiecutter.app_name}}.sql') + ' ' + os.path.join({{cookiecutter.app_name}}_package_dic_path, 'sql')
    os.system(cp_cmd)
    cp_cmd = 'cp -R ' + os.path.join(project_dir, 'sql/init-data.sql') + ' ' + os.path.join({{cookiecutter.app_name}}_package_dic_path, 'sql')
    os.system(cp_cmd)
    tar_cmd = 'cd ' + dist_path + '; tar -zcvf ' + server_config['server_name'] + '-package' + date_str + '.tar.gz ' + server_config['server_name'] + '/*'
    print(tar_cmd)
    os.system(tar_cmd)
    # os.system('mkdir -p ' + bin_path)


if __name__ == '__main__':
    try:
        title1 = '请选择环境:'
        option1 = ['ss-{{cookiecutter.app_name}}-test-01(127.0.0.1)', 'ss-{{cookiecutter.app_name}}-pro-01(127.0.0.1)']
        selected1, idx1 = pick(option1, title1, multi_select=False, min_selection_count=1)
        title2 = '请选择是否重新构建基础镜像:'
        option2 = ['否', '是']
        selected2, idx2 = pick(option2, title2, multi_select=False, min_selection_count=1)
        title3 = '请选择前端打包环境:'
        option3 = ['测试', '生产']
        selected3, idx3 = pick(option3, title3, multi_select=False, min_selection_count=1)
        fe_build_test = False
        rebuild_base_image = False
        # rebuild_fe_image = True
        if idx2 == 1:
            rebuild_base_image = True
        server_config = None
        if idx1 == 0:
            server_config = ss_{{cookiecutter.app_name}}_test_config_dict1
        elif idx1 == 1:
            server_config = ss_{{cookiecutter.app_name}}_pro_config_dict1
        if server_config is None:
            raise Exception('select index error')
        print(os.getcwd())
        if idx3 == 0:
            fe_build_test = True

        server_ip = server_config['server_ip']
        username = server_config['username']
        base_path = server_config['base_path']
        env_file_name = server_config['env_file_name']
        config_base_path = server_config['config_base_path']
        print('config_full_base_path==>' + get_config_full_base_path(config_base_path))
        print('nginx_config_full_base_path==>' + get_nginx_config_full_base_path(config_base_path))
        algo_src_path = os.path.abspath(os.path.join(os.getcwd(), "../../", '{{cookiecutter.app_name}}_algo/model'))
        be_server_src_path = os.path.abspath(os.path.join(os.getcwd(), '../'))
        fe_src_path = os.path.abspath(os.path.join(os.getcwd(), "../../../", '{{cookiecutter.app_name}}-fe'))
        algo_exclude_path = os.path.abspath(os.path.join(algo_src_path, 'demo'))
        dist_path = os.path.join(os.getcwd(), 'dist')
        clean_all()
        bin_path = os.path.join(dist_path, '{{cookiecutter.app_name}}')
        os.system('mkdir -p ' + bin_path)
        algo_bin_path = os.path.join(bin_path, 'model')
        be_server_bin_path = os.path.join(bin_path, 'be-server')
        fe_bin_path = os.path.join(bin_path, 'fe')
        os.system('mkdir -p ' + fe_bin_path)
        project_dir = os.path.abspath(os.path.join(os.getcwd(), "../"))
        be_zip_file_path = dist_path + '/{{cookiecutter.app_name}}.tar.gz'
        fe_zip_file_path = dist_path + '/{{cookiecutter.app_name}}-fe.tar.gz'
        {{cookiecutter.app_name}}_package_dic_path = os.path.join(dist_path, server_config['server_name'])
        date_str = datetime.datetime.now().strftime('%Y%m%d')
        {{cookiecutter.app_name}}_zip_file_path = dist_path + server_config['server_name'] + '-package' + date_str + '.tar.gz '
        local_path = be_zip_file_path
        remote_path = base_path
        print(be_zip_file_path)
        build_and_package()
        if idx1 == 0:
            upload()
            remote_build()
            clean_all()
        else:
            package_script()
            clean_other()

    except BaseException as e:
        logger.exception(e)
    except IOError as e:
        logger.exception(e)
