from mysql.connector import connect, Error


class MysqlDB:
    def __init__(self, dbname, user, password, host):
        self.__conn = connect(
            database=dbname,
            user=user,
            password=password,
            host=host
        )
        self.__cur = self.__conn.cursor()

    def export_from_postgresql(self, columns, data):
        try:
            # create table from postgresql
            sql = """CREATE TABLE IF NOT EXISTS car_shop ("""
            for i in columns:
                column_type = i[1].replace("integer", "INT").replace("character varying", "VARCHAR(255)")
                sql += f"{i[0]} {column_type}, "
            sql = sql[:-2] + ")"
            self.__cur.execute(sql)

            # insert exporting data
            self.__cur.executemany(
                "INSERT INTO car_shop (id, provider, customer, booking) VALUES (%s, %s, %s, %s)",
                data)

            self.__conn.commit()
        except Error as e:
            print(e)
            exit()

    def fetch(self):
        try:
            self.__cur.execute("SELECT * FROM car_shop")
            return self.__cur.fetchall()
        except Error as e:
            print(e)
            exit()

    def update(self, record_id: int, value: list):
        value.append(record_id)
        try:
            self.__cur.execute("UPDATE car_shop SET provider=%s, customer=%s, booking=%s WHERE id=%s", value)
            self.__conn.commit()
        except Error as e:
            print(e)
            exit()

