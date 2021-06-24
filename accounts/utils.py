import random
import string

def create_unique_id():
    return ''.join(random.choices(string.digits, k=10))
