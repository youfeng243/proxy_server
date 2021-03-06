#!/usr/bin/env bash

HOST_NAME="127.0.0.1"
PORT="3306"
USERNAME="root"
PASSWORD="000000"

DBNAME="proxy_server_db"
create_db_sql="create database IF NOT EXISTS ${DBNAME} default character set utf8 collate utf8_unicode_ci"

mysql -h${HOST_NAME}  -P${PORT}  -u${USERNAME} -p${PASSWORD} -e "${create_db_sql}"

yum install -y python-devel
yum install -y mysql-devel
pip install virtualenv

virtualenv .venv -p python2
.venv/bin/pip install -U pip
.venv/bin/pip install -r requirements.txt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

# 创建表
.venv/bin/python manage.py syncdb
echo "环境初始化完成..."