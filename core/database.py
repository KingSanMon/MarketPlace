import sqlite3

class DataBase:
    def __init__(self):

        self.con = sqlite3.connect("database.db")
        self.cur = self.con.cursor()

    def change(self, query, values):
        """Изменение базы данных (Insert, Update, Alert)"""
        self.cur.execute(query, values)
        self.con.commit()

    def get(self, query, values=None, fetchone=True):
        """Получение данных из базы данных"""
        self.cur.execute(query, values)
        if fetchone:
            return self.cur.fetchone()
        else:
            return self.cur.fetchall()
