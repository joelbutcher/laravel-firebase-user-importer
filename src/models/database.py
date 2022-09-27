import time
from typing import Optional
import pymysql
from pymysql.cursors import Cursor
from src.models.errors import DbConnectionError


class Database:
    def __init__(
        self,
        host: str,
        port: int,
        database: str,
        username: str,
        password: str,
        charset: str = "utf8mb4",
        cursor=pymysql.cursors.DictCursor,
    ):
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        self.charset = charset
        self.cursor = cursor

    def new_connection(
        self,
        max_attempts: int = 5,
        wait_time_seconds: Optional[int] = None,
    ) -> pymysql.connect:
        """Returns a connection object to a database.

        Args:
            max_attempts (int): Maximum number of connection attempts.
            wait_time_seconds (Optional[int]): Seconds to wait between connection attempts.

        Returns:
            connector (pymysql.connect): Connection object.

        Raises:
            DbConnectionError when unable to connect to database after max attempts.
        """
        for attempt in range(1, max_attempts + 1):
            try:
                return pymysql.connect(
                    host=self.host,
                    port=self.port,
                    user=self.username,
                    password=self.password,
                    database=self.database,
                    charset=self.charset,
                    cursorclass=self.cursor,
                )
            except Exception as exc:
                if attempt >= max_attempts:
                    raise DbConnectionError(exc=exc, max_retries=attempt)
                time.sleep(wait_time_seconds or attempt)
                continue

    @staticmethod
    def fetch_data(connection: pymysql.connect, sql: str):
        with connection.cursor() as cursor:
            cursor.execute(query=sql)
            return cursor.fetchall()

    def ping(self) -> dict[str, str]:
        """Returns a status ok when able to connect to a database.

        Returns:
            health_check (dict[str, str]): ok status when able to connect to database.

        Raises:
            DbConnectionError when unable to connect to database after max attempts.
        """
        try:
            connection = self.new_connection()
            connection.close()
            return {"status": "ok"}
        except DbConnectionError as exc:
            raise exc
