from os import getenv
from dotenv import load_dotenv
import sqlite3

load_dotenv()


class db_users:
    def __init__(self):
        self.conn = sqlite3.connect('./database/db.db')
        self.c = self.conn.cursor()

    def setup(self):
        users_table = """
        CREATE TABLE IF NOT EXISTS users (
        user_id integer PRIMARY KEY, 
        email text DEFAULT '', 
        banned integer DEFAULT 0, 
        joined_at datetime DEFAULT CURRENT_TIMESTAMP)"""
        self.c.execute(users_table)

        downloads_table = """
        CREATE TABLE IF NOT EXISTS downloads (
        user_id integer NOT NULL REFERENCES users(user_id), 
        date datetime DEFAULT CURRENT_TIMESTAMP, 
        input text, 
        output text,
        email integer)
        """
        self.c.execute(downloads_table)
        
        self.conn.commit()
        self.conn.close()

    def add_user(self, user_id):
        self.__init__()
        stmt = (
            "INSERT INTO users (user_id) VALUES (?) ON CONFLICT (user_id) DO NOTHING;"
        )
        args = (user_id,)
        self.c.execute(stmt, args)
        self.conn.commit()

        self.conn.close()

    def update_email(self, user_id, user_email):
        self.add_user(user_id)

        self.__init__()
        stmt = "UPDATE users SET email=(?) WHERE user_id=(?)"
        args = (user_email, user_id)
        self.c.execute(stmt, args)
        self.conn.commit()
        self.conn.close()

    def add_download(self, user_id, input_extension, output_extension, is_email):
        self.add_user(user_id)

        self.__init__()
        # Increment user downloads
        
        stmt = "INSERT INTO downloads(user_id, input, output, email) VALUES (?, ?, ?, ?)"
        args = (user_id, input_extension, output_extension, is_email)
        self.c.execute(stmt, args)
        self.conn.commit()

        self.conn.close()

    def delete_email(self, user_id):
        self.__init__()
        
        stmt = "UPDATE users SET email='' WHERE user_id=(?)"
        args = (user_id,)
        self.c.execute(stmt, args)
        self.conn.commit()
        self.conn.close()

    def is_banned(self, user_id):
        self.__init__()
        stmt = "SELECT banned FROM users WHERE user_id = (?)"
        args = (user_id,)
        self.c.execute(stmt, args)
        banned = self.c.fetchone()[0]
        self.conn.close()
        return banned

    def get_email(self, user_id):
        self.__init__()
        stmt = "SELECT email FROM users WHERE user_id = (?)"
        args = (user_id,)
        self.c.execute(stmt, args)
        email = self.c.fetchone()[0]
        self.conn.close()
        return email

    def get_total_downloads(self):
        self.__init__()
        stmt = "SELECT count(*) FROM downloads"
        self.c.execute(stmt)
        total_downloads = self.c.fetchone()[0]
        self.conn.close()
        return total_downloads

    def get_monthly_downloads(self):
        self.__init__()
        stmt = "SELECT count(*) FROM downloads WHERE date >= date('now', '-30 days')"
        self.c.execute(stmt)
        month_downloads = self.c.fetchone()[0]
        self.conn.close()
        return month_downloads

    def get_top_users_downloads(self):
        self.__init__()
        stmt = "SELECT user_id,count(*) FROM downloads GROUP BY user_id ORDER BY count(*) DESC LIMIT 10"
        self.c.execute(stmt)
        user_downloads = self.c.fetchall()
        self.conn.close()
        return user_downloads

    def get_top_users_monthly_downloads(self):
        self.__init__()
        stmt = "SELECT user_id,count(*) FROM downloads WHERE date >= date('now', '-30 day') GROUP BY user_id ORDER BY count(*) DESC LIMIT 10"
        self.c.execute(stmt)
        user_downloads = self.c.fetchall()
        self.conn.close()
        return user_downloads

    def get_downloads_by_month(self):
        self.__init__()
        stmt = "SELECT strftime('%Y-%m', date) AS month, count(*) FROM downloads GROUP BY month ORDER BY month DESC LIMIT 12"
        self.c.execute(stmt)
        downloads_by_month = self.c.fetchall()
        self.conn.close()
        return downloads_by_month

    def get_total_users(self):
        self.__init__()
        stmt = "SELECT count(*) FROM users"
        self.c.execute(stmt)
        total_users = self.c.fetchone()[0]
        self.conn.close()
        return total_users

    def get_all_users(self):
        self.__init__()
        stmt = "SELECT user_id FROM users"
        self.c.execute(stmt)
        users = self.c.fetchall()
        self.conn.close()
        return users

    def get_user_downloads_today(self, user_id):
        self.add_user(user_id)

        self.__init__()
        stmt = "SELECT count(*) FROM downloads WHERE user_id = (?) AND date >= date('now')"
        args = (user_id,)
        self.c.execute(stmt, args)
        downloads_today = self.c.fetchone()[0]
        self.conn.close()
        return downloads_today
