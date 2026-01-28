import pandas as pd

path="/Users/manivannans/EDA-Corpus/Augmented_Data/Prompt-Script/Flow/flow.csv"
df=pd.read_csv(path)
print(df.iloc[5])