import pandas as pd
import plotly.express as px

#THE FOLLOWING IS SETTING UP BASIC DATAFRAMES FOR FURTHER GRAPHING

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Reads in whole thing as csv, note that the 26th column (zip codes) are ints
whole_thing = pd.read_csv('/home/mids/m263306/SD212/IC24/IC24023/Data_Level3_GreenTerp - Cleaned.csv', dtype={25:str, 26:str, 37:str, 39:str, 40:str})

#Gets DataFrames for indicated residence
on_campus = whole_thing[whole_thing['Housing']=='On Campus (including South Campus Commons)']
off_campus = whole_thing[whole_thing['Housing']=='Off Campus']
greek_life = whole_thing[whole_thing['Housing']=='Fraternity or Sorority House'] #gives people living in greek life.
#print(whole_thing['Housing'].value_counts()) #5870 On campus, 2633 off campus, 2492 in a frat

# print(on_campus['Form-Type'].value_counts()) #4258/1612
# print(off_campus['Form-Type'].value_counts()) #1759/874
# print(greek_life['Form-Type'].value_counts()) #1488/1004
#Net participants: 4258 from on campus, 1759 from off campus, and 1488 from greek life

frats = whole_thing[whole_thing['House']=='Fraternity']
sororities = whole_thing[whole_thing['House']=='Sorority']
#print(frats['Form-Type'].value_counts()) #1198/826
#print(sororities['Form-Type'].value_counts()) #1823/1072

frat_list=[]
sorority_list=[]
#print(frats['Green-Chapter_House'].value_counts())
for frat in frats['Green-Chapter_House'].tolist():
    if frat in frat_list:
        pass
    else:
        frat_list.append(frat)
for sor in sororities['Green-Chapter_House'].tolist():
    if sor in sorority_list:
        pass
    else:
        sorority_list.append(sor)

#I now have a list of all frats, and another for all sororities
#Print how many registered vs how many certified for each frat/sorority
frat_ratios=[]
frat_ratios_percent=[]
frat_dict={} #this should be a dictionary mapping frat names to certification percentage
for f in frat_list:
    this_frat = frats[frats['Green-Chapter_House'] == f] #gets all the rows of people in a frat
    #print(f)
    counts=this_frat['Form-Type'].value_counts()
    try:
       # print(counts)
        #print(counts['Certification']/counts['Registration'])
        #print('\n')
        frat_ratios.append(counts['Certification']/counts['Registration'])
        #frat_ratios_percent.append(100*(counts['Certification']/counts['Registration']))
        frat_dict[f]=(counts['Certification']/counts['Registration'])
        
    except:
        #print(0)
        frat_ratios.append(0)
        frat_dict[f]=0
        #frat_ratios_percent.append(0)

#print('Avg frat certification rate (unweighted):')
#print(sum(frat_ratios)/len(frat_ratios))
sor_ratios=[]
sor_dict={}
for s in sorority_list:
    this_sor = sororities[sororities['Green-Chapter_House']==s]
    #print(s)
    counts=this_sor['Form-Type'].value_counts()
    try:
        #print(counts)
        #print(counts['Certification']/counts['Registration'])
        #print('\n')
        sor_ratios.append(counts['Certification']/counts['Registration'])
        sor_dict[s]=counts['Certification']/counts['Registration']
    except:
        #print(0)
        sor_ratios.append(0)
        sor_dict[s]=0
sor_dict['Sorority']=sorority_list
frat_dict['Frat']=frat_list
sor_dict['Ratios']=sor_ratios
frat_dict['Ratios']=frat_ratios
#print('Avg sorority certification rate (unewighted):')
#print(sum(sor_ratios)/len(sor_ratios))
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#BEGIN GRAPHS

#Finding what % of Green Terps involved in a Frat are in what fraternity:

frat_counts=frats['Green-Chapter_House'].value_counts().reset_index()
total_count=len(frats['Green-Chapter_House'])
small_frats=frat_counts.loc[frat_counts['count'] / total_count < 0.05, 'Green-Chapter_House']
frat_counts = frat_counts.sort_values(by='count', ascending=False)
frat_pie = px.pie(frat_counts, names='Green-Chapter_House', values='count',title='% of Greek Enrollment by Fraternity')
frat_pie.update_layout(title=dict(font=dict(size=32),x=0.5, y =0.95),paper_bgcolor='powderblue')
frat_pie.update_layout(
    margin=dict(l=0, r=0, b=20, t=90),  # Set margin to reduce space around the chart
    legend=dict(x=0.8, y=0.9), height=600         # Adjust legend position
)
#frat_pie.show()

