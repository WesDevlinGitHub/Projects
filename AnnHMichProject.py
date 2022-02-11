import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd
import matplotlib.animation as mpla
import numpy as np
# Read in CSV File
df = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')
# Begin understanding and organizing data.
df.sort_values(["ID"], axis=0, ascending=[True], inplace=True)
df.sort_values(["Date"], axis=0, ascending=[True], inplace=True)
# Drop leap years
i = df[(df.Date == '2008-02-29')].index
new_df = df.drop(i)
l = new_df[(new_df.Date == '2012-02-29')].index
neww_df = new_df.drop(l)
#Convert Date column to DT Object
neww_df['Date']= pd.to_datetime(df['Date'])
#Select Only the years 2005 - 2014
filtered_df = neww_df.loc[(neww_df['Date'] >= '2005-01-01') & (neww_df['Date'] <= '2014-12-31')]
data_values = filtered_df.groupby('Date').agg({'Data_Value': ['min', 'max']})
date_min_max = data_values.reset_index()
x = date_min_max['Date']
y_max = date_min_max['Data_Value','max'].max()
y_min = date_min_max['Data_Value','max'].min()

new_date_min_max = date_min_max.T.reset_index(drop=True).T
new_date_min_max.columns = ['Date', 'Min', 'Max']

new_date_min_max['day'] = new_date_min_max['Date'].dt.day
new_date_min_max['month'] = new_date_min_max['Date'].dt.month
new_date_min_max['year'] = new_date_min_max['Date'].dt.year

grouped_df = new_date_min_max.groupby(['day','month','year']).Min.min()
grouped_df_max = new_date_min_max.groupby(['day','month','year']).Max.max()

final_min = grouped_df.unstack()
final_max = grouped_df_max.unstack()

final_min['Min_Temp_Per_Day'] = final_min.min(axis = 1)
final_max['Max_Temp_Per_Day'] = final_max.max(axis = 1)

final_max = final_max.drop(final_max.columns[[0,1, 2,3,4,5,6,7,8,9]], axis=1)
final_min = final_min.drop(final_min.columns[[0,1, 2,3,4,5,6,7,8,9]], axis=1)

final_max['Max_Temp_Per_Day'] = final_max['Max_Temp_Per_Day'].div(10, axis = 0)
final_min['Min_Temp_Per_Day'] = final_min['Min_Temp_Per_Day'].div(10, axis = 0)

f_max_r = final_max.reset_index()
f_min_r = final_min.reset_index()

f_max_index = f_max_r.index
f_min_index = f_min_r.index

f_max_dfinal = f_max_r.sort_values(by = ['month','day'], ascending = True).reset_index()
f_min_dfinal = f_min_r.sort_values(by = ['month','day'], ascending = True).reset_index()

f_max_final = f_max_dfinal.drop(f_max_dfinal.columns[[0,1,2]], axis = 1)
f_min_final = f_min_dfinal.drop(f_max_dfinal.columns[[0,1,2]], axis = 1)

f_max_final_index = f_max_final.index
f_min_final_index = f_min_final.index
#Filtering 2015 Data
filtered_df2015 = neww_df.loc[(neww_df['Date'] >= '2015-01-01') & (neww_df['Date'] <= '2015-12-31')]
filtered_df2015_values = filtered_df2015.groupby('Date').agg({'Data_Value': ['min', 'max']})

df2015_r = filtered_df2015_values.reset_index()
top_date_min_max = df2015_r.T.reset_index(drop=True).T
top_date_min_max.columns = ['Date', 'Min', 'Max']

top_date_min_max['day'] = top_date_min_max['Date'].dt.day
top_date_min_max['month'] = top_date_min_max['Date'].dt.month
top_date_min_max['year'] = top_date_min_max['Date'].dt.year

top_date_min_max = top_date_min_max.drop(top_date_min_max.columns[[0,3,4,5]], axis=1)
top_date_min_max['Min'] = top_date_min_max['Min'].div(10,axis = 0)
top_date_min_max['Max'] = top_date_min_max['Max'].div(10,axis = 0)

top_date_min_max_index = top_date_min_max.index
f_min_final['2015_Min_Temps'] = top_date_min_max['Min']
f_max_final['2015_Max_Temps'] = top_date_min_max['Max']

f_max_final['Higher_Temp'] = np.where(f_max_final['2015_Max_Temps'] > f_max_final['Max_Temp_Per_Day'], f_max_final['2015_Max_Temps'], np.nan)
Highest_Temp = f_max_final.drop(f_max_final.columns[[0,1]], axis=1)
Highest_Temp.dropna(subset = ["higher_Temp"], inplace=True)
Highest_Temp_Index = Highest_Temp.index

f_min_final['Lower_Temp'] = np.where(f_min_final['2015_Min_Temps'] < f_min_final['Min_Temp_Per_Day'], f_min_final['2015_Min_Temps'], np.nan)
Lowest_Temp = f_min_final.drop(f_min_final.columns[[0,1]], axis=1)
Lowest_Temp.dropna(subset = ["Lower_Temp"], inplace=True)
Lowest_Temp_Index = Lowest_Temp.index

f_min_FINAL = f_min_final.drop(f_min_final.columns[[1,2]], axis=1)
f_max_FINAL = f_max_final.drop(f_max_final.columns[[1,2]], axis=1)
esult = pd.concat([f_max_FINAL, f_min_FINAL], axis=1, join="inner")
df3 = Lowest_Temp.reset_index()
f4 = Highest_Temp.reset_index()
f2 = result.reset_index()

#Plot line graphs showing max/min temps in Ann Arbor Michigan between 2004 and 2015
#Create a scatter plot which shows days throughout the year 2015 where the max/min temps were higher.
plt.scatter(df3['index'], df3['Lower_Temp'], color = 'blue', label = '2015 Temperatures Lower than last 10 Years')
plt.scatter(df4['index'], df4['higher_Temp'], color = 'red', label = '2015 Temperatures Higher than last 10 Years')

plt.xlabel('365 Day Calender Year')
plt.ylabel('Temperature in Celcius')

plt.title('Ann Arbor, Michigan Highest and Lowest Temperature Between 2005 and 2014')

plt.suptitle('Current Year, 2015')

plt.style.use("seaborn")

plt.plot(df2["index"], df2[["Max_Temp_Per_Day", "Min_Temp_Per_Day"]], color = 'gray', alpha = 0.5)
plt.fill_between(x = df2["index"], y1 = df2["Max_Temp_Per_Day"], y2 = df2["Min_Temp_Per_Day"], color = 'gray', label = '2005-2014 Max/Min Temperatures', alpha = 0.50)
plt.legend()
plt.show()
