from psycopg2 import connect, Error, sql


class PostgresDB:
    def __init__(self, dbname, user, password, host):

        self.__conn = connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host)
        self.__cursor = self.__conn.cursor()

    def export_from_sqlite(self, data, columns: list, fields_to_export):
        # create table with columns from sqlite table
        try:
            fields = []
            for col in columns[:fields_to_export]:
                # change sqlite columns type to postgresql
                col_type = col[1].replace("TEXT", "varchar").replace("INTEGER", "integer")

                fields.append(sql.SQL("{} {}").format(sql.Identifier(col[0]), sql.SQL(col_type)))

            # create requests query
            query = sql.SQL("CREATE TABLE IF NOT EXISTS {table_name} ( {fields} );").format(
                table_name=sql.Identifier("car_shop"),
                fields=sql.SQL(', ').join(fields)
            )
            self.__cursor.execute(query)
            self.__conn.commit()
        except Error as e:
            print(e)

        # Insert data from sqlite table
        for i in data:
            values = i[:fields_to_export]
            try:
                self.__cursor.execute(
                    """ INSERT INTO car_shop (id, provider, customer, booking) VALUES (%s, %s, %s, %s)""", values)
                self.__conn.commit()
            except Error as e:
                print(e)
                exit()

    def update(self, record_id: int, value: list):
        value.append(record_id)
        try:
            self.__cursor.execute("UPDATE car_shop SET provider=%s, customer=%s, booking=%s WHERE id=%s", value)
            self.__conn.commit()
        except Error as e:
            print(e)
            exit()


    def fetch(self):
        try:
            self.__cursor.execute(""" SELECT * FROM car_shop """)
            return self.__cursor.fetchall()
        except Error as e:
            print(e)
            exit()

    def get_columns_type(self):
        # get list od columns and their types
        self.__cursor.execute(""" SELECT column_name, data_type FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = 'car_shop'""")
        return self.__cursor.fetchall()
