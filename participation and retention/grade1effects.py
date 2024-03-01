#this program projects how freshman involvement and a slight increase in retention can result in improved participation

#grab what percentage grade1 registrations is of the whole
#this program measures the likelihood of retention, both overall and by year, in addition to
#projectiong the effects of retention in achieving UMD's goals

import pandas as pd
import plotly.express as px

greenTerp = pd.read_csv('Data_Level3_GreenTerp - Cleaned.csv', dtype={25: str, 26: str, 37: str, 39:str, 40:str})

#get what percentage of each years stuff is freshman
#get each year
totals = greenTerp['AY'].value_counts().reset_index().rename(columns={"index": "value", 0: "count"})
totals.rename(columns= {'value' : 'Academic Year' , 'AY' : 'Overall Total'}, inplace= True)
freshmen = greenTerp[greenTerp['Grade-Num'] == 1]
freshtotals = freshmen['AY'].value_counts().reset_index().rename(columns={"index": "value", 0: "count"})
freshtotals.rename(columns= {'value' : 'Academic Year' , 'AY' : 'Freshman Total'}, inplace= True)


#print(freshandTot)
#set their indexes
freshtotals = freshtotals.set_index('Academic Year')
totals = totals.set_index('Academic Year')

freshtotals = freshtotals.join(totals)

#make a new col for the percentage
freshtotals['Percentage of Freshman (%)'] = (freshtotals['Freshman Total']/freshtotals['Overall Total'])*100
print(freshtotals)