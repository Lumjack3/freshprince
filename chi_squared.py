import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats
import collections

loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')
loansData.dropna(inplace=True)

freq = collections.Counter(loansData['Open.CREDIT.Lines'])

chi, p = stats.chisquare(freq.values())
print "CHI: " + str(chi)
print "p: " + str(p)