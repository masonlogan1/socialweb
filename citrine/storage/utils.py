from math import ceil, sqrt

from citrine.storage.consts import DEFAULT_COLLECTION_SIZE

def is_prime(num) -> bool:
    """
    Determine if a number is prime
    :param num: number to check
    :return: whether the number is prime
    """
    for i in range(2, int(sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True


def get_primes(min=1, max=None):
    """
    Generates all prime numbers starting at 1. If no max is provided, the
    generator will go indefinitely
    :param min: starting value, defaults to 1
    :param max: stopping value, optional
    :return: prime integers
    """
    val = min
    while not max or val > max:
        if is_prime(val):
            yield val
        val += 1

def number_of_collections(
        capacity: int,
        max_collection_size: int = DEFAULT_COLLECTION_SIZE,
):
    """
    Generates a recommended number of collections based on the desired capacity
    and maximum collection size. Does not guarantee that the total number of
    items for the number of containers will match the capacity exactly,
    only that the number of containers will be prime and able to hold all
    items in the desired capacity.
    :param capacity: the number of items that must be able to fit
    :param max_collection_size: the maximum number of items per collection
    :return: smallest prime number of collections capable of handling capacity
    """
    needed_collections = ceil(capacity / max_collection_size)

    # the number needs to be prime, or we risk entire collections being skipped
    # by the id hashing process
    next_prime = next(get_primes(min=needed_collections))

    return next_prime

def next_number_of_collections(
        current_max_size: int,
        max_collection_size: int = DEFAULT_COLLECTION_SIZE) -> int:
    """
    Determines how many collections the next primary group will need to contain
    :param current_max_size: current max number of items
    :param max_collection_size: max number of items in each collection
    :return: number of collections that will need to be created
    """
    needed_size = ceil(current_max_size * 1.5)
    needed_collections = ceil(needed_size/max_collection_size)

    # the number needs to be prime, or we risk entire collections being skipped
    # by the id hashing process
    next_prime = next(get_primes(min=needed_collections))

    return next_prime
