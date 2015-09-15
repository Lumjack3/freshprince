import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import numpy as np

#Single Factor
loansData1 = pd.read_csv('C:\Users\Vladimir\Anaconda\Lib\site-packages\spyderlib\images\projects\Thinkful\LoanStats3a.csv', low_memory=False) 
loansData1['ir2'] = loansData1['int_rate'].replace('%', "", regex=True).astype('float')/100
x = loansData1.dropna(subset = ['annual_inc', 'ir2'])
AnIn = x['annual_inc']
x2 = np.matrix(AnIn).transpose()
x3 = sm.add_constant(x2)
inra = x['ir2']
y = np.matrix(inra).transpose()
x4 = sm.add_constant(x3)
model = sm.OLS(y,x4)
f = model.fit()
print "One Factor Regression: "
print f.summary()

#Multi Factor
def convHO(c):
    if c == "OWN":
        return 1
    else:
        return 0
        

loansData1 = pd.read_csv('C:\Users\Vladimir\Anaconda\Lib\site-packages\spyderlib\images\projects\Thinkful\LoanStats3a.csv', low_memory=False) 
loansData1['ir2'] = loansData1['int_rate'].replace('%', "", regex=True).astype('float')/100
loansData1['HO2'] = map(convHO, loansData1['home_ownership'])
x = loansData1.dropna(subset = ['annual_inc', 'ir2','HO2'])
AnIn = x['annual_inc']
HoOw = x['HO2']                        
x2 = np.matrix(AnIn).transpose()
x2b = np.matrix(HoOw).transpose()
x2c = np.column_stack([x2,x2b])
x3 = sm.add_constant(x2c)
inra = x['ir2']
y = np.matrix(inra).transpose()
x4 = sm.add_constant(x3)
model = sm.OLS(y,x4)
f = model.fit()
print "\n Multi-Factor Regression: "
print f.summary()