#Same but for Sorority:
sor_counts=sororities['Green-Chapter_House'].value_counts().reset_index()
total_count=len(sororities['Green-Chapter_House'])
sor_pie = px.pie(sor_counts, names='Green-Chapter_House', values='count',title='% of Greek Enrollment by Sorority')
sor_pie.update_layout(title=dict(font=dict(size=32),x=0.5, y =0.95),paper_bgcolor='powderblue')
sor_pie.update_layout(
    margin=dict(l=0, r=0, b=20, t=90),  # Set margin to reduce space around the chart
    legend=dict(x=0.8, y=0.9), height=600         # Adjust legend position
)
#sor_pie.show()

#creating a sorted dictionary
sorted_frat_list = frats['Green-Chapter_House'].value_counts().reset_index()['Green-Chapter_House'].tolist()
sorted_frat_ratios=[]
for f in sorted_frat_list:
    sorted_frat_ratios.append(frat_dict[f])
sorted_frat_list.reverse()
sorted_frat_ratios.reverse()
sorted_frat_dict={'Fraternity Sorted by # Registered':sorted_frat_list, '% Certified':sorted_frat_ratios}

#Creating a bar graph of each frat and soroities certification %:

frat_cert_rates = px.bar(sorted_frat_dict, x='Fraternity Sorted by # Registered', y='% Certified',        
                         title='Certification Rate by Fraternity',
                         width=1200,
                         height=750)
frat_cert_rates.add_hline(y=1,line_color='red')
frat_cert_rates.add_hline(y=0.30,line_dash='dash',line_color='green', annotation_text='Target Certification Rate')
frat_cert_rates.update_yaxes(tickformat='.0%')
color_scale=[(0,'yellow'),(1,'green'),(2,'red')]
color_discrete_map = {'yellow': 'yellow' ,'green':'green','red':'red' }
frat_rates_df=pd.DataFrame(sorted_frat_dict)
frat_cert_rates.update_traces(marker=dict(color=frat_rates_df['% Certified'].apply(lambda x: 'yellow' if x < 0.5 else 'green' if x <= 1.0 and x >= 0.5 else 'red')), selector=dict(type='bar'))
frat_cert_rates.update_layout(yaxis=dict(range=[0,1.5]), title=dict(font=dict(size=32),x=0.5),paper_bgcolor='rgba(0, 0, 0, 0)')
frat_cert_rates.write_image('Final_Frat_Cert_Rates.svg')
#frat_cert_rates.show()

sorted_sor_list = sororities['Green-Chapter_House'].value_counts().reset_index()['Green-Chapter_House'].tolist()
sorted_sor_ratios=[]
for s in sorted_sor_list:
    sorted_sor_ratios.append(sor_dict[s])
sorted_sor_list.reverse()
sorted_sor_ratios.reverse()
sorted_sor_dict={'Sorority Sorted by # Registered':sorted_sor_list, '% Certified':sorted_sor_ratios}
sor_cert_rates = px.bar(sorted_sor_dict, x='Sorority Sorted by # Registered', y='% Certified',
                         title='Certification Rate By Sorority', width=800, height=500)
sor_cert_rates.add_hline(y=1,line_color='red')
sor_cert_rates.add_hline(y=0.30,line_dash='dash',line_color='green', annotation_text='Target Certification Rate')
sor_cert_rates.update_yaxes(tickformat='.0%')
color_scale=[(0,'yellow'),(1,'green'),(2,'red')]
color_discrete_map = {'yellow': 'yellow' ,'green':'green','red':'red' }
sor_rates_df=pd.DataFrame(sorted_sor_dict)
sor_cert_rates.update_traces(marker=dict(color=sor_rates_df['% Certified'].apply(lambda x: 'yellow' if x < 0.3 else 'green' if x <= 1.0 and x >= 0.3 else 'red')), selector=dict(type='bar'))
sor_cert_rates.update_layout(yaxis=dict(range=[0,1.4]), title=dict(font=dict(size=32),x=0.5),paper_bgcolor='rgba(0, 0, 0, 0)')
#sor_cert_rates.show()
#print(sum(frat_dict['Ratios'])/len(frat_dict['Ratios']))


