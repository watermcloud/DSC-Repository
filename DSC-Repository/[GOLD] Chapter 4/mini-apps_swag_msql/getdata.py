from konek import mysql
class getDatas(object):
    def __init__(self):
        self.cursor = mysql.connect().cursor()

    def getAllData(self):
        self.cursor.execute("SELECT * FROM customers")
        aData = self.cursor.fetchall()
        return aData