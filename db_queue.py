import project_settings
from pymongo import *
from abc_base.db_base import DbBase
import re


class MongoDbQueue(DbBase):
    db = None
    tbl_name = ''

    def __init__(self, home_page, tbl_name='pages'):

        if tbl_name == '':
            raise ValueError('Table name should not be empty')

        regx_tbl_name = re.compile(r'^[a-zA-Z0-9_]+$')
        if not regx_tbl_name.match(tbl_name):
            raise ValueError('Table name provided is not valid, please check it out')

        MongoDbQueue.tbl_name = tbl_name

        MongoDbQueue.db = MongoClient(project_settings.DB_CONNECTION_STRING)[project_settings.DB_REPOSITORY_NAME]

        if project_settings.DB_DROP_TABLES_WHEN_RESTART:
            MongoDbQueue.db[MongoDbQueue.tbl_name].drop()

        # add home page to make crawler start
        MongoDbQueue.save_pending_queue([home_page])

        # create unique index
        MongoDbQueue.db[MongoDbQueue.tbl_name].create_index('url', unique=True)

    @staticmethod
    def get_pending_queue():
        return [r['url'] for r in MongoDbQueue.db[MongoDbQueue.tbl_name].find({'is_crawled': False}, {'url': 1})]

    @staticmethod
    def is_page_in_queue(url):
        return MongoDbQueue.db[MongoDbQueue.tbl_name].find_one({'url': url}) is not None

    @staticmethod
    def save_pending_queue(urls):
        for url in urls:
            if not MongoDbQueue.db[MongoDbQueue.tbl_name].find_one({'url': url}):
                MongoDbQueue.db[MongoDbQueue.tbl_name].insert({'url': url, 'is_crawled': False})

    @staticmethod
    def set_page_crawled(url):
        if MongoDbQueue.db[MongoDbQueue.tbl_name].find_one({'url': url, 'is_crawled': False}) is not None:
            MongoDbQueue.db[MongoDbQueue.tbl_name].update({'url': url}, {'$set': {'is_crawled': True}})
