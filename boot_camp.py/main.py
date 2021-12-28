import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

%matplotlib inline
flights =pd.read_csv('flights_data.csv')
print(flights.shape)
flights.head()

sb.countplot( data = flights, x= 'Source')
#plt.xticks( rotation = 30)
plt.ylabel_'Number of Flights',fontsize=12)
plt.xlabel('Source',fontsize=12)