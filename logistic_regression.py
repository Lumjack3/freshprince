import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import numpy as np
from math import exp

def conv(a):
	return min(map(int, a.split('-')))

def convIR(b):
	return float(b[:len(b)-1])

def convMths(c):
	return int(c[:len(c)- 7])

def convIRTF(d):
	if d < 12:
		return 0
	else:
		return 1

def logistic_function(FS_Coeff, LA_Coeff, Int_Coeff, FiSc, LoAm):
	p = 1/(1+ exp(Int_Coeff + FS_Coeff * FiSc - LA_Coeff * LoAm))
	return p

loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')
loansData.dropna(inplace=True)
#loansData.to_csv('loansData_clean.csv', header=True, index=False)

#Clean Fico Score Data
loansData['Fico2'] = map(conv, loansData['FICO.Range'])

#Clean Interest Rate
loansData['Interest.Rate2'] = map(convIR, loansData['Interest.Rate'])

#Cleans loan length dataanalysis
loansData['Loan.Length2'] = map(convMths, loansData['Loan.Length'])

#New Column for if int rate is above or below 12%
loansData['IR_TF'] = map(convIRTF, loansData['Interest.Rate2'])

#Constant intercept column
loansData['Constant'] = 1

intrate = loansData['Interest.Rate2']
loanamt = loansData['Amount.Requested']
fico = loansData['Fico2']

# The dependent variable
y = np.matrix(intrate).transpose()
# The independent variables shaped as columns
x1 = np.matrix(fico).transpose()
x2 = np.matrix(loanamt).transpose()

indvars = np.column_stack([x1,x2, loansData['Constant']])
logit = sm.Logit(loansData['IR_TF'], indvars)
result = logit.fit()
FS_Coeff = result.params[0]
LA_Coeff = result.params[1]
Int_Coeff = result.params[2]
FiSc = input('Enter FICO Score: ')
LoAm = input('Enter Loan Amount: ')

Pred = logistic_function(FS_Coeff, LA_Coeff, Int_Coeff, FiSc, LoAm)
print Pred