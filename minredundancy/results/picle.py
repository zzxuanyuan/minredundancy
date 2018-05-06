import pickle
import sys
import matplotlib.pyplot as plt

with open ('suogce_avail_080.txt', 'rb') as fp:
	suogce_avail_080_list = pickle.load(fp)
	fp.close()
with open ('suogce_avail_090.txt', 'rb') as fp:
	suogce_avail_090_list = pickle.load(fp)
	fp.close()
with open ('suogce_avail_099.txt', 'rb') as fp:
	suogce_avail_099_list = pickle.load(fp)
	fp.close()
with open ('glow_avail_080.txt', 'rb') as fp:
	glow_avail_080_list = pickle.load(fp)
	fp.close()
with open ('glow_avail_090.txt', 'rb') as fp:
	glow_avail_090_list = pickle.load(fp)
	fp.close()
with open ('glow_avail_099.txt', 'rb') as fp:
	glow_avail_099_list = pickle.load(fp)
	fp.close()
with open ('mwt2_avail_080.txt', 'rb') as fp:
	mwt2_avail_080_list = pickle.load(fp)
	fp.close()
with open ('mwt2_avail_090.txt', 'rb') as fp:
	mwt2_avail_090_list = pickle.load(fp)
	fp.close()
with open ('mwt2_avail_099.txt', 'rb') as fp:
	mwt2_avail_099_list = pickle.load(fp)
	fp.close()


n, bins, patches = plt.hist(suogce_avail_080_list, 50, normed=1, facecolor='green', alpha=0.75)
plt.gca()
n, bins, patches = plt.hist(suogce_avail_090_list, 50, normed=1, facecolor='blue', alpha=0.75)
plt.gca()
n, bins, patches = plt.hist(suogce_avail_099_list, 50, normed=1, facecolor='red', alpha=0.75)
plt.show()

n, bins, patches = plt.hist(glow_avail_080_list, 50, normed=1, facecolor='green', alpha=0.75)
plt.gca()
n, bins, patches = plt.hist(glow_avail_090_list, 50, normed=1, facecolor='blue', alpha=0.75)
plt.gca()
n, bins, patches = plt.hist(glow_avail_099_list, 50, normed=1, facecolor='red', alpha=0.75)
plt.show()

n, bins, patches = plt.hist(mwt2_avail_080_list, 50, normed=1, facecolor='green', alpha=0.75)
plt.gca()
n, bins, patches = plt.hist(mwt2_avail_090_list, 50, normed=1, facecolor='blue', alpha=0.75)
plt.gca()
n, bins, patches = plt.hist(mwt2_avail_099_list, 50, normed=1, facecolor='red', alpha=0.75)
plt.show()
