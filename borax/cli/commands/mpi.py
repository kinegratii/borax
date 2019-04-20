# coding=utf8
"""
borax-cli mpi
"""
import os
import platform
import configparser

import click

BUILTIN_URLS = {
    "pypi": "https://pypi.python.org/simple",
    "tuna": "https://pypi.tuna.tsinghua.edu.cn/simple",
    "douban": "https://pypi.doubanio.com/simple",
    "aliyun": "https://mirrors.aliyun.com/pypi/simple",
    "ustc": "https://mirrors.ustc.edu.cn/pypi/web/simple"
}

SECTION_KEY = 'global'
VALUE_KEY = 'index-url'


def get_user_config_path():
    if 'Windows' in platform.system():
        config_path = r'~\pip\pip.ini'
    else:
        config_path = r'~/.pip/pip.conf'
    return os.path.expanduser(config_path)


def read_url(path):
    cp = configparser.ConfigParser()
    try:
        cp.read(path)
        return cp.get(SECTION_KEY, VALUE_KEY)
    except configparser.Error:
        return None


def write_url(path, url):
    cp = configparser.ConfigParser()
    cp.read(path)
    if not cp.has_section(SECTION_KEY):
        cp.add_section(SECTION_KEY)
    cp.set(SECTION_KEY, VALUE_KEY, url)
    with open(path, 'w+') as f:
        cp.write(f)


@click.command()
@click.option('--name', help='The builtin name of PyPI url.')
@click.option('--url', help='The url of PyPI')
@click.option('--path', help='The pip config path.')
def cli(name, url, path):
    if not path:
        path = get_user_config_path()
    click.secho('[Info] PIP config file: {}\n'.format(path))
    if name is None and url is None:
        current = read_url(path)
        url_list = []
        for name, url in BUILTIN_URLS.items():
            url_list.append(
                ' {0:<3}{1:<10}{2}'.format(
                    '*' if url == current else ' ',  # [' ', '*'][url==current]
                    name,
                    url
                )
            )
        click.echo('\n'.join(url_list))
        return
    if name:
        target = BUILTIN_URLS.get(name, None)
        if target:
            write_url(path, target)
            click.secho('[Success] ', nl=False, fg='green')
            click.echo('The PyPI index-url has set to {}'.format(target))
        else:
            click.secho('[Error] ', nl=False, fg='red')
            click.echo('Invalid name for PyPI.Choices are: {}'.format(' '.join(BUILTIN_URLS.keys())))
    else:
        if url:
            write_url(path, url)
            click.secho('[Success] ', nl=False, fg='green')
            click.echo('The PyPI index-url has set to {}'.format(url))
        else:
            click.secho('[Error] ', nl=False, fg='red')
            click.echo('Invalid url for PyPI.')
