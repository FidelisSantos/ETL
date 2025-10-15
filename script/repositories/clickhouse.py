from typing import Any, Dict, List
from clickhouse_driver import Client as ClickHouseClient

class ClickHouseRepository:
    def __init__(self, host: str, database: str, user: str = "default", password: str = ""):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def _get_client(self) -> ClickHouseClient:
        return ClickHouseClient(host=self.host, database=self.database, user=self.user, password=self.password)

    def insert_one(self, table: str, data: Dict[str, Any]):
        cols = ", ".join(data.keys())
        values = [tuple(data.values())]
        client = self._get_client()
        client.execute(f"INSERT INTO {table} ({cols}) VALUES", values)
        return 1

    def insert_many(self, table: str, data: List[Dict[str, Any]]):
        if not data:
            return 0
        cols = ", ".join(data[0].keys())
        values = [tuple(d.values()) for d in data]
        client = self._get_client()
        client.execute(f"INSERT INTO {table} ({cols}) VALUES", values)
        return len(values)
