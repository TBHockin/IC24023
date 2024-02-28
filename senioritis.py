#a program to evaluate how grade effects likelihood to register, certify, ect.
#import
import pandas as pd
import plotly.express as px


#
greenTerp = pd.read_csv('Data_Level3_GreenTerp - Cleaned.csv', dtype={25: str, 26: str, 37: str, 39:str, 40:str})

gradeForm = greenTerp[['Grade-Num', 'Form-Type']]

#create a function that evaluates dataframes and gives their value counts
grade1 = gradeForm[gradeForm['Grade-Num'] == 1]
grade2 = gradeForm[gradeForm['Grade-Num'] == 2]
grade3 = gradeForm[gradeForm['Grade-Num'] == 3]
grade4 = gradeForm[gradeForm['Grade-Num'] == 4]
grade5 = gradeForm[gradeForm['Grade-Num'] == 5]

grades = [grade1, grade2, grade3, grade4, grade5]
gradecounts = []

for i in range(len(grades)):
    count = grades[i].value_counts()
    count = dict(count)
    count['Registration'] = count[(i+1, 'Registration')]
    count['Certification'] = count[(i+1, 'Certification')]
    count.pop((i+1, 'Registration'))
    count.pop((i+1, 'Certification'))
    gradecounts.append(count)
    #grab the registration, put it in a list
    
countDF = pd.DataFrame(gradecounts)
countDF = countDF.assign(Grade=[1,2,3,4,5])
print(countDF)
#now make a data frame from this information, having a grade col, a cert col, and a registration col

#now make and display a pie chart for registrations, certs, all organized by grade with consistent colors
fig = px.pie(countDF, values='Certification', names='Grade', title='Certifications By Grade (All Years)')
fig.show()

regfig = fig = px.pie(countDF, values='Registration', names='Grade', title='Registration By Grade (All Years)')
regfig.show()

