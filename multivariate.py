import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import numpy as np


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
print f.summary()