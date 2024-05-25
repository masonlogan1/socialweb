"""
Contains importable dicts of crystallization/decrystallization caches

Caches are scoped to the thread in which they are used and will need to be
regenerated in different threads
"""

CRYSTALLIZATION_CACHE = {}
DECRYSTALLIZATION_CACHE = {}


def save_to_crystallization_cache(id, cls):
    CRYSTALLIZATION_CACHE[id] = cls


def save_to_decrystallization_cache(id, cls):
    DECRYSTALLIZATION_CACHE[id] = cls


def crystallization_cache_has(id):
    return id in CRYSTALLIZATION_CACHE.keys()


def decrystallization_cache_has(id):
    return id in DECRYSTALLIZATION_CACHE.keys()


def load_from_crystallization_cache(id):
    return CRYSTALLIZATION_CACHE.get(id, None)


def load_from_decrystallization_cache(id):
    return DECRYSTALLIZATION_CACHE.get(id, None)
