from peewee import PostgresqlDatabase, SqliteDatabase

from configurations.envs import DEV_ENV


if DEV_ENV:
    db = SqliteDatabase("db.sqlite3")
else:
    db = PostgresqlDatabase("")
