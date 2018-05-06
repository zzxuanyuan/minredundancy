import pandas as pd
from intervaltree import Interval, IntervalTree
import sys
import warnings
import numpy as np
import scipy.stats as st
import statsmodels as sm
import matplotlib
import matplotlib.pyplot as plt
from decimal import Decimal

class PDF_Fitter:
	def __init__(self, file_name):
		self.file_name = file_name
		self.df = pd.read_csv(file_name)
		self.label_list = ['Recycle', 'Retire', 'Kill', 'Preemption', 'NetworkIssue']
		# Distributions to check
		self.distribution_list = [        
        		st.norm, st.uniform, st.gamma, st.chi, st.johnsonsu, st.johnsonsb, st.invweibull, st.exponweib
    		]
    		self.dist_dict = {st.johnsonsu:'Johnson SU', st.johnsonsb:'Johnson SB', st.chi:'Chi-Squared', st.uniform:'Uniform', st.norm:'Normal', st.gamma:'Gamma', st.weibull_min:'Weibull Min', st.weibull_max:'Weibull Max', st.invweibull:'Inverted Weibull', st.exponweib:'Exponential Weibull'}
		self.name_dict = dict()
		names = self.df['ResourceNames'].value_counts().index
		index = 0
		for name in sorted(names):
			self.name_dict[name] = 'C'+str(index)
			index += 1
		self.pdf_dict = dict()

	def fit(self, resource_name):
		df_name = self.df[self.df['ResourceNames']==resource_name]
		x_max = np.max(df_name['Duration'])
		x = range(0, x_max)
		total_pdf = None
		for label in self.label_list:
			best_fit_dist, best_fit_params = self._distribution_fit(resource_name, label)
			best_dist = getattr(st, best_fit_dist.name)
#			print "best_dist : ", best_dist
			arg = best_fit_params[:-2]
			loc = best_fit_params[-2]
			scale = best_fit_params[-1]
#			print "best_fit_dist.name : ", best_fit_dist.name
#			print "best_fit_params : ", best_fit_params
#			print "arg : ", arg
#			print "loc : ", loc
#			print "scale : ", scale
			df_label = df_name[df_name['Class']==label]
			pdf = best_fit_dist.pdf(x, *best_fit_params)
#			print pdf.shape
			pdf_partial_max = np.max(pdf[pdf < 1.0])
			pdf[pdf >= 1.0] = pdf_partial_max
			if total_pdf is None:
				total_pdf = (pdf * float(len(df_label.index)) / float(len(df_name.index)))
			else:
				total_pdf += (pdf * float(len(df_label.index)) / float(len(df_name.index)))
		pd.Series(total_pdf, x).plot()
		"""
		data = df_name['Duration']
		# Plot for comparison
		ax = data.plot(kind='hist', bins=300, normed=True, alpha=0.5, color=plt.rcParams['axes.color_cycle'][1])
		ax.set_ylim(ymin=0)
		ax.set_xlim(xmin=0, xmax=230000)
		ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
		ax.tick_params(axis='both', labelsize=28)
		ax.set_xlabel("Duration (Minutes)", fontsize=28)
		ax.set_ylabel("Probability", fontsize=28)
		y, x = np.histogram(data, bins=x_max, density=True)
		sse = np.sum(np.power(y - total_pdf, 2.0))
		print sse
		plt.show()
		"""
		self.pdf_dict[resource_name] = total_pdf
		return total_pdf

	def _distribution_fit(self, resource, label):
		print resource, label
		df_filter = self.df[(self.df['ResourceNames']==resource)&(self.df['Class']==label)]
		data = df_filter[(df_filter.Duration > df_filter.Duration.quantile(0.05))&(df_filter.Duration < df_filter.Duration.quantile(0.95))]['Duration']
		if data.size == 0:
			return
		# Plot for comparison
		ax = data.plot(kind='hist', bins=300, normed=True, alpha=0.5, color=plt.rcParams['axes.color_cycle'][1])
		# Save plot limits
		dataYLim = ax.get_ylim()
		# Find best fit distribution
		best_fit_dist, best_fit_params = self._best_fit_distribution(data, 300, ax)
		"""
		best_dist = getattr(st, best_fit_dist.name)
		# Update plots
		ax.set_ylim(dataYLim)
		title = label + " jobs on the cluster " + resource + ", the best distribution fit is " + best_fit_dist.name
		ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
		ax.tick_params(axis='both', labelsize=18)
		ax.set_title(title, fontsize=18)
		ax.set_xlabel("Duration (Minutes)", fontsize=18)
		ax.set_ylabel("Probability", fontsize=18)
		plt.rc('font', size=18)
		plt.legend(loc='upper right',prop={'size':14})
		plt.tight_layout()
		plt.show()
		"""
		return (best_fit_dist, best_fit_params)

	# Create models from data
	def _best_fit_distribution(self, data, bins=200, ax=None):
	    """Model data by finding best fit distribution to data"""
	    # Get histogram of original data
	    y, x = np.histogram(data, bins=bins, density=True)
	    x = (x + np.roll(x, -1))[:-1] / 2.0

	    # Best holders
	    best_distribution = st.norm
	    best_params = (0.0, 1.0)
	    best_sse = np.inf

	    # Estimate distribution parameters from data
	    for distribution in self.distribution_list:

		# Try to fit the distribution
		try:
		    # Ignore warnings from data that can't be fit
		    with warnings.catch_warnings():
			warnings.filterwarnings('ignore')

			# fit dist to data
			params = distribution.fit(data)
			# Separate parts of parameters
			arg = params[:-2]
			loc = params[-2]
			scale = params[-1]

			# Calculate fitted PDF and error with fit in distribution
			pdf = distribution.pdf(x, loc=loc, scale=scale, *arg)
			sse = np.sum(np.power(y - pdf, 2.0))
			# if axis pass in add to plot
			try:
			    if ax:
	#			dist_label = dist_dict[distribution] + ", SSE=" + sse
				test = "{:.2E}".format(Decimal('40800000000.00000000000000'))
				test = "{:.2E}".format(sse)
				dist_label = self.dist_dict[distribution] + ", SSE=" + str("{:.2E}".format(Decimal(sse)))
				pd.Series(pdf, x).plot(ax=ax, legend=True, label=dist_label)
			    end
			except Exception:
			    pass

			# identify if this distribution is better
			if best_sse > sse > 0:
			    best_distribution = distribution
			    best_params = params
			    best_sse = sse

		except Exception:
		    pass

	    return (best_distribution, best_params)
