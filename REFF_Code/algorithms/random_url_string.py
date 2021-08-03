import string
import random

# All characters used: 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
# That is a total of 3,521,614,606,208 possible 7-character combinations
def url_generator(size=7, chars=string.digits + string.ascii_letters):
    return ''.join(random.choice(chars) for _ in range(size))