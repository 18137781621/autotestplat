import pymysql
import json
import datetime

host = '127.0.0.1'
port = 3306
db = 'autotest'
user = 'root'
password = '123456'

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)

class OperationMysql:
    def __init__(self):
        # 连接数据库
        self.conn = pymysql.connect(user=user,passwd=password,db=db,port=port,host=host,charset='utf-8')

    # 清除数据库
    def clear(self, table_name):
        # real_sql = "truncate table" + table_name + ";"
        real_sql = "delete from " + table_name + ";"
        with self.conn.cursor() as cursor:
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
            cursor.execute(real_sql)
        self.conn.commit()

    #查询一条数据
    def search_one(self,sql):
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()
            result = json.dumps(result,cls=DateEncoder,ensure_ascii=False)
        return result

    # 查询多条数据
    def search_many(self, sql):
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
        return result

    # 增加一条数据
    def add_one(self,sql):
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
        self.conn.commit()

    #更新数据
    def update_data(self,sql):
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
        self.conn.commit()
    # 关闭数据库连接
    def close(self):
        self.conn.close()



if __name__ == '__main__':
    op_mysql = OperationOracle()

    sql = sql = "select runcard_id from  r_wip_product where wo_id= 'WORKORDER003'"
    print(sql)
    res = op_mysql.search_many(sql)
    print(res)
    op_mysql.close()