#Make a graph of certification rates for people living in greek life houses, vs on campus, vs off campus.
#comparison_df = {"Frats":frat_dict['Ratios'], "Sororities":sor_dict['Ratios'],}
greek_ratio = greek_life['Form-Type'].value_counts()['Certification']/greek_life['Form-Type'].value_counts()['Registration']
on_campus_ratio = on_campus['Form-Type'].value_counts()['Certification']/on_campus['Form-Type'].value_counts()['Registration']
off_campus_ratio = off_campus['Form-Type'].value_counts()['Certification']/off_campus['Form-Type'].value_counts()['Registration']
comparison_dict = {'Greek Life':greek_ratio,'On Campus':on_campus_ratio, 'Off Campus':off_campus_ratio, 'Housing':['On Campus','Off Campus','Greek Life'],'% Certification':[on_campus_ratio,off_campus_ratio,greek_ratio]}
comparison_df = pd.DataFrame(comparison_dict)
colors = {'Greek Life':'green', 'On Campus':'orange', 'Off Campus':'yellow'}

comparison_fig = px.bar(comparison_df, x='Housing',y='% Certification', title='Certification Rates by Housing',
                        height=900, width=700, color_discrete_sequence=['green'])
comparison_fig.update_yaxes(tickformat='.0%')
comparison_fig.update_layout(yaxis=dict(range=[0,1.0]),title=dict(font=dict(size=32),x=0.5),paper_bgcolor='rgba(0, 0, 0, 0)')
#comparison_fig.show()

#of green terps by greek affiliation
registers = whole_thing[whole_thing['Form-Type']=='Registration']
# print(registers['House'].value_counts())
# print(len(registers))
non_greeks = 7505-1823-1198
affiliations = {'Affiliation':['Non Greek Life', 'Sorority/Fraternity'], '% Green Terps':[non_greeks,1823+1198]}
affiliations_pie = px.pie(affiliations, names='Affiliation', values='% Green Terps',title='% of Green Terps by Greek Affiliation')
affiliations_pie.update_layout(title=dict(font=dict(size=32),x=0.5, y =0.95),paper_bgcolor='rgba(0, 0, 0, 0)')
affiliations_pie.update_layout(
    margin=dict(l=0, r=0, b=20, t=90),  # Set margin to reduce space around the chart
    legend=dict(x=0.7, y=0.9), height=600         # Adjust legend position
)
#affiliations_pie.show()

enrollment = {'Affiliation':['Non Greek Life', 'Sorority/Fraternity'],'% Student Body':[0.84,0.16]}
enrollment_pie = px.pie(enrollment, names='Affiliation', values='% Student Body', title='% Of Student Body by Greek Affiliation' )
enrollment_pie.update_layout(title=dict(font=dict(size=32),x=0.5, y =0.95),paper_bgcolor='rgba(0, 0, 0, 0)')
enrollment_pie.update_layout(
    margin=dict(l=0, r=0, b=20, t=90),  # Set margin to reduce space around the chart
    legend=dict(x=0.7, y=0.9), height=600         # Adjust legend position
)
#enrollment_pie.show()


housing = registers['Housing'].value_counts().reset_index()
perc_on = 9450/30350 #gotten from campusvisitorguides.com
perc_off = 0.62
perc_greek = 1-perc_on-perc_off
housing_dict = {'Housing':['On Campus', 'Greek Housing', 'Off Campus'], 'percent':[perc_on,perc_greek,perc_off]}
colors_df = pd.DataFrame({'Housing': ['On Campus', 'Off Campus', 'Greek Housing'],
                          'percent': [perc_on, perc_off, perc_greek],
                          'color': ['blue', 'red', 'green']})
category_order = ['On Campus', 'Greek Housing', 'Off Campus']

housing_pie = px.pie(colors_df, names='Housing',values='percent',color='color',title='% Of UMD Population by Housing',
                     category_orders={'Housing': ['On Campus', 'Off Campus', 'Greek Housing']})
housing_pie.update_layout(title=dict(font=dict(size=32),x=0.5, y =0.95),paper_bgcolor='rgba(0, 0, 0, 0)')
housing_pie.update_layout(
    margin=dict(l=0, r=0, b=20, t=90),  # Set margin to reduce space around the chart
    legend=dict(x=0.7, y=0.9), height=600         # Adjust legend position
)
#housing_pie.show()

green_housing_pie = px.pie(housing, names=['On Campus', 'Off Campus', 'Greek Housing'], values='count', title='% Of Green terp Participation by Housing')
green_housing_pie.update_layout(title=dict(font=dict(size=32),x=0.5, y =0.95),paper_bgcolor='rgba(0, 0, 0, 0)')
green_housing_pie.update_layout(
    margin=dict(l=0, r=0, b=20, t=90),  # Set margin to reduce space around the chart
    legend=dict(x=0.7, y=0.9), height=600         # Adjust legend position
)
#green_housing_pie.show()


