import time
numerator = 4.0 
denominator = 1.0 
total = 0.0
i = True 
iterations = 100000
j = 0
ct = time.time()
while (j < iterations):
    if i == True:
        total += (numerator / denominator)
    else:
        total -= (numerator / denominator)
    denominator += 2.0
    i = not i
    j += 1
print(total, "in", time.time() - ct, "seconds")
