import string
import random

# All characters used: 'abcdefghijklmnopqrstuvwxyz0123456789' -> that is a total of 34,359,738,368 permutations (order important: yes, repetition allowed: yes)
# When using capital letters too we get a total of 3,521,614,606,208 possible permutations (order important: yes, repetition allowed: yes), however we've decided not to use capital letters
def url_generator(size=7, chars=string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))
