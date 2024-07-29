import pymysql


class Read:
    def __init__(self):
        self.db = pymysql.connect(host="bigdata1", port=3306, user="root", password="123456", db="xiecheng_db")
        self.cursor = self.db.cursor()

    def source_mysql(self, sql):
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def __del__(self):
        self.cursor.close()
        self.db.close()