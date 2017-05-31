import pandas as pd

df = pd.read_csv('../../data/trends_dataset_joined.csv', sep='\t')
decimals = pd.Series([0], index=['IMDb_Rating'])
df.round(decimals)

df.to_csv("../../data/10_class_rating_dataset.csv", sep='\t')
