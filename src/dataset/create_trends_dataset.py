import pandas as pd
from src.db.get_data_from_pytrends import get_trends


data_frame = pd.read_csv('../../data/compressed_dataset2.csv', sep='\t')
new_df = pd.DataFrame(columns=['W1', 'W2', 'W3', 'W4', 'Total_W_AVG', 'Growth_Rate'])

all_trends_data = []

for index, row in data_frame.iterrows():
	print ("")
	print ("index: " + str(index))

	Title = row['Title']
	Year = row['Year']
	Month = row['Month']
	Day = row['Day']

	print (Title, Year, Month, Day)

	trends_data, avgs, total_avg, growth_rate = get_trends(Title, int(Year), Month, int(Day))
	row = avgs + [total_avg, growth_rate]

	all_trends_data += [[Title, Year, Month, Day, trends_data, avgs, total_avg, growth_rate]]
	print (row)

	new_df.loc[index] = row
	index += 1

new_data_frame = pd.concat([data_frame, new_df], axis=1)
new_data_frame = new_data_frame.drop_duplicates()
new_data_frame.to_csv("../../data/trends_dataset.csv", sep='\t')

thefile = open('trends_only.txt', 'w')
for item in all_trends_data:
	thefile.write("%s\n" % item)

