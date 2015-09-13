import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats
import collections

loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')
loansData.dropna(inplace=True)

freq = collections.Counter(loansData['State'])
plt.bar(range(len(freq.values())), sorted(freq.values()), align = 'center')
plt.xticks(range(len(freq.values())), sorted(freq, key=freq.get), size= 'small')
plt.show()

