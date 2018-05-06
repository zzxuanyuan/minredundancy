import pickle
import sys

with open (sys.argv[1], 'rb') as fp:
	itemlist = pickle.load(fp)
print itemlist
