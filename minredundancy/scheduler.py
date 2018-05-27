import pandas as pd
import numpy as np
from intervaltree import Interval, IntervalTree
import sys

class Scheduler:
	def __init__(self, job_dict, pdf_dict, interval_tree, matching_algorithm):
		self.job_dict = job_dict
		self.pdf_dict = pdf_dict
		self.interval_tree = interval_tree
		self.algorithm = matching_algorithm

	def schedule(self, time_point, lease_period, availability_dict):
		job_list = self.interval_tree[time_point]
		print "time_point = ", time_point
		print "job_list = ", job_list
		failure_rate_dict = {}
		for job in job_list:
			job_id = job[2]
			job_info = self.job_dict[job_id]
			failure_rate_dict[job_id] = self._to_failure_rate(job_info, time_point, lease_period)
		# evalute sizes of data set and job set
		acceptable_failure_rate_count = 0
		for job in failure_rate_dict:
			if failure_rate_dict[job] < 1.0:
				acceptable_failure_rate_count = acceptable_failure_rate_count + 1
		if acceptable_failure_rate_count < len(availability_dict) * 3:
			print "Error: there are less than 3 times of jobs that are acceptable"
			return None

		match_job_dict = self.negotiate(availability_dict, failure_rate_dict)
		return match_job_dict

	def negotiate(self, availability_dict, failure_rate_dict):
		return self._do_negotiate(availability_dict, failure_rate_dict, self.algorithm)

	def _do_negotiate(self, availability_dict, failure_rate_dict, algorithm):
		if algorithm == "fast":
			return self._do_fast_negotiate(availability_dict, failure_rate_dict)
		elif algorithm == "1copy":
			return self._do_1copy_negotiate(availability_dict, failure_rate_dict)
		elif algorithm == "random1copy":
			return self._do_random1copy_negotiate(availability_dict, failure_rate_dict)
		elif algorithm == "random2copy":
			return self._do_random2copy_negotiate(availability_dict, failure_rate_dict)
		elif algorithm == "random3copy":
			return self._do_random3copy_negotiate(availability_dict, failure_rate_dict)

	def _do_random3copy_negotiate(self, availability_dict, failure_rate_dict):
		match_job_dict = {}
		for dataset in availability_dict:
			job_list = []
			if not failure_rate_dict:
				return None
			job_id, rate = failure_rate_dict.popitem()
			job_list.append(job_id)
			if not failure_rate_dict:
				return None
			job_id, rate = failure_rate_dict.popitem()
			job_list.append(job_id)
			if not failure_rate_dict:
				return None
			job_id, rate = failure_rate_dict.popitem()
			job_list.append(job_id)
			match_job_dict[dataset] = job_list
		return match_job_dict

	def _do_random2copy_negotiate(self, availability_dict, failure_rate_dict):
		match_job_dict = {}
		for dataset in availability_dict:
			job_list = []
			if not failure_rate_dict:
				return None
			job_id, rate = failure_rate_dict.popitem()
			job_list.append(job_id)
			if not failure_rate_dict:
				return None
			job_id, rate = failure_rate_dict.popitem()
			job_list.append(job_id)
			match_job_dict[dataset] = job_list
		return match_job_dict

	def _do_random1copy_negotiate(self, availability_dict, failure_rate_dict):
		match_job_dict = {}
		for dataset in availability_dict:
			job_list = []
			if not failure_rate_dict:
				return None
			job_id, rate = failure_rate_dict.popitem()
			job_list.append(job_id)
			match_job_dict[dataset] = job_list
		return match_job_dict

	def _do_1copy_negotiate(self, availability_dict, failure_rate_dict):
		match_job_dict = {}
		for dataset in availability_dict:
			required_availability = availability_dict[dataset]
			find = False
			for job_id in failure_rate_dict:
				if failure_rate_dict[job_id] < 1.0 - required_availability:
					rate = failure_rate_dict.pop(job_id, None)
					if rate == None:
						print "Error: rate is None"
						return None
					find = True
					match_job_dict[dataset] = [job_id]
					break
			if find == False:
				print "Error: does not find a pilot job which meets required availability"
			if dataset not in match_job_dict:
				print "Error: ", dataset, " is not in match_job_dict"
				return None
		return match_job_dict

	def _do_fast_negotiate(self, availability_dict, failure_rate_dict):
		match_job_dict = {}
		for dataset in availability_dict:
			required_availability = availability_dict[dataset]
			job_list = []
			accu_failure_rate = 1.0
			accu_availability = 0.0
			while required_availability > accu_availability:
				if not failure_rate_dict:
					return None
				job_id, rate = failure_rate_dict.popitem()
				if rate >= 1.0:
					continue
				job_list.append(job_id)
				accu_failure_rate = accu_failure_rate * rate
				accu_availability = 1.0 - accu_failure_rate
			match_job_dict[dataset] = job_list
		return match_job_dict

	def _to_failure_rate(self, job_info, time_point, release_period):
		resource_name = job_info['ResourceNames']
		pdf = self.pdf_dict[resource_name]
		# calculate conditional probability
		job_initial_time = int(job_info['DesktopStartDateMinute'])
		start_time = time_point - job_initial_time
		end_time = start_time + release_period
		# the integral of range [start_time, end_time); since the step = 1, so the area of integration is height which is represented by pdf[point] multiplied by length which is step size 1
		p_nominator = np.sum(pdf[start_time:end_time])
		p_denominator = np.sum(pdf[start_time:])
		failure_rate = p_nominator/p_denominator
		print "time_point, p_nominator,p_denominator,failure_rate,job_initial_time,start_time,end_time,job_id = ", time_point,p_nominator,p_denominator,failure_rate,job_initial_time,start_time,end_time,job_info['JobId']
		return failure_rate

