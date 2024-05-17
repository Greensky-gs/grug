class Cache:
    _cache = {}

    def __init__(self):
        self._cache = {}
    
    def cache(self, key, value = None):
        if value is None:
            if key in self._cache:
                self._cache.pop(key)
            return self._cache
        self._cache[key] = value
        return value
    def delete(self, key):
        if key in self._cache:
            self._cache.pop(key)
    def get(self, key, default = None):
        return self._cache.get(key, default)
    