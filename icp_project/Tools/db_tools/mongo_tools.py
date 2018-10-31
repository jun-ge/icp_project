#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import time
import logging
from pymongo import MongoClient, errors


class MongoConnection(object):
    def __init__(self):
        self.logger = logging.getLogger('MongoConnection')

    def mongo_conn(self, **kwargs):
        while True:
            try:
                if kwargs.get('url', None):
                    return MongoClient(kwargs.get('url'))[kwargs.get('db')]
                else:
                    return MongoClient('mongodb://localhost:27017/')['test']
            except errors.PyMongoError as e:
                self.logger.error("mongodb_conn链接失败,reconnect,error_msg:{}".format(e))
                time.sleep(3)
                continue


class MongoClientTools(object):
    def __init__(self, **kwargs):
        self.logger = logging.getLogger('MongoClientTools')
        self.__conn = MongoConnection().mongo_conn(**kwargs)

    def save(self, dict_data, table_name, find=None, many=None):
        if find:
            if getattr(self.__conn, table_name).find(find).count():
                if many:
                    getattr(self.__conn, table_name).update_many(find, {'$set': dict_data})
                else:
                    getattr(self.__conn, table_name).update(find, {'$set': dict_data})
            else:
                self.logger.debug('匹配字段:{}无法查询到 % find')
        else:
            getattr(self.__conn, table_name).insert(dict_data)


