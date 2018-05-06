import warnings
import numpy as np
import pandas as pd
import scipy.stats as st
import statsmodels as sm
import matplotlib
import matplotlib.pyplot as plt
import sys
from decimal import Decimal

matplotlib.rcParams['figure.figsize'] = (16.0, 12.0)
matplotlib.style.use('ggplot')

df = pd.read_csv('/Users/zhezhang/Downloads/5labels.csv')
df['Class'] = df['Class'].replace(['Recycle'], 'IdleShutDown')
dist_map = {'johnsonsu':'Johnson SU', 'johnsonsb':'Johnson SB', 'chi':'Chi-Squared', 'uniform':'Uniform', 'norm':'Normal', 'gamma':'Gamma', 'invweibull':'Inverted Weibull', 'exponweib':'Exponential Weibull'}
name_dict = dict()
names = df['ResourceNames'].value_counts().index
index = 0
for name in sorted(names):
	name_dict[name] = 'C'+str(index)
	index += 1

# Create models from data
def best_fit_distribution(data, bins=200, ax=None):
    """Model data by finding best fit distribution to data"""
    # Get histogram of original data
    y, x = np.histogram(data, bins=bins, density=True)
    x = (x + np.roll(x, -1))[:-1] / 2.0

    # Distributions to check
    """   
    DISTRIBUTIONS = [        
        st.alpha,st.anglit,st.arcsine,st.beta,st.betaprime,st.bradford,st.burr,st.cauchy,st.chi,st.chi2,st.cosine,
        st.dgamma,st.dweibull,st.erlang,st.expon,st.exponnorm,st.exponweib,st.exponpow,st.f,st.fatiguelife,st.fisk,
        st.foldcauchy,st.foldnorm,st.frechet_r,st.frechet_l,st.genlogistic,st.genpareto,st.gennorm,st.genexpon,
        st.genextreme,st.gausshyper,st.gamma,st.gengamma,st.genhalflogistic,st.gilbrat,st.gompertz,st.gumbel_r,
        st.gumbel_l,st.halfcauchy,st.halflogistic,st.halfnorm,st.halfgennorm,st.hypsecant,st.invgamma,st.invgauss,
        st.invweibull,st.johnsonsb,st.johnsonsu,st.ksone,st.kstwobign,st.laplace,st.levy,st.levy_l,st.levy_stable,
        st.logistic,st.loggamma,st.loglaplace,st.lognorm,st.lomax,st.maxwell,st.mielke,st.nakagami,st.ncx2,st.ncf,
        st.nct,st.norm,st.pareto,st.pearson3,st.powerlaw,st.powerlognorm,st.powernorm,st.rdist,st.reciprocal,
        st.rayleigh,st.rice,st.recipinvgauss,st.semicircular,st.t,st.triang,st.truncexpon,st.truncnorm,st.tukeylambda,
        st.uniform,st.vonmises,st.vonmises_line,st.wald,st.weibull_min,st.weibull_max,st.wrapcauchy
    ]

    DISTRIBUTIONS = [        
        st.alpha,st.anglit,st.arcsine,st.beta,st.betaprime,st.bradford,st.burr,st.cauchy,st.chi,st.chi2,st.cosine,
        st.dgamma,st.dweibull,st.erlang,st.expon,st.exponnorm,st.exponweib,st.exponpow,st.f,st.fatiguelife,st.fisk,
        st.foldcauchy,st.foldnorm,st.frechet_r,st.frechet_l,st.genlogistic,st.genpareto,st.gennorm,st.genexpon,
        st.genextreme,st.gausshyper,st.gamma,st.gengamma,st.genhalflogistic,st.gilbrat,st.gompertz,st.gumbel_r,
        st.gumbel_l,st.halfcauchy,st.halflogistic,st.halfnorm,st.halfgennorm,st.hypsecant,st.invgamma,st.invgauss,
        st.invweibull,st.johnsonsb,st.johnsonsu,st.kstwobign,st.laplace,st.levy,st.levy_l,st.levy_stable,
        st.logistic,st.loggamma,st.loglaplace,st.lognorm,st.lomax,st.maxwell,st.mielke,st.nakagami,st.ncx2,
        st.norm,st.pareto,st.pearson3,st.powerlaw,st.powerlognorm,st.powernorm,st.rdist,st.reciprocal,
        st.rayleigh,st.rice,st.recipinvgauss,st.semicircular,st.t,st.triang,st.truncexpon,st.truncnorm,
        st.uniform,st.vonmises,st.vonmises_line,st.wald,st.weibull_min,st.weibull_max,st.wrapcauchy
    ]
    """
    DISTRIBUTIONS = [        
        st.norm, st.uniform, st.gamma, st.chi, st.johnsonsu, st.johnsonsb, st.invweibull, st.exponweib
    ]
    dist_dict = {st.johnsonsu:'Johnson SU', st.johnsonsb:'Johnson SB', st.chi:'Chi-Squared', st.uniform:'Uniform', st.norm:'Normal', st.gamma:'Gamma', st.weibull_min:'Weibull Min', st.weibull_max:'Weibull Max', st.invweibull:'Inverted Weibull', st.exponweib:'Exponential Weibull'}
    # Best holders
    best_distribution = st.norm
    best_params = (0.0, 1.0)
    best_sse = np.inf

    # Estimate distribution parameters from data
    for distribution in DISTRIBUTIONS:

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
			dist_label = dist_dict[distribution] + ", SSE=" + str("{:.2E}".format(Decimal(sse)))
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

