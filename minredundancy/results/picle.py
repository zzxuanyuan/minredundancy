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

p1 = plt.subplot(5,1,1)

f1 = plt.subplot(3,1,1)
n, bins, patches = plt.hist(suogce_avail_080_list, 50, normed=1, facecolor='green', alpha=0.75, label='Availability = 0.80')
plt.title('Distribution of Data Loss Rate on C39')
ax1 = plt.gca()
ax1.set_xlim(xmin=0.0,xmax=1.0)
f2 = plt.subplot(3,1,2)
n, bins, patches = plt.hist(suogce_avail_090_list, 50, normed=1, facecolor='blue', alpha=0.75, label='Availability = 0.90')
ax2 = plt.gca()
plt.ylabel('Probability')
ax2.set_xlim(xmin=0.0,xmax=1.0)
f3 = plt.subplot(3,1,3)
n, bins, patches = plt.hist(suogce_avail_099_list, 50, normed=1, facecolor='red', alpha=0.75, label='Availability = 0.99')
ax3 = plt.gca()
ax3.set_xlim(xmin=0.0,xmax=1.0)
plt.xlabel('Data Loss Rate')
plt.show()

f1 = plt.subplot(3,1,1)
n, bins, patches = plt.hist(glow_avail_080_list, 50, normed=1, facecolor='green', alpha=0.75, label='Availability = 0.80')
plt.legend()
plt.title('Distribution of Data Loss Rate on C10')
ax1 = plt.gca()
ax1.set_xlim(xmin=0.0,xmax=0.3)
f2 = plt.subplot(3,1,2)
n, bins, patches = plt.hist(glow_avail_090_list, 50, normed=1, facecolor='blue', alpha=0.75, label='Availability = 0.90')
plt.legend()
ax2 = plt.gca()
plt.ylabel('Probability')
ax2.set_xlim(xmin=0.0,xmax=0.3)
f3 = plt.subplot(3,1,3)
n, bins, patches = plt.hist(glow_avail_099_list, 50, normed=1, facecolor='red', alpha=0.75, label='Availability = 0.99')
plt.legend()
ax3 = plt.gca()
ax3.set_xlim(xmin=0.0,xmax=0.3)
plt.xlabel('Data Loss Rate')
plt.show()

f1 = plt.subplot(3,1,1)
n, bins, patches = plt.hist(mwt2_avail_080_list, 50, normed=1, facecolor='green', alpha=0.75, label='Availability = 0.80')
plt.title('Distribution of Data Loss Rate on C23')
ax1 = plt.gca()
ax1.set_xlim(xmin=0.0,xmax=1.0)
f2 = plt.subplot(3,1,2)
n, bins, patches = plt.hist(mwt2_avail_090_list, 50, normed=1, facecolor='blue', alpha=0.75, label='Availability = 0.90')
ax2 = plt.gca()
plt.ylabel('Probability')
ax2.set_xlim(xmin=0.0,xmax=1.0)
f3 = plt.subplot(3,1,3)
n, bins, patches = plt.hist(mwt2_avail_099_list, 50, normed=1, facecolor='red', alpha=0.75, label='Availability = 0.99')
ax3 = plt.gca()
ax3.set_xlim(xmin=0.0,xmax=1.0)
plt.xlabel('Data Loss Rate')
plt.show()
