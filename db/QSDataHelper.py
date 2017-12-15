# coding:utf-8

"""
@author: smartgang
@contact: zhangxingang92@qq.com
@file: QSDataHelper.py
@time: 2017/12/8 17:19
"""
from db.SqliteHelper import SqliteHelper
from config import DB_CONFIG_FILE
from config import DB_CONFIG_TABLE


class QSDataHelper(SqliteHelper):
    def __init__(self):
        self.sqlhelper = SqliteHelper(DB_CONFIG_FILE)

    def __del__(self):
        del self

    def create(self):
        create_table_sql = '''CREATE TABLE %s (
                                      `id` int(11) NOT NULL,
                                      `md5` varchar(32) DEFAULT NULL,
                                      `author` varchar(20) DEFAULT NULL,
                                      `content` varchar(500) DEFAULT NULL,
                                      `pic` varchar(200) DEFAULT NULL,
                                       PRIMARY KEY (`id`)
                                    )''' % DB_CONFIG_TABLE
        self.sqlhelper.create(create_table_sql)

    def insert(self, data):
        '''
        insert items
        :param data:data tuple
        :return:
        '''
        save_sql = 'INSERT INTO %s values (?, ?, ?, ?, ?)' % DB_CONFIG_TABLE
        self.sqlhelper.insert(save_sql, data)

    def update(self, rows=None):
        '''
        update items
        :param rows:
        :return:
        '''
        if rows:
            for item in rows:
                update_sql = '''UPDATE %(table)s SET  \
                             md5 = '%(md5)s' ,  \
                             author = '%(author)s' ,  \
                             content = '%(content)s' WHERE  \
                             ID = ?''' % {'table': DB_CONFIG_TABLE,
                                          'md5': item['md5'],
                                          'author': item['author'],
                                          'content': item['content']}
                data = [(item['id'],), ]
                self.sqlhelper.update(update_sql, data)

    def delete(self, conditions=None):
        '''
        delete items all
        :return:
        '''
        if conditions is None:
            update_sql = 'DELETE FROM %s ' % DB_CONFIG_TABLE
            self.sqlhelper.delete(update_sql)
        else:
            for item in conditions:
                update_sql = 'DELETE FROM %s WHERE id = ?' % DB_CONFIG_TABLE
                data = [(item['id'],), ]
                self.sqlhelper.delete(update_sql, data)
    def get_diff_items_num(self):
        '''
        get the different item counts from the database
        :return: num
        '''
        sql = 'SELECT MIN(id), md5, COUNT(md5) FROM {} GROUP by md5 HAVING COUNT(md5) > 1'.format(DB_CONFIG_TABLE)
        return self.sqlhelper.excu_select(sql)

    def get_diff_items(self):
        '''
        get the different items from the database
        :return:
        '''
        sql = 'SELECT id, md5, COUNT(md5) FROM {} GROUP by md5'.format(DB_CONFIG_TABLE)
        return self.sqlhelper.excu_select(sql)

    def delete_repeated_items(self):
        '''
        get the different item counts from the database
        :return: num
        '''
        sql = 'DELETE FROM {} WHERE id in ' \
              '(SELECT id FROM {})' \
              'AND id not in (SELECT min(id) FROM {} GROUP by md5 HAVING COUNT(md5) > 1)'.\
            format(DB_CONFIG_TABLE, DB_CONFIG_TABLE,DB_CONFIG_TABLE)
        return self.sqlhelper.excu(sql)

    def get_max_data_id(self):
        '''
        get the max id from the data
        :return:
        '''
        sql = 'SELECT MAX(id) FROM {}'.format(DB_CONFIG_TABLE)
        return self.sqlhelper.excu_select(sql)

    def fetchonebymd5(self, md5):
        '''
        get the item from the data by md5
        :return:
        '''
        sql = 'SELECT * FROM {} WHERE md5 = ?'.format(DB_CONFIG_TABLE)
        return self.sqlhelper.fetchone(sql, md5)

if __name__ == '__main__':
    qs = QSDataHelper()
    qs.create()
    items = qs.get_diff_items_num()
    for item in items:
        print item
    qs.delete_repeated_items()
    index = qs.get_max_data_id()
    print index
    # qs.delete_repeated_items()
    # data = [(1, u'489efe77fc4ac08e', u'zxg', u'代课教师福克斯的合法开始', ''),
    #         (2, u'489efe77dfdfdfde', u'xgxcg', u'dfdsf的说法看激动', '')]
    # qs.insert(data)
    # data1 = [{}]
    # data1[0]['id'] = int(1)
    # data1[0]['md5'] = u'489efe77fc4ac08e'
    # data1[0]['author'] = u'大理'
    # data1[0]['content'] = u'dfgfdh'
    # qs.update(data1)
    # # qs.delete()
    # data2 = [{}]
    # data2[0]['id'] = int(1)
    # qs.delete(data2)
    # qs.insert(data)

