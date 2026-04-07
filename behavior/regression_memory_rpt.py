import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats

path = 'file_directory/'
dprime = pd.read_csv(path + 'behavior/sdt_results.csv')

powtype = 'total_encoding', 'total_recall'
memory_measure = 'd_all', 'beta_all'

regData = dprime.groupby(['subject'], as_index=False).mean()

encoding_rpt = pd.read_csv(path + 'tf/encoding_hitmiss_total_long_100600_max.csv')
encoding_rpt = encoding_rpt[(encoding_rpt['channel'].isin(chans)) & (encoding_rpt['frequency'] == band) & (encoding_rpt['subject'].isin(subs))]
encoding_rpt = encoding_rpt.groupby(['subject', 'reactionType'], as_index=False).mean()[['subject', 'reactionType', measure]]

recall_rpt = pd.read_csv(path + 'tf/recall_total_long_100600_max.csv')
recall_rpt = recall_rpt[recall_rpt['channel'].isin(chans) & (recall_rpt['frequency'] == band) & (recall_rpt['subject'].isin(subs))]
recall_rpt = recall_rpt.groupby(['subject', 'reactionType'], as_index=False).mean()[['subject', 'reactionType', measure]]

regData['total_encoding'] = data1.groupby(['subject'], as_index=False).mean()['peak'].reset_index(drop=True)
regData['total_recall'] = data2.groupby(['subject'], as_index=False).mean()['peak'].reset_index(drop=True)

regData['d_all'] = stats.zscore(regData['d_all'])
regData['beta_all'] = stats.zscore(regData['beta_all'])

regData['total_encoding'] = stats.zscore(regData['total_encoding'])
regData['total_recall'] = stats.zscore(regData['total_recall'])

md = smf.glm("d_all ~ total_encoding", regData)
mdf = md.fit()
print(mdf.summary())

md = smf.glm("beta_all ~ total_encoding", regData)

mdf = md.fit()
print(mdf.summary())

md = smf.glm("d_all ~ total_recall", regData)

mdf = md.fit()
print(mdf.summary())

md = smf.glm("beta_all ~ total_recall", regData)

mdf = md.fit()
print(mdf.summary())