#Pie chart of green terp certification by housing
certs = whole_thing[whole_thing['Form-Type']=='Certification']
# print(certs['Housing'].value_counts()) #used to find numbers
total = 1612+1004+874
certs_on = 1612/total
certs_greek = 1004/total
certs_off = 874/total
certs_housing_dict = {'Housing':['On Campus', 'Off Campus','Greek Housing'], '% Certification':[certs_on,certs_off,certs_greek]}

cert_housing_pie = px.pie(certs_housing_dict, names='Housing', values='% Certification', title='% Of Overall Certifications by Housing',
                          category_orders={'Housing':['On Campus', 'Off Campus', 'Greek Housing']})
cert_housing_pie.update_layout(title=dict(font=dict(size=32),x=0.5,y=0.95),paper_bgcolor='rgba(0, 0, 0, 0)')
cert_housing_pie.update_layout(
    margin = dict(l=0, r=0, b=20, t=90),  # Set margin to reduce space around the chart
    legend=dict(x=0.7, y=0.9), height=600         # Adjust legend position
)
cert_housing_pie.show()

#Can we give a number of difficulty to each selectd option, and rank how people are choosing them? i.e. give a score.
choices_dine = whole_thing['Choices_Dine'] #0: 5843, 1: 5152
choices_aware = whole_thing['Choices_Awareness'] #0: 10632, 1:363
choices_commute = whole_thing['Choices_Commute'] #0: 5715, 1:5280
choices_reduce = whole_thing['Choices_Reduce'] #1: 5539, 0: 5456
choices_products = whole_thing['Choices_Products'] #0: 5732, 1: 5263
choices_energy = whole_thing['Choices_Energy'] #0: 5555, 1: 5440
choices_water = whole_thing['Choices_Water'] #0: 5466, 1: 5529
choices2 = whole_thing['Choices_Choices'] #0: 5806, 1: 5189

#now doing it for frats and soroities:
frats_dine = frats['Choices_Dine']#0: 917, 1: 1107, 55%
frats_aware = frats['Choices_Awareness']# Everyone said no
frats_commute = frats['Choices_Commute']# 57% said yes
frats_reduce = frats['Choices_Reduce']# 59.5% said yes
frats_products = frats['Choices_Products']# 56.3% said yes
frats_energy = frats['Choices_Energy']# 58.6% said yes
frats_water = frats['Choices_Water']# 59.5% said yes
frats_choices = frats['Choices_Choices']# 60.2% said yes

sor_dine = sororities['Choices_Dine']# 48% said yes
sor_aware = sororities['Choices_Awareness']# again 0?
sor_commute = sororities['Choices_Commute']# 48.6% said yes
sor_reduce = sororities['Choices_Reduce']# 50.4% said yes
sor_products = sororities['Choices_Products']# 48.5% said yes
sor_energy = sororities['Choices_Energy']# 49.7% said yes
sor_water = sororities['Choices_Water']# 50.7%
sor_choices = sororities['Choices_Choices']# 50.5%

# vals = sor_choices.value_counts()
# print(vals)

# #prints ratio of people who said they would/total people
# print(vals[1]/len(sor_choices))

#Since these values are so conistent, maybe find people who always said no/yes
zeros = whole_thing[(whole_thing['Choices_Dine']==0) & (whole_thing['Choices_Reduce']==0) & (whole_thing['Choices_Commute']==0) & (whole_thing['Choices_Products']==0) & (whole_thing['Choices_Energy']==0) & (whole_thing['Choices_Water']==0) & (whole_thing['Choices_Choices']==0) & (whole_thing['Choices_Awareness']==0)]
# print(len(zeros[zeros['Form-Type']=='Registration']))
# print(len(zeros[(zeros['Form-Type']=='Registration') & (zeros['AY']!='2018-2019')]))
# print(len(zeros[zeros['Form-Type']=='Certification']))
# print(len(zeros[(zeros['Form-Type']=='Certification') & (zeros['AY']!='2018-2019')]))

# print(len(whole_thing[whole_thing['Form-Type']=='Certification']))


past_2019 = whole_thing[whole_thing['AY']!='2018-2019']
# print(len(past_2019[past_2019['Form-Type']=='Certification']))
awares = whole_thing['Choices_Awareness']
#print(awares.value_counts())

