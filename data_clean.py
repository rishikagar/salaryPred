# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 11:04:43 2023

@author: Rishika
"""
import pandas as pd

df = pd.read_csv('C:/Users/Nana/OneDrive - Ferdinand-Steinbeis-Institut/Documents/project/glassdoor_jobs.csv')

#salary parsing

# add the hourly and employer provided column in data frame
df['hourly']= df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)
df['employer_provided']= df['Salary Estimate'].apply(lambda x: 1 if 'employer provided salary:' in x.lower() else 0)

# remove rows with salary = -1
df = df[df['Salary Estimate']!= '-1']
# remove (glassdoor est.)
salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0])
# remove K and $ sign
remove_k = salary.apply(lambda x: x.replace('K', '').replace('$', ''))
# remove per "hour" and "employer provided" text
min_hr = remove_k.apply(lambda x: x.lower().replace('per hour', '').replace('employer provided salary:', ''))
# get minimum salary
df['min_salary']= min_hr.apply(lambda x: int(x.split('-')[0]))
# get maximum salary
df['max_salary']= min_hr.apply(lambda x: int(x.split('-')[1]))
# avg salary
df['avg_salary']= (df.min_salary + df.max_salary)/2

#company name to text only
df['company_txt'] = df.apply(lambda x: x['Company Name'] if x['Rating'] < 0 else x['Company Name'][:-3], axis = 1)

# state
df['job_state']=df['Location'].apply(lambda x: x.split(',')[1])
print(df.job_state.value_counts())

#job location is at the headquaters
df['same_state']= df.apply(lambda x: 1 if x.Location == x.Headquarters else 0, axis = 1)
# company age
df['age']= df.Founded.apply(lambda x: x if x< 0 else 2022 - x)

# job description parsing( python, R studio, spark, aws, excel)
#python
df['python_yn'] = df['Job Description'].apply(lambda x : 1 if 'python' in x.lower() else 0)

#R studio
df['R_yn'] = df['Job Description'].apply(lambda x : 1 if 'r studio' in x.lower() else 0)

#spark
df['spark'] = df['Job Description'].apply(lambda x : 1 if 'spark' in x.lower() else 0)
print(df.spark.value_counts())

#aws
df['aws'] = df['Job Description'].apply(lambda x : 1 if 'aws' in x.lower() else 0)
print(df.aws.value_counts())

#excel
df['excel'] = df['Job Description'].apply(lambda x : 1 if 'excel' in x.lower() else 0)
print(df.excel.value_counts())

#drop the unnamed column
df_out = df.drop(['Unnamed: 0'], axis = 1)

# save data to csv
df_out.to_csv('salary_data_cleaned.csv', index = False)