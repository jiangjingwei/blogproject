#! coding:utf-8

from fabric.api import env, run
from fabric.operations import sudo

# 设置git地址
GIT_REPO = 'https://github.com/jiangjingwei/blogproject.git'

# 服务器用户名
env.user = 'jiangjingwei'

# 服务器密码
env.password = 'Jiang1992911'

# 服务器主机
env.hosts = ['139.196.81.14']

# 服务器端口
env.port = '22'


def deploy():

    # 项目目录
    source_folder = '/home/jiangjingwei/site/www.jjwxy.com/blogproject'

    run('cd %s && git pull' % source_folder)

    run("""
        cd {} &&
        ../env/bin/pip install -r requirements.txt &&
        ../env/bin/python3 manage.py collectstatic --noinput &&
        ../env/bin/python3 manage.py migrate
        ../env/bin/gunicorn blogproject.wsgi:application -b 127.0.0.1:8080 --daemon --reload
    """.format(source_folder))

    sudo('service nginx reload')
