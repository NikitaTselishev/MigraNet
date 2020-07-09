import psycopg2  # type: ignore
from psycopg2 import sql  # type: ignore

import config


def main():
    # fmt: off
    with psycopg2.connect(dbname=config.DB_NAME, user=config.DB_USER,
                          password=config.DB_PASSWORD, host=config.DB_HOST) as conn:
        with conn.cursor() as cursor:
            cursor.execute("DROP TABLE user_sessions")
            cursor.execute("DROP TABLE geolocations")
            cursor.execute("DROP TABLE chat_messages;")
            stmt = sql.SQL("DROP TABLE chats;")
            cursor.execute(stmt)
            cursor.execute("DROP TABLE action_members;")
            cursor.execute("DROP TABLE actions;")
            cursor.execute("DROP TABLE chat_ids;")
            cursor.execute("DROP TABLE friends;")
            cursor.execute("DROP TABLE wait_friend_add;")
            cursor.execute("DROP TABLE blocked_by_user;")
            stmt = sql.SQL("DROP TABLE users;")
            cursor.execute(stmt)
            print("Success")
    # fmt: on


if __name__ == "__main__":
    main()
