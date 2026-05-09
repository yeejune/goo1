from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class Record:
    key: str
    long_url: str
    created_at: datetime
    ttl: timedelta
    access_count: int = 0

    def is_expired(self) -> bool:
        return datetime.utcnow() > self.created_at + self.ttl

class Storage:
    """Thread‑safe in‑memory storage used by the URL service.
    It implements the minimal CRUD methods required by the service.
    """
    def __init__(self):
        self._data: dict[str, Record] = {}
        self._lock = __import__('threading').Lock()

    def save(self, record: Record) -> None:
        with self._lock:
            self._data[record.key] = record

    def get(self, key: str) -> Record | None:
        with self._lock:
            return self._data.get(key)

    def get_by_long(self, long_url: str) -> Record | None:
        with self._lock:
            for rec in self._data.values():
                if rec.long_url == long_url:
                    return rec
            return None

    def exists(self, key: str) -> bool:
        with self._lock:
            return key in self._data

    def update(self, record: Record) -> None:
        # In‑memory update is simply a re‑save
        self.save(record)
