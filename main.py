from db.sqlt import SqliteDB
from db.postgreSQL import PostgresDB
from db.mySQL import MysqlDB
from utils.constants import *


def main():
    # work with sqlite
    sqlite = SqliteDB(PATH_TO_SQLITE_DB)
    sqlite.create()
    sqlite.insert(DATA)

    # update with test parameter
    sqlite.update(1, ["Lexus", "Lexus Service Center", "Lexus", "19.03.2021", 1111, 1])
    # receive data and columns type for export to postgres
    sqlt_data = sqlite.get_table_data()
    sqlt_columns = sqlite.get_columns_types()
    # number of first fields to export
    fields_to_export = 4

    # work with postgres
    postgres = PostgresDB(POSTGRES_DB_NAME, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST)
    postgres.export_from_sqlite(sqlt_data, sqlt_columns, fields_to_export)
    # update with test parameter

    postgres.update(1, ["R", "R", "R"])
    # receive data and columns type for export to mysql
    postgres_data = postgres.fetch()
    postgres_columns_type = postgres.get_columns_type()

    # work with mysql
    mysql = MysqlDB(MYSQL_DB_NAME, MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST)
    mysql.export_from_postgresql(postgres_columns_type, postgres_data)
    # update with test parameter
    mysql.update(1, ["L", "L", "L"])
    print(mysql.fetch())



if __name__ == "__main__":
    main()
