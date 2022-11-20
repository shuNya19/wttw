import pandas as pd
import numpy as np
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def convert(i):
	try:
		h,m = i.split(' ')
	except:
		m = i
		h = '0h'
	m = m[:-3]
	h = h[:-1]
	res = int(h)*60+int(m)
	return res

def splitting(i):
	try:
		y = list(i.split(' '))[2]
		y = int(y)
		return y
	except:
		return int(i)

df = pd.read_csv('data/data.csv', encoding = 'cp1251')
#df['Duration'] = [convert(i) for i in df['Duration'].to_list()]
#df['Aired'] = [i.split(' (')[0] for i in df['Aired'].to_list()]
#df.to_csv('data.txt', index = False, encoding = 'cp1251')
#df['Aired'] = [splitting(i) for i in df['Aired']]
df['MyRate'] = [np.nan for i in df['Aired']]
df.to_csv('data.txt', index = False, encoding = 'cp1251')
#print(max(['Aired']), min(df['Aired']))