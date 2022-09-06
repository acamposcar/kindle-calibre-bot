import psycopg2
from os import getenv
from dotenv import load_dotenv

load_dotenv()

HOST = getenv("HOST")
USER = getenv("USER")
PASSWORD = getenv("PASSWORD")
DATABASE = getenv("DATABASE")
PORT = getenv("PORT")


class db_users:
    def __init__(self):

        self.conn = psycopg2.connect(
            host=HOST, database=DATABASE, user=USER, password=PASSWORD, port=PORT
        )
        self.c = self.conn.cursor()

    def setup(self):
        table = "CREATE TABLE IF NOT EXISTS users (user_id bigint PRIMARY KEY, user_email text, user_downloads integer)"
        self.c.execute(table)
        self.conn.commit()
        self.conn.close()

    def add_item(self, user_id, user_email):
        self.__init__()
        self.c.execute("SELECT user_id FROM users")
        all_users = {x[0] for x in self.c.fetchall()}

        if user_id in all_users:
            if "@kindle.com" in user_email:
                stmt = "UPDATE users SET user_email=(%s) WHERE user_id=(%s)"
                args = (user_email, user_id)
                self.c.execute(stmt, args)
                self.conn.commit()
        else:
            stmt = "INSERT INTO users (user_id, user_email, user_downloads) VALUES (%s, %s, %s)"
            args = (user_id, user_email, 0)
            self.c.execute(stmt, args)
            self.conn.commit()

        self.conn.close()

    def add_download(self, user_id):
        self.__init__()

        # Increment user downloads
        stmt = "UPDATE users SET user_downloads=user_downloads+1 WHERE user_id=(%s)"
        args = (user_id,)
        self.c.execute(stmt, args)
        self.conn.commit()

        self.conn.close()

    def delete_email(self, user_id):
        self.__init__()
        stmt = "UPDATE users SET user_email=(%s) WHERE user_id=(%s)"
        args = (
            "",
            user_id,
        )
        self.c.execute(stmt, args)
        self.conn.commit()
        self.conn.close()

    def is_banned(self, user_id):
        self.__init__()
        stmt = "SELECT banned FROM users WHERE user_id = (%s)"
        args = (user_id,)
        self.c.execute(stmt, args)
        banned = self.c.fetchone()[0]
        self.conn.close()
        return banned

    def get_email(self, user_id):
        self.__init__()
        stmt = "SELECT user_email FROM users WHERE user_id = (%s)"
        args = (user_id,)
        self.c.execute(stmt, args)
        email = self.c.fetchone()[0]
        self.conn.close()
        return email
