import numpy as np
with open('W9.txt', "r") as ins:
    for line in ins:
	items = line.split(",")
tmp=np.asarray(items)
ttmp = tmp.astype(np.float)
W7_txt = ttmp.reshape(1, 10)

with open('W1.txt', "r") as ins:
    for line in ins:
	items = line.split(",")
tmp=np.asarray(items)
ttmp = tmp.astype(np.float)
W1_txt = ttmp.reshape(5,5,1,24)
print(type(W1_txt[0][0][0][0]))