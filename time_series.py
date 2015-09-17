import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import numpy as np

df = pd.read_csv('C:\Users\Vladimir\Anaconda\Lib\site-packages\spyderlib\images\projects\Thinkful\LoanStats3b.csv', low_memory=False, skiprows=[0]) 
df['issue_d_format'] = pd.to_datetime(df['issue_d']) 
dfts = df.set_index('issue_d_format') 
year_month_summary = dfts.groupby(lambda x : x.year * 100 + x.month).count()
loan_count_summary = year_month_summary['issue_d']

#Normal Plot
print "Monthly Summary Count:"
print "ACF PLOT:"
fig = plt.figure()
fig = sm.graphics.tsa.plot_acf(loan_count_summary)
fig = plt.show()

print "PACF PLOT:"
fig = plt.figure()
fig = sm.graphics.tsa.plot_pacf(loan_count_summary)
fig = plt.show()

#Differences plots
print "Differences Plot:"
loandiff = np.diff(loan_count_summary)
fig = plt.figure()
fig = sm.graphics.tsa.plot_acf(loandiff)
fig = plt.show()

print "Differences PACF PLOT:"
fig = plt.figure()
fig = sm.graphics.tsa.plot_pacf(loandiff)
fig = plt.show()

print "There are autocorrelated structures in this data."