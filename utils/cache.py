import memcache

mc = memcache.Client(["127.0.0.1:11211"], debug=True)

def set(key, value, timeout=60*10):
    return mc.set(key=key, val=value, time=timeout)

def get(key):
    return mc.get(key=key)

def delete(key):
    return mc.delete(key=key)