# coding:utf-8

"""
@author: smartgang
@contact: zhangxingang92@qq.com
@file: SqliteHelper.py
@time: 2017/12/8 16:58
"""
# coding:utf-8
"""
@author: smartgang
@contact: zhangxingang92@qq.com
@file: SqliteHelper.py
@time: 2017/12/7 18:19
"""
import sqlite3

class SqliteHelper:
    def __init__(self, dataFile):
        try:
            self.conn = sqlite3.connect(dataFile)
        except sqlite3.Error as e:
            print "connect the database failed:", e.args[0]

    def getcursor(self):
        return self.conn.cursor()

    def drop(self, table):
        '''
        if the table exist,please be carefull
        '''
        if table is not None and table != '':
            cu = self.getcursor()
            sql = 'DROP TABLE IF EXISTS ' + table
            try:
                cu.execute(sql)
            except sqlite3.Error as why:
                print "delete table failed:", why.args[0]
                return
            self.conn.commit()
            print "delete table successful!"
            cu.close()
        else:
            print "table does not exist！"

    def create(self, sql):
        '''
        create database table
        :param sql:
        :return:
        '''
        if sql is not None and sql != '':
            cu = self.getcursor()
            try:
                cu.execute(sql)
            except sqlite3.Error as why:
                print "create table failed:", why.args[0]
                return
            self.conn.commit()
            print "create table successful!"
            cu.close()
        else:
            print "sql is empty or None"

    def insert(self, sql, data):
        '''
        insert data to the table
        :param sql:
        :param data:
        :return:
        '''
        if sql is not None and sql != '':
            if data is not None:
                cu = self.getcursor()
                try:
                    for d in data:
                        cu.execute(sql, d)
                        self.conn.commit()
                except sqlite3.Error as why:
                    print "insert data failed:", why.args[0]
                cu.close()
        else:
            print "sql is empty or None"

    def fetchall(self, sql):
        '''
        query all data
        :param sql:
        :return:
        '''
        if sql is not None and sql != '':
            cu = self.getcursor()
            try:
                cu.execute(sql)
                content = cu.fetchall()
                if len(content) > 0:
                    for item in content:
                        for element in item:
                            print element,
                        print ''
                else:
                    for element in content:
                        print element,
                    print ''
            except sqlite3.Error as why:
                print "fetchall data failed:", why.args[0]
            cu.close()
        else:
            print "sql is empty or None"

    def fetchone(self, sql, data):
        '''
        query one data
        :param sql:
        :param data:
        :return:
        '''
        if sql is not None and sql != '':
            if data is not None:
                cu = self.getcursor()
                try:
                    d = (data,)
                    cu.execute(sql, d)
                    content = cu.fetchone()
                    return content
                except sqlite3.Error as why:
                    print "fetch the data failed:", why.args[0]
                cu.close()
        else:
            print "sql is empty or None"

    def update(self, sql, data):
        '''
        update the data
        :param sql:
        :param data:
        :return:
        '''
        if sql is not None and sql != '':
            if data is not None:
                cu = self.getcursor()
                try:
                    for d in data:
                        cu.execute(sql, d)
                        self.conn.commit()
                except sqlite3.Error as why:
                    print "update data failed:", why.args[0]
                cu.close()
        else:
            print "sql is empty or None"

    def delete(self, sql, data=None):
        '''
        delete the data
        :param sql:
        :param data:
        :return:
        '''
        if sql is not None and sql != '':
            cu = self.getcursor()
            if data is not None:
                try:
                    for d in data:
                        cu.execute(sql, d)
                        self.conn.commit()
                except sqlite3.Error as why:
                    print "delete data failed:", why.args[0]
            else:
                try:
                    cu.execute(sql)
                    self.conn.commit()
                except sqlite3.Error as why:
                    print "delete data failed:", why.args[0]
            cu.close()
        else:
            print "sql is empty or None"

    def excu_select(self, sql):
        '''
        execute the sql statement
        :param sql:
        :return:
        '''
        try:
            cu = self.getcursor()
            cu.execute(sql)
            content = cu.fetchall()
            cu.close()
            return content
        except sqlite3.Error as why:
            print "excute the sql %s failed!" % sql
            print why.args[0]
    def excu(self, sql):
        '''
        execute the sql statement
        :param sql:
        :return:
        '''
        try:
            cu = self.getcursor()
            cu.execute(sql)
            self.conn.commit()
            cu.close()
        except sqlite3.Error as why:
            print "excute the sql %s failed!" % sql
            print why.args[0]

    def __del__(self):
        self.conn.close()


# test
if __name__ == '__main__':
    TABLE_NAME = 'student'

    sqlhelper = SqliteHelper('test.db')


    def drop_table_test():
        '''删除数据库表测试'''
        print('删除数据库表测试...')
        sqlhelper = SqliteHelper('test.db')
        sqlhelper.drop(TABLE_NAME)


    def create_table_test():
        '''创建数据库表测试'''
        print('创建数据库表测试...')
        # 创建表（id,name,gender,age,address,phone)
        create_table_sql = '''CREATE TABLE `student` (
                              `id` int(11) NOT NULL,
                              `name` varchar(20) NOT NULL,
                              `gender` varchar(4) DEFAULT NULL,
                              `age` int(11) DEFAULT NULL,
                              `address` varchar(200) DEFAULT NULL,
                              `phone` varchar(20) DEFAULT NULL,
                               PRIMARY KEY (`id`)
                            )'''
        sqlhelper = SqliteHelper('test.db')
        sqlhelper.create(create_table_sql)


    def save_test():
        '''保存数据测试...'''
        print('保存数据测试...')
        save_sql = 'INSERT INTO student values (?, ?, ?, ?, ?, ?)'
        data = [(1, 'Zhang', u'男', 15, u'北京', '12345678910'),
                (2, 'Li', u'男', 50, u'吉林省长春市', '1567891****'),
                (3, 'Zhao', u'女', 40, u'黑龙江', '18*********'),
                (4, 'Xi', u'女', 30, u'上海', '1**********'),
                (5, 'Liao', u'男', 15, u'湖南', '12345678910'),
                (6, 'Ling', u'男', 50, u'大理', '1567891****'),
                (7, 'JJJ', u'女', 40, u'***', '18*********'),
                (8, 'LLL', u'女', 30, u'Hongkong', '1**********')]

        sqlhelper.insert(save_sql, data)


    def fetchall_test():
        '''查询所有数据...'''
        print('查询所有数据...')
        fetchall_sql = '''SELECT * FROM student'''
        sqlhelper.fetchall(fetchall_sql)


    def fetchone_test():
        '''查询所有数据...'''
        print('查询一条数据...')
        fetchall_sql = '''SELECT * FROM student WHERE ID = ? '''
        data = 1
        sqlhelper.fetchone(fetchall_sql, data)
        update_sql = '''UPDATE student SET name = ? WHERE ID = ? '''
        data = [(1, 'James'),
                (2, 'Kobe')]
        sqlhelper.update(update_sql, data)


    def update_test():
        '''更新数据'''
        print('更新一条数据...')
        update_sql = '''UPDATE student SET name = ? WHERE ID = ? '''
        data = [('James', 1),
                ('Kobe', 2)]
        sqlhelper.update(update_sql, data)


    def delete_test():
        '''删除数据'''
        print('删除一条数据...')
        update_sql = '''DELETE FROM student WHERE ID = ? AND NAME = ?'''
        data = [(1, 'James')]
        sqlhelper.delete(update_sql, data)


    drop_table_test()
    create_table_test()
    save_test()
    update_test()
    delete_test()
