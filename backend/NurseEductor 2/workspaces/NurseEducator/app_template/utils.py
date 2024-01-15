import random
import string

def generate_random_code():
    # Select 2 random alphabets
    alphabets = ''.join(random.choices(string.ascii_uppercase, k=3))

    # Select 3 random numeric values
    numbers = ''.join(random.choices(string.digits, k=3))

    # Combine alphabets and numbers
    random_string = alphabets + numbers

    # Shuffle the characters in the string
    random_list = list(random_string)
    random.shuffle(random_list)
    shuffled_random_string = ''.join(random_list)

    return shuffled_random_string
