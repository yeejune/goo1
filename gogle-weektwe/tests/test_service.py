import pytest
from src.service import URLService
from src.storage import Storage
from datetime import timedelta

@pytest.fixture
def service():
    # fresh storage for each test
    return URLService(storage=Storage(), ttl=timedelta(seconds=1))

def test_create_short_returns_key(service):
    key = service.create_short('https://www.safetydata.go.kr/viewer/skin/doc.html?fn=d7518c722f961c13f031d401a5de6792449f916a267c2c096b0db9c5dfa2114f&rs=/viewer/viewerFile/')
    assert isinstance(key, str)
    assert len(key) == 6

def test_idempotent_creation(service):
    key1 = service.create_short('https://www.safetydata.go.kr/viewer/skin/doc.html?fn=d7518c722f961c13f031d401a5de6792449f916a267c2c096b0db9c5dfa2114f&rs=/viewer/viewerFile/')
    key2 = service.create_short('https://www.safetydata.go.kr/viewer/skin/doc.html?fn=d7518c722f961c13f031d401a5de6792449f916a267c2c096b0db9c5dfa2114f&rs=/viewer/viewerFile/')
    assert key1 == key2

def test_resolve_and_access_count(service):
    url = 'https://www.safetydata.go.kr/viewer/skin/doc.html?fn=d7518c722f961c13f031d401a5de6792449f916a267c2c096b0db9c5dfa2114f&rs=/viewer/viewerFile/'
    key = service.create_short(url)
    # first resolve increments count to 1
    assert service.resolve(key) == url
    stats = service.stats(key)
    assert stats['access_count'] == 1
    # second resolve increments count to 2
    service.resolve(key)
    stats = service.stats(key)
    assert stats['access_count'] == 2

def test_expiration(service):
    # ttl is 1 second from fixture
    key = service.create_short('https://www.safetydata.go.kr/viewer/skin/doc.html?fn=d7518c722f961c13f031d401a5de6792449f916a267c2c096b0db9c5dfa2114f&rs=/viewer/viewerFile/')
    # wait for ttl to pass
    import time; time.sleep(2)
    with pytest.raises(KeyError):
        service.resolve(key)
