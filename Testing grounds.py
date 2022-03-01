import random
        #They generate the same number so:
seed=10
random.seed(seed) 
print(random.random())
seed+=1
random.seed(seed)
print(random.random()) 