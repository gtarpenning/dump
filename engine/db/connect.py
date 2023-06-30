import datetime
import os
from typing import Any, Dict, List

import psycopg2


class DBConnection:
    def __init__(self):
        self.conn = self.get_conn()

    def get_conn(self) -> psycopg2.extensions.connection:
        ps = os.getenv("POSTGRES_PASSWORD")
        db_str = f"host=dump-db.fly.dev port=5433 user=postgres password={ps} dbname=dump connect_timeout=5 sslmode=require"
        conn = psycopg2.connect(db_str)
        return conn

    def get_db_version(self) -> str:
        cur = self.conn.cursor()
        cur.execute("SELECT version()")
        db_version = cur.fetchone()
        return db_version

    def get_db_tables(self) -> List[str]:
        cur = self.conn.cursor()
        cur.execute(
            "SELECT * FROM information_schema.tables WHERE table_schema = 'public';"
        )
        db_tables = cur.fetchall()

        table_names: List[str] = [x[2] for x in db_tables]

        return table_names

    def describe_db_table(self, table_name: str) -> List[Dict[str, str]]:
        cur = self.conn.cursor()
        cur.execute(
            f"SELECT table_name, column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}';"
        )
        db_table_info = cur.fetchall()

        formatted: List[Dict[str, str]] = [
            {"col": x[1], "type": x[2]} for x in db_table_info
        ]

        return formatted

    def get_users(self) -> List[Dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM users;")
        users: List[Dict[str, Any]] = cur.fetchall()
        return users

    def get_user(self, user_id) -> Dict[str, Any]:
        cur = self.conn.cursor()
        cur.execute(f"SELECT * FROM users WHERE user_id = {user_id};")
        user: Dict[str, Any] = cur.fetchall()
        return user

    def put_user(self, email) -> None:
        cur = self.conn.cursor()

        created_on = datetime.datetime.now()
        cur.execute(
            "INSERT INTO users (email, created_on) VALUES (%s, %s)", (email, created_on)
        )
        self.conn.commit()

    def update_user(self, user_id, new_email) -> None:
        cur = self.conn.cursor()

        cur.execute(
            "UPDATE users SET email = %s WHERE user_id = %s", (new_email, user_id)
        )
        self.conn.commit()

    def get_user_tags(self, user_id) -> List[Any]:
        # TODO(gst): make this better in a data range
        cur = self.conn.cursor()
        cur.execute(f"SELECT * FROM tags WHERE user_id = {user_id};")
        user_tags: List[Any] = cur.fetchall()
        return user_tags

    def get_user_transcriptions(self, user_id) -> List[Any]:
        cur = self.conn.cursor()
        cur.execute(f"SELECT * FROM transcriptions WHERE user_id = {user_id};")
        user_transcriptions: List[Any] = cur.fetchall()
        return user_transcriptions

    def put_user_transcription(self, user_id, transcription, version="0") -> None:
        cur = self.conn.cursor()

        created_on = datetime.datetime.now()
        cur.execute(
            "INSERT INTO transcriptions (user_id, text, version, created_on) VALUES (%s, %s, %s, %s)",
            (user_id, transcription, version, created_on),
        )
        self.conn.commit()

    def get_user_tags_from_tags(self, user_id, tags: List[str]) -> List[List[Any]]:
        cur = self.conn.cursor()
        tag_str = list_to_sql_str(tags)
        cur.execute(
            f"SELECT * FROM tags WHERE user_id = {user_id} AND (tag IN {tag_str});"
        )
        occurences: List[List[Any]] = cur.fetchall()

        return occurences

    def put_user_tags(self, user_id, tags: List[str]) -> None:
        cur = self.conn.cursor()

        date = datetime.datetime.now()
        for tag in tags:
            cur.execute(
                "INSERT INTO tags (user_id, tag, date) VALUES (%s, %s, %s)",
                (user_id, tag, date),
            )
        self.conn.commit()


def list_to_sql_str(words: List[str]) -> str:
    list_str = ", ".join([f"'{x.strip()}'" for x in words])
    return f"({list_str})"


def main() -> None:
    db = DBConnection()
    db_version = db.get_db_version()
    print(f"db_version={db_version}")
    tables = db.get_db_tables()
    for table in tables:
        table_info = db.describe_db_table(table)
        print(f"table {table}, info: {table_info}")

    # put_user(conn, "griffin@tarpenning.com")
    db.update_user(1, "gtarpenning@gmail.com")

    users = db.get_users()
    print(f"{users=}")

    db.put_user_transcription(1, "hello world")

    transcriptions = db.get_user_transcriptions(1)
    print(f"{transcriptions=}")


if __name__ == "__main__":
    main()
