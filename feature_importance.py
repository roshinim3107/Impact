import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import mutual_info_classif

scaler = MinMaxScaler()

mob_data = pd.read_csv("E:/Covid Hackathon/Global_Mobility_Report.csv") #change path accordingly
mob_data_bool = ((mob_data['country_region'] == 'India'))
mob_data_india = mob_data[mob_data_bool]
mob_data_india = mob_data_india.drop(columns = ['sub_region_2'])
mob_data_india = mob_data_india.dropna()

unique_states = mob_data_india.sub_region_1.unique()
final_df = pd.DataFrame()

for state in unique_states:
	df_bool = mob_data_india['sub_region_1'] == state
	df = mob_data_india[df_bool]
	df = df.iloc[:,4:df.shape[1]]
	mean_vec = df.mean(axis = 0)
	final_df = final_df.append(mean_vec,ignore_index = 'True')

cases1 = [33,3171,2,781,3061,279,369,2,15257,68,15195,1381,273,1921,448,2418,1004,53,7261,56948,44,20,1,4,1593,46,2139,7703,1,18545,2098,230,469,6991,4192]
cases = []
for val in cases1:
	if val < 100:
		cases.append('0')
	elif val > 100 and val < 1000:
		cases.append('1')
	else:
		cases.append('2')

final_df['confirmed cases'] = pd.Series(cases)

x_df = final_df.iloc[:,0:final_df.shape[1]-1]
y_df = final_df.iloc[:,final_df.shape[1] - 1]

x_df = scaler.fit_transform(x_df)
x_df = pd.DataFrame(x_df)
mi_list = mutual_info_classif(x_df,y_df)
print("The mutual information of features in order are:")
print(mi_list)

fig = plt.figure()
labels = ('Retail and Recreation','Grocery and Pharmacy','Parks','Transit stations','Workplaces','Residential')
x_pos = np.arange(len(labels))
values = mi_list
plt.bar(x_pos,values)
plt.xticks(x_pos,labels,rotation = 'vertical')
plt.ylabel('Mutual Information with number of cases')
plt.title('Impact of mobility at different places on number of cases in India')
fig.tight_layout()
plt.savefig('E:/Covid Hackathon/Plots/bar_plot.png')

