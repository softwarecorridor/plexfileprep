import sqlite3

PATH_TO_DB = ""

def create_tables():
    create_statement = '''CREATE TABLE {table} ({old} text, {new} text)'''
    execute(create_statement)


def add_entry(old_path, new_path):
    insert_statement = '''INSERT INTO {table} VALUES (?, ?)'''
    execute(insert_statement, [old_path, new_path])
    pass


def get_entry_by_newest_path(new_path):
    pass


def clear_db():
    pass

def execute(statement, args = []):
    conn = sqlite3.connect(PATH_TO_DB)

    c = conn.cursor()
    c.execute(statement, args)

    conn.commit()
    conn.close()
