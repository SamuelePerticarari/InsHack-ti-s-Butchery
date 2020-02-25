import random


def get_random_string(length=15):
    alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    string = ''
    for i in range(length):
        string += random.choice(alphabet)
    return string
