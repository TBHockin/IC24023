#this program measures the likelihood of retention, both overall and by year, in addition to
#projectiong the effects of retention in achieving UMD's goals

import pandas as pd
import plotly.express as px

greenTerp = pd.read_csv('Data_Level3_GreenTerp - Cleaned.csv', dtype={25: str, 26: str, 37: str, 39:str, 40:str})

#create a data frame to tell me how many unique ids are repeated:
idFrame = greenTerp[['AY', 'Form-Type', 'Grade-Num', 'UniqueID']]
idFreshmen = idFrame[idFrame['Grade-Num'] == 1]

#get the value counts for the ids
repeated = idFrame['UniqueID'].value_counts()
repFrame = repeated.reset_index().rename(columns={"index": "value", 0: "count"}) #made into a df for ease of analysis

#check for the presense of multiple years for each id with more than one count
repFrame = repFrame[repFrame['UniqueID'] > 1] #limit it to only people who did it more than once
print(repFrame)
#check for multiple years and pare down df based on those who have multiple years
fullrepFrame = idFrame[idFrame['UniqueID'].isin(repFrame['value'])]

#now parse the df down to just those with multiple years:
    
noDupes = fullrepFrame.drop_duplicates(subset=['UniqueID','AY'])

#now, show what percent of people did how many years of participation
# make a data frame out of this stuff of noDupes
noDupeCount = noDupes['UniqueID'].value_counts().reset_index().rename(columns={"index": "value", 0: "count"})
pieDF = noDupeCount['UniqueID'].value_counts().reset_index().rename(columns={"index": "value", 0: "count"})
print(pieDF)
fig = px.pie(pieDF, values='UniqueID', names='value', title='Student Retention In Years')
fig.update_layout({'paper_bgcolor' : 'rgba(0, 0, 0, 0)','plot_bgcolor' : 'rgba(0, 0, 0, 0)'})

fig.show()
