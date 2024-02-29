#a program to evaluate how grade effects likelihood to register, certify, ect.
#import
import pandas as pd
import plotly as px

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
gradedictts = {}

for i in range(len(grades)):
    gradedictts[i+1] = grades[i]['Form-Type'].value_counts()
    print(gradedictts[i+1])

print(gradedictts)
#now make the 
