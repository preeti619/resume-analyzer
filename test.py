import pandas as pd
df = pd.read_csv("UpdatedResumeDataSet.csv")
print(df.columns)
print(df['Category'].value_counts())