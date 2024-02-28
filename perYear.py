import pandas as pd
import plotly.express as px

greenTerp = pd.read_csv('Data_Level3_GreenTerp - Cleaned.csv', dtype={25: str, 26: str, 37: str, 39:str, 40:str})


#make a chart for each year
regyears = greenTerp['AY'].value_counts()
regyears = dict(regyears)
#print(regyears)

#create a dict of lists with the data in it
data = {'AY(Registration)' : regyears.keys(), 'Amount of Registrations': regyears.values()}
regyearDF = pd.DataFrame.from_dict(data)

print(regyearDF)

#now graph this to show overall trend for the academic years
fig = px.bar(regyearDF, x = 'AY(Registration)', y= 'Amount of Registrations', title= 'Registrations by Academic Year')
fig.show()

#now break it down by grade:
yearNgrade = greenTerp[['AY', 'Form-Type', 'Grade-Num']]
year1grade = yearNgrade[yearNgrade['Grade-Num'] == 1]

#break it down by year:
gOne1819 = year1grade[year1grade['AY'] == '2018-2019']
gOne1920 = year1grade[year1grade['AY'] == '2019-2020']
gOne2122 = year1grade[year1grade['AY'] == '2021-2022']
gOne2223 = year1grade[year1grade['AY'] == '2022-2023']

#make a list of years
yearlist = []
gOnes = [gOne1819, gOne1920, gOne2122, gOne2223]

#save these as value counts somehow

frame1819 = gOne1819.value_counts().reset_index().rename(columns={"index": "value", 0: "count"})
frame1920 = gOne1920.value_counts().reset_index().rename(columns={"index": "value", 0: "count"})
frame2122 = gOne2122.value_counts().reset_index().rename(columns={"index": "value", 0: "count"})
frame2223 = gOne2223.value_counts().reset_index().rename(columns={"index": "value", 0: "count"})

frameAllyears = pd.concat([frame1819,frame1920,frame2122,frame2223],ignore_index=True).reset_index()

#separate it into reg and cert data frames
#ovrAllyears = frameAllyears[frameAllyears['Form-Type'] == 'Registration' | 'Certification']
#certAllyears = frameAllyears[frameAllyears['Form-Type'] == 'Certification']

#now visualize the effectiveness of GreenTerp Advertising to Incoming Classes over the Acedemic Years available
barboth = px.histogram(frameAllyears, x="AY", y="count",
             color='Form-Type', barmode='group',
             title='Grade 1 Involvement Over the Years')

barboth.show()