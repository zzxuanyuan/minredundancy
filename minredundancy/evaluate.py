import numpy as np

class Evaluater:
	def __init__(self, interval_tree, job_dict):
		self.interval_tree = interval_tree
		self.job_dict = job_dict

	def evaluate(self, evaluate_time, match_job_dict):
		tree_job_list = self.interval_tree[evaluate_time]
		tree_job_dict = {}
		tree_job_set = set()
		for interval in tree_job_list:
			tree_job_dict[interval[2]] = interval
			tree_job_set.add(interval[2])
		data_loss = 0
		for data in match_job_dict:
			data_job_set = set()
			data_job_dict = {}
			for tup in match_job_dict[data]:
				if type(tup) is int:
					print "data : ", data, "tup : ", tup
					print match_job_dict
				data_job_set.add(tup[2])
				data_job_dict[tup[2]] = tup
			intersect_set = data_job_set.intersection(tree_job_set)
			if not intersect_set:
				data_loss = data_loss + 1
				continue
			# verify if the job from two sets were starting and ending at the same time
			same_start_end = False
			for job in intersect_set:
				job_tup = tree_job_dict[job]
				data_tup = data_job_dict[job]
				if data_tup[0] == job_tup[0] and data_tup[1] == job_tup[1]:
					same_start_end = True
					break
			if same_start_end == False:
				data_loss = data_loss + 1
		return data_loss

			
