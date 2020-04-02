#!/usr/bin/env python
# encoding: utf-8
import datetime

# 获取时间戳
def get_time_stamp():
    return int(datetime.datetime.now().timestamp()*1000)

# 获取时间
def get_time():
    return datetime.datetime.utcnow() + datetime.timedelta(hours=8)


# 根据时间戳返回datetime对象
def get_datetime(time_stamp):
    """
    根据时间戳返回datetime对象
    :param time_stamp: 时间戳
    :return: datetime
    """
    return datetime.datetime.utcfromtimestamp(time_stamp)


def get_values_by_keys(dict_data, keys_defaults):
    """

    :param dict_data: 字典数据
    :param keys_defaults: 列表形式可以指定多个key值，可以使用（key,default）的形式指定默认值
    :return: list
    """
    res = []
    for key_default in keys_defaults:
        if type(key_default) == str:
            res.append(dict_data.get(key_default))
        else:
            key, default = key_default
            data = dict_data.get(key)
            if data is None:
                res.append(default)
            else:
                res.append(data)
    return res



