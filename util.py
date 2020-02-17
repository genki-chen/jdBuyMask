# -*- coding=utf-8 -*-
import hashlib
import json
import re
import socket
import requests

_dnscache = {}

def parse_json(s):
    begin = s.find('{')
    end = s.rfind('}') + 1
    return json.loads(s[begin:end])


def getconfigMd5():
    with open('configDemo.ini', 'r', encoding='utf-8') as f:
        configText = f.read()
        return hashlib.md5(configText.encode('utf-8')).hexdigest()

def response_status(resp):
    if resp.status_code != requests.codes.OK:
        print('Status: %u, Url: %s' % (resp.status_code, resp.url))
        return False
    return True


def _setDNSCache():
    """
    Makes a cached version of socket._getaddrinfo to avoid subsequent DNS requests.
    """

    def _getaddrinfo(*args, **kwargs):
        global _dnscache
        if args in _dnscache:
            # print(str(args) + " in cache")
            return _dnscache[args]

        else:
            # print(str(args) + " not in cache")
            _dnscache[args] = socket._getaddrinfo(*args, **kwargs)
            return _dnscache[args]

    if not hasattr(socket, '_getaddrinfo'):
        socket._getaddrinfo = socket.getaddrinfo
        socket.getaddrinfo = _getaddrinfo


def split_area_id(area):
    """将地区id字符串按照下划线进行切割，构成数组。数组长度不满4位则用'0'进行填充。
    :param area: 地区id字符串（使用 _ 或 - 进行分割），如 12_904_3375 或 12-904-3375
    :return: list
    """
    area_id_list = list(map(lambda x: x.strip(), re.split('_|-', area)))
    area_id_list.extend((4 - len(area_id_list)) * ['0'])
    return area_id_list
