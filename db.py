import sqlite3
import os

class Database():
    def __init__(self, file='db.db'):
        if not os.path.isfile(file):
            raise FileNotFoundError('Database file was not found...')
        self.file = file

    def __enter__(self):
        try:
            self.conn = sqlite3.connect(self.file)
        except sqlite3.Error as error:
            raise ConnectionError('Could not connect to the main database...')
        # Enable foreign keys
        self.conn.execute("PRAGMA foreign_keys = 1")
        # Return results as a dict object?
        self.conn.row_factory = sqlite3.Row
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()

    def _create_database(self):
        conn = sqlite3.connect(self.file)
        cursor = conn.cursor()

        create_names_table(cursor)
        create_emails_table(cursor)
        create_addresses_table(cursor)
        create_bank_accounts_table(cursor)
        create_sources_table(cursor)
        create_yougov_accounts_table(cursor)
        create_yougov_custom_fields_table(cursor)
        create_yougov_ip_addresses_table(cursor)
        create_yougov_tasks_table(cursor)
        create_yougov_upload_history(cursor)

        cursor.close()
        conn.close()



def create_names_table(cursor):
    cursor.execute("""CREATE TABLE names (
                name_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                name TEXT NOT NULL UNIQUE
        )""")

def create_emails_table(cursor):
    cursor.execute("""CREATE TABLE emails (
                email_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                email TEXT NOT NULL UNIQUE
        )""")

def create_addresses_table(cursor):
    cursor.execute("""CREATE TABLE addresses (
                address_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                address TEXT NOT NULL UNIQUE,
                city TEXT NOT NULL,
                postcode TEXT NOT NULL
        )""")

def create_bank_accounts_table(cursor):
    cursor.execute("""CREATE TABLE bank_accounts (
                bank_account_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                sort_code INTEGER NOT NULL,
                account_number INTEGER NOT NULL UNIQUE,
                account_name TEXT NOT NULL,
                description TEXT,
                available INTEGER NOT NULL DEFAULT 1
        )""")

def create_sources_table(cursor):
    cursor.execute("""CREATE TABLE sources (
                source_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                source TEXT NOT NULL UNIQUE
        )""")

def create_yougov_accounts_table(cursor):
    cursor.execute("""CREATE TABLE yougov_accounts (
                account_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                auth_token TEXT UNIQUE,
                points INTEGER DEFAULT NULL,
                user_agent TEXT DEFAULT NULL,
                name_id INTEGER NOT NULL UNIQUE,
                email_id INTEGER NOT NULL UNIQUE,
                address_id INTEGER NOT NULL UNIQUE,
                bank_account_id INTEGER NOT NULL UNIQUE,
                FOREIGN KEY (name_id) REFERENCES names (name_id),
                FOREIGN KEY (email_id) REFERENCES names (email_id),
                FOREIGN KEY (address_id) REFERENCES names (address_id),
                FOREIGN KEY (bank_account_id) REFERENCES names (bank_account_id)

        )""")

def create_yougov_custom_fields_table(cursor):
    cursor.execute("""CREATE TABLE yougov_custom_fields (
                custom_field_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                custom_field TEXT NOT NULL,
                value TEXT NOT NULL,
                account_id INTEGER NOT NULL,
                FOREIGN KEY (account_id) REFERENCES names (account_id)
        )""")

def create_yougov_ip_addresses_table(cursor):
    cursor.execute("""CREATE TABLE yougov_ip_addresses (
                ip_address_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                ip_address TEXT NOT NULL UNIQUE,
                account_id INTEGER NOT NULL,
                FOREIGN KEY (account_id) REFERENCES names (account_id)
        )""")

def create_yougov_tasks_table(cursor):
    cursor.execute("""CREATE TABLE yougov_tasks (
                custom_field_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                next_upload_date INTEGER NOT NULL,
                account_id INTEGER NOT NULL,
                source_id INTEGER NOT NULL,
                FOREIGN KEY (source_id) REFERENCES sources (source_id),
                FOREIGN KEY (account_id) REFERENCES names (account_id)
        )""")

def create_yougov_upload_history(cursor):
    cursor.execute("""CREATE TABLE yougov_upload_history (
                upload_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                points_earned INTEGER NOT NULL,
                upload_date INTEGER NOT NULL,
                account_id INTEGER NOT NULL,
                source_id INTEGER NOT NULL,
                FOREIGN KEY (source_id) REFERENCES sources (source_id),
                FOREIGN KEY (account_id) REFERENCES names (account_id)
        )""")

