import string
import random
def text_generator(length):
    text = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
    return text

