#import
import pandas as pd

#
greenTerp = pd.read_csv('Data_Level3_GreenTerp - Cleaned.csv')
gt2 = greenTerp['Full_Choices']
# .value_counts()
print(gt2.value_counts())