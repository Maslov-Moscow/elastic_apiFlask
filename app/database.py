import sqlite3
from datetime import datetime


class SQLdatabase:
    def __init__(self):
        self.connection = sqlite3.connect("db.db")
        self.cursor = self.connection.cursor()

    def get_data(self):
        with self.connection:
            return self.cursor.execute("SELECT id,text FROM posts").fetchall()

    def get_records(self, id_list: tuple) -> list:
        with self.connection:
            sql = f"SELECT * from posts WHERE id IN ({','.join(['?'] * len(id_list))})"
            list_rec = self.cursor.execute(sql, id_list).fetchall()
            return sorted(list_rec, key=lambda x: datetime.strptime(x[1], '%Y-%m-%d %H:%M:%S'), reverse=True)

    def delete_record(self, id_rec: int) -> None:
        with self.connection:
            sql = f"DELETE FROM posts WHERE id = {id_rec}"
            self.cursor.execute(sql)

# (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,

# db = SQLdatabase()
# db.cursor.execute('''CREATE TABLE IF NOT EXISTS posts
#                      (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,
#                      text TEXT,
#                      created_date TEXT,
#                      rubrics TEXT)''')
# res = db.cursor.execute("SELECT id, text FROM posts ").fetchall()
# print(res[1])
