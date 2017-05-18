from time import sleep
import numpy as np

import pandas as pd
from src.db.get_data_from_pytrends import get_trends


data_frame = pd.read_csv('../../data/compressed_dataset2.csv', sep='\t')
new_df = pd.DataFrame(0, index=np.arange(len(data_frame.index)), columns=['W1', 'W2', 'W3', 'W4', 'Total_W_AVG', 'Growth_Rate'])
thefile = open('trends_only.txt', 'w')


for index, row in data_frame.loc[data_frame['Year'] >= 2012].iterrows():
	print ("")
	print ("index: " + str(index))

	Title = row['Title']
	Year = row['Year']
	Month = row['Month']
	Day = row['Day']

	print (Title, Year, Month, Day)

	trends_data, avgs, total_avg, growth_rate = get_trends(Title, int(Year), Month, int(Day))
	row = avgs + [total_avg, growth_rate]
	avgs_str = "\t".join(map(lambda x: str(x), avgs))

	str_to_file = "\t".join([Title, str(Year), str(Month), str(Day), avgs_str, str(total_avg), str(growth_rate), str(trends_data)])
	print (str_to_file)
	thefile.write("%s\n" % str_to_file)

	print (row)

	try:
		new_df.loc[index] = row
	except:
		print ("Mismatch columns")
		new_df.loc[index] = [0, 0, 0, 0, 0, 0]


new_df.to_csv("../../data/trends_dataset_new.csv", sep='\t')
new_data_frame = pd.concat([data_frame, new_df], axis=1)
new_data_frame = new_data_frame.drop_duplicates()
new_data_frame.to_csv("../../data/trends_dataset_joined.csv", sep='\t')
