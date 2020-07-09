from typing import *
from dataclasses import dataclass

import psycopg2  # type: ignore
from psycopg2 import sql
from psycopg2.extras import RealDictCursor, RealDictRow  # type: ignore


@dataclass
class PostgreSQL:
    db_host: str
    db_name: str
    user: str
    _password: str

    def get_from(
        self,
        identifier: str,
        columns: Optional[Union[Iterable[str], Iterator[str]]] = None,
    ) -> List[RealDictRow]:
        with psycopg2.connect(
            dbname=self.db_name,
            user=self.user,
            password=self._password,
            host=self.db_host,
        ) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                if columns:
                    stmt = sql.SQL("SELECT {} FROM {}").format(
                        sql.SQL(",").join(map(sql.Identifier, columns)),
                        sql.Identifier(identifier),
                    )
                else:
                    stmt = sql.SQL("SELECT * FROM {}").format(
                        sql.Identifier(identifier)
                    )
                cursor.execute(stmt)
                return cursor.fetchall()

    def get_from_where(
        self,
        identifier: str,
        condition: str,
        columns: Optional[Union[Iterable[str], Iterator[str]]] = None,
    ) -> List[RealDictRow]:
        with psycopg2.connect(
            dbname=self.db_name,
            user=self.user,
            password=self._password,
            host=self.db_host,
        ) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                s = "SELECT %s FROM {} WHERE %s" % ("%s", condition)
                if columns:
                    s = s % "{}"
                    stmt = sql.SQL(s).format(
                        sql.SQL(",").join(map(sql.Identifier, columns)),
                        sql.Identifier(identifier),
                    )
                else:
                    s = s % "*"
                    stmt = sql.SQL(s).format(sql.Identifier(identifier))
                cursor.execute(stmt)
                return cursor.fetchall()

    def insert_value(self, identifier: str, data: Dict[str, Any]) -> None:
        with psycopg2.connect(
            dbname=self.db_name,
            user=self.user,
            password=self._password,
            host=self.db_host,
        ) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                keys = data.keys()
                values = [data[k] for k in keys]
                stmt = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                    sql.Identifier(identifier),
                    sql.SQL(",").join(map(sql.Identifier, keys)),
                    sql.SQL(",").join(map(sql.Literal, values)),
                )
                cursor.execute(stmt)

    def mass_insert_values(
        self, identifier: str, data: List[Dict[str, Any]]
    ) -> None:
        with psycopg2.connect(
            dbname=self.db_name,
            user=self.user,
            password=self._password,
            host=self.db_host,
        ) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                if not data:
                    return
                main_keys = list(data[0].keys())
                stmt = sql.SQL(
                    "INSERT INTO {} ({}) VALUES %s"
                    % ",".join(["({})" for _ in range(len(data))])
                ).format(
                    sql.Identifier(identifier),
                    sql.SQL(",").join(map(sql.Identifier, main_keys)),
                    *[
                        sql.SQL(",").join(
                            map(sql.Literal, [d[k] for k in main_keys])
                        )
                        for d in data
                    ]
                )
                cursor.execute(stmt)

    def delete_from_where(self, identifier: str, condition: str) -> None:
        with psycopg2.connect(
            dbname=self.db_name,
            user=self.user,
            password=self._password,
            host=self.db_host,
        ) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                s = "DELETE FROM {} WHERE %s" % condition
                stmt = sql.SQL(s).format(sql.Identifier(identifier))
                cursor.execute(stmt)


if __name__ == "__main__":
    import config

    db = PostgreSQL(
        config.DB_HOST, config.DB_NAME, config.DB_USER, config.DB_PASSWORD
    )
    print(db.get_from("users"))
    print(db.get_from_where("users", "user_id>1", ["user_id"]))
    print(db.get_from_where("users", "user_id>1 AND password='Nick'"))
