import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from intervaltree import Interval, IntervalTree
from scheduler import Scheduler
from pdf_fitter import PDF_Fitter
from evaluate import Evaluater
import sys
import random

job_dict = dict()
file_name = '/Users/zhezhang/Downloads/5labels.csv'
df = pd.read_csv(file_name)
pdf_dict = dict()
pdf_fitter = PDF_Fitter(file_name)

#resource_list = ['SU-OG-CE', 'GLOW', 'MWT2', 'BU_ATLAS_Tier2', 'SU-OG-CE1', 'NIKHEF-ELPROD', 'CIT_CMS_T2', 'UConn-OSG', 'AGLT2', 'SPRACE']
#availability_list = ['0.999', '0.99', '0.95', '0.90', '0.80', '0.70', '0.60', '0.50']
#replication_list = ['fast', 'random1copy', 'random2copy', 'random3copy', '1copy']
#lease_list = ['25', '50', '100', '200', '300', '400', '500', '600', '700', '800', '900', '1000', '2000', '3000', '4000', '5000']
resource_list = ['SU-OG-CE', 'GLOW', 'MWT2', 'SPRACE', 'CIT_CMS_T2', 'NIKHEF-ELPROD','UConn-OSG','AGLT2','SU-OG-CE1']
availability_list = ['0.99', '0.95', '0.90', '0.80', '0.70', '0.60', '0.50']
replication_list = ['fast', 'random1copy', 'random2copy', 'random3copy', '1copy']
lease_list = ['25', '50', '100', '200', '400', '800', '1600', '3200']

def cal_loss_redundancy(resource, availability, replication, lease):
	replication_count = 0
	data_loss = 0
	data_count = 100
	data_iterated = 0
	lease_period = int(lease)
	desired_availability = float(availability)
	iteration = 0
	bad_iteration = 0
	while iteration < 30:
		quantile = int(range_minute * 0.05)
		time_point = random.randint(start_minute+quantile, end_minute-quantile)
		job_count = len(interval_tree[time_point])
		# evaluate sizes of data set and job set
		if job_count < data_count * 3:
#			print "Error : job set is less than 3 times of data set"
			bad_iteration += 1
			continue
		availability_dict = dict()
		for data_index in range(data_count):
			data_name = "data" + str(data_index)
			availability_dict[data_name] = desired_availability
		match_job_dict = scheduler.schedule(time_point, lease_period, availability_dict)
		if not match_job_dict:
#			print "Error : match_job_dict is none"
			bad_iteration += 1
			continue
		for job in match_job_dict:
			replication_count += len(match_job_dict[job])
		evaluater = Evaluater(interval_tree, job_dict)
		data_iterated = data_iterated + data_count
		data_loss += evaluater.evaluate(time_point+lease_period, match_job_dict)
		iteration += 1
	data_loss_rate = float(data_loss)/float(data_iterated)
	redundancy_rate = float(replication_count)/float(data_iterated)
	print "data loss rate : ", data_loss_rate
	print "redundancy : ", redundancy_rate
	return (data_loss_rate, redundancy_rate)

result_dict = {}
for resource in resource_list:
	resource_name = resource
	interval_tree = IntervalTree()
	df_resource = df[df['ResourceNames']==resource_name]
	for index, job_info in df_resource.iterrows():
		job_id = job_info['JobId']
		if job_id not in job_dict:
			job_dict[job_id] = []
		start_time = int(job_info['DesktopStartDateMinute'])
		end_time = int(job_info['DesktopEndDateMinute'])
		if start_time == end_time:
			end_time = end_time + 1
			job_info['DesktopEndDateMinute'] = end_time
		job_dict[job_id].append(job_info)
		interval_tree[start_time:end_time] = job_id

	pdf = pdf_fitter.fit(resource_name)
	plt.clf()
	df_name = df[df['ResourceNames']==resource_name]
	start_minute = np.min(df_name['DesktopStartDateMinute'])
	end_minute = np.max(df_name['DesktopEndDateMinute'])
	range_minute = end_minute - start_minute
	x_max = np.max(df_name['Duration'])
	x = range(0, x_max)
	figure_name = resource_name + '_pdf'
	fig = plt.figure()
	pd.Series(pdf, x).plot()
	fig.savefig(figure_name)
	plt.close(fig)
	pdf_dict[resource_name] = pdf
	for availability in availability_list:
		for replication in replication_list:
			matching_algorithm = replication
			scheduler = Scheduler(job_dict, pdf_dict, interval_tree, matching_algorithm)
			for lease in lease_list:
				name = resource + '_availability_' + availability + '_replication_' + replication + '_lease_' + lease
				value = cal_loss_redundancy(resource, availability, replication, lease)
				result_dict[name] = value
		fname = resource + '_' + availability + '.txt'
		with open(fname, 'wb') as fp:
			pickle.dump(result_dict, fp, protocol=pickle.HIGHEST_PROTOCOL)
		fp.close()

with open('replication_model_result.txt', 'wb') as fp:
	pickle.dump(result_dict, fp, protocol=pickle.HIGHEST_PROTOCOL)
fp.close()

#resource_dict = {'SU-OG-CE':'suogce', 'GLOW':'glow', 'MWT2':'mwt2'}
#avail_dict = {'0.99':'099', '0.90':'090', '0.80':'080'}
#file_name = resource_dict[sys.argv[1]] + '_avail_' + avail_dict[sys.argv[2]] + '_replication_' + sys.argv[3] + '_lease_' + sys.argv[4] + '.txt'
#print file_name
#with open(file_name, 'wb') as fp:
#	pickle.dump(loss_rate_list, fp)

