import os

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


def main() -> None:
    conn = get_conn()
    db_version = get_db_version(conn)
    print(f"db_version={db_version}")


if __name__ == "__main__":
    main()