def make_pdf(dist, params, size=10000):
    """Generate distributions's Propbability Distribution Function """

    # Separate parts of parameters
    arg = params[:-2]
    loc = params[-2]
    scale = params[-1]

    # Get sane start and end points of distribution
    start = dist.ppf(0.01, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.01, loc=loc, scale=scale)
    end = dist.ppf(0.99, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.99, loc=loc, scale=scale)

    # Build PDF and turn into pandas Series
    x = np.linspace(start, end, size)
    y = dist.pdf(x, loc=loc, scale=scale, *arg)
    pdf = pd.Series(y, x)

    return pdf

def distribution_fit(resource, label):
	df_filter = df[(df['ResourceNames']==resource)&(df['Class']==label)]
	data = df_filter[(df_filter.Duration > df_filter.Duration.quantile(0.05))&(df_filter.Duration < df_filter.Duration.quantile(0.95))]['Duration']
	if data.size == 0:
		return
	# Plot for comparison
	ax = data.plot(kind='hist', bins=300, normed=True, alpha=0.5, color=plt.rcParams['axes.color_cycle'][1])
	# Save plot limits
	dataYLim = ax.get_ylim()
	# Find best fit distribution
	best_fit_dist, best_fit_params = best_fit_distribution(data, 300, ax)
	best_dist = getattr(st, best_fit_dist.name)
	# Update plots
	ax.set_ylim(dataYLim)
	title = label + " jobs on the cluster " + name_dict[resource] + ", the best distribution fit is " + dist_map[best_fit_dist.name]
	ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
	ax.tick_params(axis='both', labelsize=18)
	ax.set_title(title, fontsize=18)
	ax.set_xlabel("Duration (Minutes)", fontsize=18)
	ax.set_ylabel("Probability", fontsize=18)
	plt.rc('font', size=18)
	plt.legend(loc='upper right',prop={'size':14})
	plt.tight_layout()
	"""
	# Make PDF
	pdf = make_pdf(best_dist, best_fir_paramms)

	# Display
	plt.figure(figsize=(12,8))
	ax = pdf.plot(lw=2, label='PDF', legend=True)
	data.plot(kind='hist', bins=50, normed=True, alpha=0.5, label='Data', legend=True, ax=ax)

	param_names = (best_dist.shapes + ', loc, scale').split(', ') if best_dist.shapes else ['loc', 'scale']
	param_str = ', '.join(['{}={:0.2f}'.format(k,v) for k,v in zip(param_names, best_fir_paramms)])
	dist_str = '{}({})'.format(best_fit_name, param_str)

	ax.set_title(u'sea temp. with best fit distribution \n' + dist_str)
	ax.set_xlabel(u'Temp.')
	ax.set_ylabel('Frequency')
	"""
	fig = ax.get_figure()
	figure_name = 'duration_' + resource + '_' + label
	figure_name = '/Users/zhezhang/osgparse/figures/' + figure_name
#	fig.savefig(figure_name)
	plt.close(fig)
	return (best_fit_dist, best_fit_params)

#name_list = ['GLOW', 'SU-OG-CE', 'SU-OG-CE1', 'CIT_CMS_T2', 'UConn-OSG', 'SPRACE', 'MWT2', 'MIT_CMS', 'NWICG_NDCMS', 'BU_ATLAS_Tier2', 'uprm-cms', 'IIT_CE1', 'Sandhills', 'WEIZMANN-LCG2', 'AGLT2', 'Crane']
name_list = ['GLOW', 'SU-OG-CE', 'MWT2']
label_list = ['IdleShutDown', 'Retire', 'Kill', 'Preemption', 'NetworkIssue']
"""
for name in name_list:
	for label in label_list:
		distribution_fit(name, label)
"""
total_pdf = None
test_random_variable = st.johnsonsb.rvs(0.38358009181926289, 0.56404652198821881, 302.16538858481425, 1237.5077925073733)
print "test_random_variable = ", test_random_variable
for name in name_list:
	df_name = df[df['ResourceNames']==name]
	x_max = np.max(df_name['Duration'])
	print x_max
	x = range(0, x_max)
	for label in label_list:
		best_fit_dist, best_fit_params = distribution_fit(name, label)
		best_dist = getattr(st, best_fit_dist.name)
		print "best_dist : ", best_dist
		arg = best_fit_params[:-2]
		loc = best_fit_params[-2]
		scale = best_fit_params[-1]
		print "best_fit_dist.name : ", best_fit_dist.name
		print "best_fit_params : ", best_fit_params
		print "arg : ", arg
		print "loc : ", loc
		print "scale : ", scale
		df_label = df_name[df_name['Class']==label]
		pdf = best_fit_dist.pdf(x, *best_fit_params)
		print pdf.shape
		pdf_partial_max = np.max(pdf[pdf < 1.0])
		pdf[pdf >= 1.0] = pdf_partial_max
		print pdf.shape
		print type(pdf)
		if total_pdf is None:
			print float(len(df_label.index)), float(len(df_name.index))
			total_pdf = (pdf * float(len(df_label.index)) / float(len(df_name.index)))
		else:
			print float(len(df_label.index)), float(len(df_name.index))
			total_pdf += (pdf * float(len(df_label.index)) / float(len(df_name.index)))
		print name, label, np.max(total_pdf), np.min(total_pdf)
	pd.Series(total_pdf, x).plot()
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
	total_pdf = None
	plt.tight_layout()
	fig = ax.get_figure()
	figure_name = 'estimation_pdf_' + name
	figure_name = '/Users/zhezhang/osgparse/figures/' + figure_name
	fig.savefig(figure_name)
	plt.close(fig)
	plt.show()
