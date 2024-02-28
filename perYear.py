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

byyearDF = pd.DataFrame(yearlist)
print(byyearDF)



