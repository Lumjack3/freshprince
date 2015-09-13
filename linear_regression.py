import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import numpy as np


def conv(a):
	return min(map(int, a.split('-')))

def convIR(b):
	return float(b[:len(b)-1])

def convMths(c):
	return int(c[:len(c)- 7])

loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')
loansData.dropna(inplace=True)

#Clean Fico Score Data
loansData['Fico2'] = map(conv, loansData['FICO.Range'])

#Clean Interest Rate
loansData['Interest.Rate2'] = map(convIR, loansData['Interest.Rate'])

#Cleans loan length dataanalysis
loansData['Loan.Length2'] = map(convMths, loansData['Loan.Length'])

intrate = loansData['Interest.Rate2']
loanamt = loansData['Amount.Requested']
fico = loansData['Fico2']

# The dependent variable
y = np.matrix(intrate).transpose()
# The independent variables shaped as columns
x1 = np.matrix(fico).transpose()
x2 = np.matrix(loanamt).transpose()

x = np.column_stack([x1,x2])
X = sm.add_constant(x)
model = sm.OLS(y,X)
f = model.fit()
print f.summary()