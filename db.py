import sqlite3
import os

PATH_TO_DB = "test.db"
FILENAME_TABLE = "paths"
OLD_COL = "old_path"
NEW_COL = "new_path"


def create_tables():
    create_statement = '''CREATE TABLE IF NOT EXISTS {table} ({old} text, {new} text)'''.format(table=FILENAME_TABLE,old = OLD_COL, new=NEW_COL)
    execute(create_statement)


def add_entry(old_path, new_path):
    insert_statement = '''INSERT INTO {table} VALUES (?, ?)'''.format(table=FILENAME_TABLE)
    execute(insert_statement, [old_path, new_path])


def get_entry_by_newest_path(new_path):
    conn = sqlite3.connect(PATH_TO_DB)
    c = conn.cursor()

    query_statement = 'SELECT {old} FROM {table} WHERE {new}=?'.format(old=OLD_COL,table=FILENAME_TABLE,new=NEW_COL)
    c.execute(query_statement, [new_path])

    query_result = c.fetchone()

    conn.close()


    if query_result:
       return query_result[0]

    return None

def clear_db():
    os.remove(PATH_TO_DB)
    create_tables()

def execute(statement, args = []):
    conn = sqlite3.connect(PATH_TO_DB)

    c = conn.cursor()
    c.execute(statement, args)

    conn.commit()
    conn.close()
