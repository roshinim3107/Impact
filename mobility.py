import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import datetime
from matplotlib.font_manager import FontProperties

fontP = FontProperties()
fontP.set_size('small')

mobility_type = ['retail_and_recreation_percent_change_from_baseline','grocery_and_pharmacy_percent_change_from_baseline','parks_percent_change_from_baseline','transit_stations_percent_change_from_baseline','workplaces_percent_change_from_baseline','residential_percent_change_from_baseline']
states = ['Andhra Pradesh','Delhi','Karnataka','Maharashtra','Tamil Nadu']

		
for state in states:
	mob_data = pd.read_csv("E:/Covid Hackathon/Global_Mobility_Report.csv") #change path accordingly
	mob_data_bool = ((mob_data['country_region'] == 'India') & (mob_data['sub_region_1'] == state))
	mob_data_india = mob_data[mob_data_bool]
	mob_data_india = mob_data_india.drop(columns = ['sub_region_2'])
	mob_data_india = mob_data_india.dropna()

	for i in range(len(mobility_type)):
		x_axis = []
		y_axis = []
		for j in range(0,mob_data_india.shape[0],20):
			x_axis.append(mob_data_india.iloc[j,3])
			y_axis.append(mob_data_india.iloc[j,i+4])
		plt.plot(x_axis,y_axis,label = mobility_type[i])
		plt.legend(prop=fontP,bbox_to_anchor=(0.36,0.55))
		plt.title(state)
		plt.xlabel('dates')
		plt.ylabel('Percent change from baseline')
		
	plt.savefig('E:/Covid Hackathon/Plots/' + state + '.png') #change path accordingly
	plt.close()
	

		