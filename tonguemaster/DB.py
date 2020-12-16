import sqlite3
from datetime import date
from sqlite3 import Error
from enum import IntEnum


class Verbosity(IntEnum):
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    DEBUG = 4


class MyDB:
    def __init__(self, db_file, table=None):
        self.conn = None
        self.verbose = Verbosity.NONE
        self.__create_db(db_file)
        self.cursor = self.conn.cursor()
        if table is not None:
            self.create_table(table)

    def close(self):
        self.conn.close()

    def __create_db(self, db_file):
        try:
            self.conn = sqlite3.connect(db_file)
            if self.verbose >= Verbosity.DEBUG:
                print(sqlite3.version)
        except Error as e:
            print(e)
            raise

    def create_table(self, table_name):
        sql_create_projects_table = f""" CREATE TABLE IF NOT EXISTS {table_name} (
                                            src_language text,
                                            dst_language text,
                                            EZ_factor real DEFAULT 2.5,
                                            next_date text,
                                            priority integer DEFAULT 2,
                                            interval integer DEFAULT 0,
                                            repetitions integer DEFAULT 1,
                                            mp3_file_name text,
                                            valid integer DEFAULT 1
                                        ); """
        try:
            self.cursor.execute(sql_create_projects_table)
            if self.verbose >= Verbosity.HIGH:
                print(f'table \'{table_name}\' was created')
        except Error as e:
            print(e)
            raise

    def insert_entry(self, table, entry):
        sql_insert = f""" INSERT OR REPLACE INTO {table}
                            VALUES (?,?,?,?);"""
        self.cursor.execute(sql_insert, entry)
        self.conn.commit()
        if self.verbose >= Verbosity.HIGH:
            print(f'entry added/replaced: {entry}')
        return self.cursor.lastrowid

    def insert_word(self, table, entry):
        sql_insert = f""" INSERT OR REPLACE INTO {table} (src_language, dst_language)
                            VALUES (?,?);"""
        self.cursor.execute(sql_insert, entry)
        self.conn.commit()
        if self.verbose >= Verbosity.LOW:
            print(f'entry added/replaced: {entry}')
        return self.cursor.lastrowid

    def get_entries(self, table):
        sql_select = f""" SELECT * FROM {table};"""
        self.cursor.execute(sql_select)
        # self.conn.commit()
        rows = self.cursor.fetchall()
        if self.verbose >= Verbosity.LOW:
            print(f'the rows of table {table} are:')
            for row in rows:
                print(row)
        return rows

    def word_exists(self, table, field, params):
        sql_select = f""" SELECT COUNT({field}) FROM {table} WHERE {field}=?;"""
        if self.verbose >= Verbosity.DEBUG:
            print(sql_select)
        self.cursor.execute(sql_select, params)
        # self.conn.commit()
        exists = self.cursor.fetchone()[0]
        if exists == 1:
            return True
        else:
            return False

    def get_rand_values(self, table, amount, fields):
        fields_str = ', '.join(fields) if len(fields) > 1 else fields[0]
        sql_select = f""" SELECT {fields_str} FROM {table} ORDER BY RANDOM() LIMIT {amount};"""
        self.cursor.execute(sql_select)
        # self.conn.commit()
        values = self.cursor.fetchall()
        if self.verbose >= Verbosity.HIGH:
            print(f'the rand values of table {table} are:')
            for val in values:
                print(val)
        return values

    def clean_table(self, table):
        self.cursor.execute(f""" DELETE FROM {table};""")
        self.conn.commit()
        if self.verbose >= Verbosity.HIGH:
            print(f'the table \'{table}\' was cleaned')
            self.get_entries(table)

    def update_word(self, table, cols, conds, params):
        cols_str = ''
        for col in cols:
            cols_str = f'{cols_str}{col}=?, '
        cols_str = cols_str[:-2]
        conds_str = ''
        for cond in conds:
            conds_str = f'{conds_str}{cond}=?, '
        conds_str = conds_str[:-2]
        sql_update = f""" UPDATE {table} SET {cols_str} WHERE {conds_str};"""
        self.cursor.execute(sql_update, params)
        self.conn.commit()
        if self.verbose >= Verbosity.LOW:
            # print(f'in table {table} in entry {cond}={params[3]} the col {col} was updated to {params[0]}')
            if self.verbose >= Verbosity.LOW:
                self.get_entries(table)

    def get_words(self, table, amount, cols):
        curr_date = str(date.today())
        cols_str = ', '.join(cols) if len(cols) > 1 else cols[0]
        sql_get = f""" SELECT {cols_str} FROM {table} WHERE (valid=1) AND (next_date BETWEEN '1970-01-01' AND '{curr_date}') 
                       ORDER BY next_date DESC, priority DESC LIMIT ?"""
        self.cursor.execute(sql_get, [amount])
        self.conn.commit()
        rows = self.cursor.fetchall()
        if len(rows) < amount:
            sql_get = f""" SELECT {cols_str} FROM {table} WHERE (valid=1) AND (next_date IS NULL)  
                            ORDER BY priority DESC LIMIT ?"""
            self.cursor.execute(sql_get, [amount - len(rows)])
            # self.conn.commit()
            null_date_rows = self.cursor.fetchall()
            if self.verbose >= Verbosity.HIGH:
                print(null_date_rows)
            rows = rows + null_date_rows
        if self.verbose >= Verbosity.HIGH:
            print(f'the rows ({len(rows)}) of table {table} are:')
            for row in rows:
                print(row)
        return rows
