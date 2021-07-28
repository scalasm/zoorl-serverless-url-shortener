import hashlib

from datetime import datetime, timedelta

def compute_epoch_time_from_ttl(days_from_now: int) -> int:
    """Compute the UNIX epoch time from now according to the specified threshold"""
    now = get_now()

    time_delta = timedelta(days=days_from_now)
    ttl_date = now + time_delta
    return int(ttl_date.timestamp())

def compute_hash(url: str) -> str:
    """Compute the hash of a given URL as Base62-encoded string"""
    hash = int(hashlib.sha256(url.encode('utf-8')).hexdigest(), 16) % 10**12

    return to_base_62(hash)

def to_base_62(some_number: int) -> str:
    """Encode a number into its Base62 representation"""
    s = '012345689abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    hash_str = ''
    while some_number > 0:
       hash_str = s[some_number % 62] + hash_str
       some_number //= 62
    return hash_str

def get_now() -> datetime:
    """Compute this instant (this is needed for testing, since we cannot mock datetime built-in type)"""
    return datetime.now()
