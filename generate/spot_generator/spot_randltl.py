import spot
import random

# go and check spot gitlab (on my computer spot_next) and under test/python check all the tests. there is randltl.py


for i in range(5):
    f = spot.randltl(['a', 'b', 'c'], seed=random.randint(1, 10000))
    print(next(f))
