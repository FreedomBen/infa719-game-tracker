import random


def getBoolean(is_private):
    if is_private == 'True':
        return True
    return False
    
def getLetter():
    return chr(random.randint(ord('A'), ord('Z'))) + chr(random.randint(ord('A'), ord('Z')))