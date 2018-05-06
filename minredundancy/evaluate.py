import numpy as np

class Evaluater:
	def __init__(self, interval_tree, job_dict):
		self.interval_tree = interval_tree
		self.job_dict = job_dict

	def evaluate(self, evaluate_time, match_job_dict):
		tree_job_list = self.interval_tree[evaluate_time]
		tree_job_set = set()
		for interval in tree_job_list:
			tree_job_set.add(interval[2])
#		print "tree_job_set is as follows:"
#		print len(tree_job_set)
		data_loss = 0
		for data in match_job_dict:
			data_job_set = set(match_job_dict[data])
			intersect_set = data_job_set.intersection(tree_job_set)
#			print intersect_set
			if not intersect_set:
#				print "intersect_set is empty"
				data_loss = data_loss + 1
		return data_loss

			
