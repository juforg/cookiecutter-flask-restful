#!/bin/bash
echo "本脚本专门用于部署{{cookiecutter.app_name}}-server-01服务器"
echo "是否重新build基础镜像？ "
OPTIONS="是 否"
select opt in $OPTIONS;do
if [ "$opt" = "是" ];then
  echo "将会构建基础镜像，请耐心等待。"
  break
elif [ "$opt" = "否" ];then
  break
else
  echo "无此选项，请重选"
fi
done
echo $opt
if [ "$opt" = "是" ];then
  cd ./{{cookiecutter.app_name}}_base_image
  docker build -t {{cookiecutter.app_name}}-base .
fi
cd /home/{{cookiecutter.app_name}}/docker/
ENV_FILE_NAME=flask{{cookiecutter.app_name}}proenv docker-compose build --build-arg USER_ID=$(id -u) {{cookiecutter.app_name}}-be
ENV_FILE_NAME=flask{{cookiecutter.app_name}}proenv docker-compose build --build-arg USER_ID=$(id -u) {{cookiecutter.app_name}}-fe
USER_ID=$(id -u) ENV_FILE_NAME=flask{{cookiecutter.app_name}}proenv  docker-compose up -d

docker rm $(docker ps -a|grep Exited| awk '{print $1}')
docker rmi $(docker images | grep 'none' | awk '{print $3}')
docker exec -uroot {{cookiecutter.app_name}}-be  chown -R app:app /opt/{{cookiecutter.app_name}}