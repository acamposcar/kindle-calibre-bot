import sqlite3


class db_users:
    def __init__(self, dbname="db.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)
        self.c = self.conn.cursor()

    def setup(self):
        table = "CREATE TABLE IF NOT EXISTS users (user_id integer PRIMARY KEY, user_email text)"
        self.conn.execute(table)
        self.conn.commit()
        self.conn.close()

    def add_item(self, user_id, user_email):
        self.__init__()
        self.c.execute("SELECT user_id FROM users")
        all_users = {x[0] for x in self.c.fetchall()}

        if user_id in all_users:
            if "@kindle.com" in user_email:
                stmt = "UPDATE users SET user_email=(?) WHERE user_id=(?)"
                args = (user_email, user_id)
                self.conn.execute(stmt, args)
                self.conn.commit()
        else:
            stmt = "INSERT INTO users (user_id, user_email) VALUES (?, ?)"
            args = (user_id, user_email)
            self.conn.execute(stmt, args)
            self.conn.commit()

        self.conn.close()

    def delete_item(self, user_id):
        self.__init__()
        stmt = "DELETE FROM users WHERE user_id = (?)"
        args = (user_id,)
        self.conn.execute(stmt, args)
        self.conn.commit()
        self.conn.close()

    def get_email(self, user_id):
        self.__init__()
        stmt = "SELECT user_email FROM users WHERE user_id = (?)"
        args = (user_id,)
        email = [x[0] for x in self.conn.execute(stmt, args)]
        self.conn.close()
        return email[0]
