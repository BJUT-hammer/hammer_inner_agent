import os
import sys
import argparse

from fabric import Connection, Config
from patchwork import files


# hosts
TARGET_ENVS = {
    'dev': [
        {
            'host': '49.233.80.33',
            'password': '1qaz@WSX'
        },
    ],
    'preview': [
        {
            'host': '',
            'password': 'Cdn123456'
        }
    ],
}

USER = "ubuntu"
# app
APP_NAME = "hammer_agent"
VENV_NAME = 'isms'
# local
WORKSPACE = "/Users/xiaoxi/Codes/%s/" % APP_NAME
# remote
EXPORT_DIR = "/tmp/"
HOME_DIR = "/home/%s/grey" % USER
VENV_BIN = "/home/%s/.pyenv/versions/%s/bin/" % (USER, VENV_NAME)

EXPORT_PATH = os.path.join(EXPORT_DIR, APP_NAME)
DEPLOY_PATH = os.path.join(HOME_DIR, APP_NAME)
PACKAGE_FILE = "%s.tar.gz" % APP_NAME



def package_project(conn):
    print("=" * 30)
    print("本地打包源码文件")
    _tmp_path = "/tmp/%s" % APP_NAME

    with conn.cd(WORKSPACE):
        if not os.path.isdir(_tmp_path):
            os.mkdir(_tmp_path)
        _tar_cmd = "tar zc --exclude '.gitignore' --exclude '.git' -f %s/%s /users/xiaoxi/codes/hammer_agent/" % (_tmp_path, PACKAGE_FILE)
        conn.local(_tar_cmd)


def make_remote_env(conn):
    print("=" * 30)
    if not files.exists(conn, EXPORT_DIR):
        conn.sudo(user=USER, command="mkdir %s" % EXPORT_DIR)


def rsync_package_to_remote(conn):
    print("=" * 30)
    print("把本地打包好的源码文件同步到远端服务器")
    _tmp_console_path = "/tmp/%s" % APP_NAME
    _remote_dir = EXPORT_DIR
    # api.sudo(user='%USER', command="chown -R %s:%s %s" % (api.env.user, api.env.user, _remote_dir))
    _local_file = os.path.join(_tmp_console_path, PACKAGE_FILE)
    result = conn.put(_local_file, _remote_dir)  # 覆盖
    print("Uploaded {0.local} to {0.remote}".format(result))


def export_package(conn):
    print("=" * 30)
    print("解压源码包")
    _package_path = os.path.join(EXPORT_DIR, PACKAGE_FILE)
    if not files.exists(conn, _package_path):
        print("The package %s do not exists" % _package_path)
        sys.exit(-1)
    print("Now clear the export path %s" % EXPORT_PATH)
    conn.sudo(user=USER, command="rm -rf %s" % EXPORT_PATH)
    conn.sudo(user=USER, command="mkdir %s" % EXPORT_PATH)
    print("Now export package %s to %s" % (PACKAGE_FILE, EXPORT_PATH))
    _cmd = "tar -xzf %s -C %s" % (_package_path, EXPORT_PATH)
    conn.sudo(user=USER, command=_cmd)
    print("Done")


def sync_project_files(conn):
    print("=" * 30)
    print("同步源码到部署目录")
    conn.sudo(user=USER, command="/usr/bin/rsync -aczr %s/* %s" % (EXPORT_PATH, DEPLOY_PATH))
    print('Done')


def install_requirements(conn):
    """
    安装依赖包
    :return:
    """
    # print("=" * 30)
    # print("install requirements")
    # conn.sudo(user='%USER', command=VENV_BIN+"pip install -r %s/requirements.txt" % DEPLOY_PATH)
    print('Done')


def restart_project_service(conn):
    """
    """
    print("=" * 30)
    print("重启服务")
    # restart_cmd = 'supervisorctl -c '+ DEPLOY_PATH + '/etc/supervisord.conf restart all'
    # status_cmd = 'supervisorctl -c '+ DEPLOY_PATH + '/etc/supervisord.conf status all'
    # conn.sudo(user='%USER', command=VENV_BIN + restart_cmd)
    # conn.sudo(user='%USER', command=VENV_BIN + status_cmd)

    print('Done')


def deploy():
    parser = argparse.ArgumentParser()
    parser.add_argument("env", choices = ['dev', 'preview'],
            help="specify the deploy env")
    args = parser.parse_args()
    env = args.env
    target_envs = TARGET_ENVS[env]

    for env in target_envs:
        c = Connection(host=env['host'], user=USER, connect_kwargs={'password': env['password']})
        c.warn = True
        package_project(c)
        make_remote_env(c)
        rsync_package_to_remote(c)
        export_package(c)
        sync_project_files(c)
        install_requirements(c)
        restart_project_service(c)


if __name__ == "__main__":
    deploy()

