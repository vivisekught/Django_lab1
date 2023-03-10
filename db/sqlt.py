import sqlite3


class SqliteDB:
    def __init__(self, db_path):
        self.__con = sqlite3.connect(db_path)
        self.__cursor = self.__con.cursor()

    def create(self):
        try:
            self.__cursor.execute("""CREATE TABLE IF NOT EXISTS car_shop 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,  
                            provider TEXT, 
                            customer TEXT,
                            booking TEXT,
                            terms TEXT,
                            article INTEGER,
                            amount INTEGER)
                        """)
        except sqlite3.Error as e:
            print(e)

    def insert(self, data):
        self.__cursor.executemany(
            """INSERT INTO car_shop
            (provider, customer, booking, terms, article, amount) 
            VALUES (?, ?, ?, ?, ?, ?)""",
            data)
        self.__con.commit()

    def update(self, record_id, value):
        value.append(record_id)
        self.__cursor.execute(
            "UPDATE car_shop SET provider=?, customer=?, booking=?, terms=?, article=?, amount=? WHERE id=?", value)
        self.__con.commit()


    def get_columns_types(self):
        return self.__cursor.execute("""SELECT name, type FROM pragma_table_info('car_shop') """).fetchall()

    def get_table_data(self):
        return self.__cursor.execute("SELECT * FROM car_shop").fetchall()



