import datetime
import os
from typing import Any, Dict, List

import psycopg2


def get_conn() -> psycopg2.extensions.connection:
    ps = os.getenv("POSTGRES_PASSWORD")
    db_str = f"host=dump-db.fly.dev port=5433 user=postgres password={ps} dbname=dump connect_timeout=5 sslmode=require"
    conn = psycopg2.connect(db_str)
    return conn


def get_db_version(conn: psycopg2.extensions.connection) -> str:
    cur = conn.cursor()
    cur.execute("SELECT version()")
    db_version = cur.fetchone()
    return db_version


def get_db_tables(conn: psycopg2.extensions.connection) -> List[str]:
    cur = conn.cursor()
    cur.execute("SELECT * FROM information_schema.tables WHERE table_schema = 'public';")
    db_tables = cur.fetchall()

    table_names = [x[2] for x in db_tables]

    return table_names


def describe_db_table(conn: psycopg2.extensions.connection, table_name: str) -> List[Dict[str, Any]]:
    cur = conn.cursor()
    cur.execute(
        f"SELECT table_name, column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}';"
    )
    db_table_info = cur.fetchall()

    formatted = [{"col": x[1], "type": x[2]} for x in db_table_info]

    return formatted


def get_users(conn: psycopg2.extensions.connection) -> List[Dict[str, Any]]:
    cur = conn.cursor()
    cur.execute("SELECT * FROM users;")
    users = cur.fetchall()
    return users


def get_user(conn: psycopg2.extensions.connection, user_id) -> List[Dict[str, Any]]:
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users WHERE user_id = {user_id};")
    user = cur.fetchall()
    return user


def put_user(conn: psycopg2.extensions.connection, email) -> None:
    cur = conn.cursor()

    created_on = datetime.datetime.now()
    cur.execute("INSERT INTO users (email, created_on) VALUES (%s, %s)", (email, created_on))
    conn.commit()


def update_user(conn: psycopg2.extensions.connection, user_id, new_email) -> None:
    cur = conn.cursor()

    cur.execute("UPDATE users SET email = %s WHERE user_id = %s", (new_email, user_id))
    conn.commit()


def get_user_tags(conn: psycopg2.extensions.connection, user_id) -> List[Dict[str, Any]]:
    # TODO(gst): make this better in a data range
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM tags WHERE user_id = {user_id};")
    user_tags = cur.fetchall()
    return user_tags


def get_user_transcriptions(conn: psycopg2.extensions.connection, user_id) -> List[Dict[str, Any]]:
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM transcriptions WHERE user_id = {user_id};")
    user_transcriptions = cur.fetchall()
    return user_transcriptions


def put_user_transcription(conn: psycopg2.extensions.connection, user_id, transcription, version="0") -> None:
    cur = conn.cursor()

    created_on = datetime.datetime.now()
    cur.execute(
        "INSERT INTO transcriptions (user_id, text, version, created_on) VALUES (%s, %s, %s, %s)",
        (user_id, transcription, version, created_on),
    )
    conn.commit()


def main() -> None:
    conn = get_conn()
    db_version = get_db_version(conn)
    print(f"db_version={db_version}")
    tables = get_db_tables(conn)
    for table in tables:
        table_info = describe_db_table(conn, table)
        print(f"table {table}, info: {table_info}")

    # put_user(conn, "griffin@tarpenning.com")
    update_user(conn, 1, "gtarpenning@gmail.com")

    users = get_users(conn)
    print(f"{users=}")

    put_user_transcription(conn, 1, "hello world")

    transcriptions = get_user_transcriptions(conn, 1)
    print(f"{transcriptions=}")


if __name__ == "__main__":
    main()
