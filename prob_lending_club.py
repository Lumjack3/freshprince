import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats


loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')
loansData.dropna(inplace=True)

plt.figure()
loansData.boxplot(column = 'Amount.Requested')
plt.savefig('LendingClubBoxPlot.png')

plt.figure()
loansData.hist(column='Amount.Requested')
plt.savefig('LendingClubHistogram.png')

plt.figure()
graph = stats.probplot(loansData['Amount.Requested'], dist="norm", plot=plt)
plt.savefig('LeningClubQQ.png')

