import pandas as pd

df = pd.read_csv('../../data/trends_dataset_joined.csv', sep='\t')
df.loc[df["IMDb_Rating"] < 7, "IMDb_Rating"] = 0
df.loc[df["IMDb_Rating"] >= 7, "IMDb_Rating"] = 1
print (df["IMDb_Rating"])
df.to_csv("../../data/2_class_rating_dataset.csv", sep='\t')
