import random
import string
from datetime import timedelta
from .storage import Storage, Record

BASE62 = string.digits + string.ascii_letters

def _generate_key(length: int = 6) -> str:
    return ''.join(random.choice(BASE62) for _ in range(length))

class URLService:
    def __init__(self, storage: Storage = None, ttl: timedelta = timedelta(hours=24)):
        self.storage = storage if storage is not None else Storage()
        self.ttl = ttl

    def create_short(self, long_url: str) -> str:
        # Idempotency: return existing key if long URL already stored
        existing = self.storage.get_by_long(long_url)
        if existing:
            return existing.key
        # generate unique key
        key = _generate_key()
        while self.storage.exists(key):
            key = _generate_key()
        rec = Record(
            key=key,
            long_url=long_url,
            created_at=__import__('datetime').datetime.utcnow(),
            ttl=self.ttl,
            access_count=0,
        )
        self.storage.save(rec)
        return key

    def resolve(self, key: str) -> str:
        rec = self.storage.get(key)
        if not rec:
            raise KeyError('short key not found')
        if rec.is_expired():
            raise KeyError('short key expired')
        rec.access_count += 1
        self.storage.update(rec)
        return rec.long_url

    def stats(self, key: str) -> dict:
        rec = self.storage.get(key)
        if not rec:
            raise KeyError('short key not found')
        return {
            'original_url': rec.long_url,
            'access_count': rec.access_count,
            'expires_at': rec.created_at + rec.ttl,
        }
