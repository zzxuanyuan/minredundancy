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
resource_name = sys.argv[1]

df = pd.read_csv(file_name)

interval_tree = IntervalTree()
df_resource = df[df['ResourceNames']==resource_name]
for index, job_info in df_resource.iterrows():
	job_id = job_info['JobId']
	job_dict[job_id] = job_info
	start_time = int(job_info['DesktopStartDateMinute'])
	end_time = int(job_info['DesktopEndDateMinute'])
	if start_time == end_time:
		end_time = end_time + 1
	interval_tree[start_time:end_time] = job_id

pdf_dict = dict()
pdf_fitter = PDF_Fitter(file_name)
pdf = pdf_fitter.fit(resource_name)
print "pdf shape = ", pdf.shape

plt.clf()
df_name = df[df['ResourceNames']==resource_name]
x_max = np.max(df_name['Duration'])
print "x_max = ", x_max
x = range(0, x_max)
pd.Series(pdf, x).plot()
plt.show()

pdf_dict[resource_name] = pdf
matching_algorithm = sys.argv[3]
scheduler = Scheduler(job_dict, pdf_dict, interval_tree, matching_algorithm)

start_minute = np.min(df_name['DesktopStartDateMinute'])
end_minute = np.max(df_name['DesktopEndDateMinute'])
range_minute = end_minute - start_minute

loss_rate_list = []
for run in range(1):
	data_loss = 0
	data_count = 100
	data_iterated = 0
	lease_period = int(sys.argv[4])
	desired_availability = float(sys.argv[2])
	iteration = 0
	bad_iteration = 0
	while iteration < 10:
		quantile = int(range_minute * 0.05)
#		print "quantile is : ", quantile
		time_point = random.randint(start_minute+quantile, end_minute-quantile)
#		print "time_point is : ", time_point
		job_count = len(interval_tree[time_point])
		# evaluate sizes of data set and job set
		if job_count < data_count * 3:
			print "Error : job set is less than 3 times of data set"
			bad_iteration += 1
			continue
		availability_dict = dict()
		for data_index in range(data_count):
			data_name = "data" + str(data_index)
			availability_dict[data_name] = desired_availability
#		print availability_dict
		match_job_dict = scheduler.schedule(time_point, lease_period, availability_dict)
		if not match_job_dict:
			print "Error : match_job_dict is none"
			bad_iteration += 1
			continue
#		for job in match_job_dict:
#			print job, match_job_dict[job]
		evaluater = Evaluater(interval_tree, job_dict)
		data_iterated = data_iterated + data_count
		data_loss += evaluater.evaluate(time_point+lease_period, match_job_dict)
		iteration += 1
	print "data_loss : ", data_loss
	print "data_iterated : ", data_iterated
	print "iteration, bad_iteration : ", iteration, bad_iteration
	loss_rate_list.append(float(data_loss)/float(data_iterated))
	print loss_rate_list
print loss_rate_list

resource_dict = {'SU-OG-CE':'suogce', 'GLOW':'glow', 'MWT2':'mwt2'}
avail_dict = {'0.99':'099', '0.90':'090', '0.80':'080'}
file_name = resource_dict[sys.argv[1]] + '_avail_' + avail_dict[sys.argv[2]] + '_replication_' + sys.argv[3] + '_lease_' + sys.argv[4] + '.txt'
print file_name
with open(file_name, 'wb') as fp:
	pickle.dump(loss_rate_list, fp)

