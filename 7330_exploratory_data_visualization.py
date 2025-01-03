# -*- coding: utf-8 -*-
"""7330_Exploratory_Data_Visualization.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1iK_yGdkHenOiCqQEITdGPu-DcaRkBNdd

# Into

As a graduate student at Hong Kong Baptist University, I embarked on an analysis of Hong Kong's higher education system and its impact on graduates' career trajectories. With eight public universities producing a significant number of talents annually, it is crucial to understand whether these graduates pursue further studies or enter the workforce, and if so, which industries they prefer.

# Import libraries
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import requests
import numpy as np

#Visualisation
#MatPlotLib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
# %matplotlib inline

#Seaborn
import seaborn as sns
plt.style.use('ggplot')
pd.set_option('display.max_colwidth', None)

"""# Files Connection"""

from google.colab import drive
drive.mount('/content/drive')
drivePath = '/content/drive'

def download_file_from_github(file_url, file_path):
    response = requests.get(file_url)
    if response.status_code == 200:
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"The file have been downloaded at:{file_path}")
    else:
        print(f"Eerror:{response.status_code}")

# download table-Graduate_Employment_Situation(Eng)
file_url = 'https://raw.githubusercontent.com/Yi-XIE/JustHomework/refs/heads/main/Graduate_Employment_Situation(Eng).csv'
file_path = drivePath + '/MyDrive/Colab Notebooks/data/GES.csv'
download_file_from_github(file_url, file_path)

!ls '/content/drive/MyDrive/Colab Notebooks/data' #Check the file

df = pd.read_csv(file_path)
print(df.columns)

"""# Data Cleaning"""

df['Academic Year'] = df['Academic Year'].astype(str)

# Find the first index which value is"2012/13"in the 'Academic Year'column
first_2012_index = df[df['Academic Year'] == '2012/13'].index.min()

# Delete all the row before "2012/13"
df = df.loc[first_2012_index:].reset_index(drop=True)

# check the result
print(df.head())

"""# Dataset Analysis
Using Python, you will conduct an in-depth analysis of the dataset, identifying:
- the structure of the dataset
- the data types involved
- the statistical properties of data
o numerical variables: average, maximum, and minimum values
o categorical: possible values and their frequency
- the different data fields that can be useful for your data analysis task
"""

# Analyze the structure of the dataset
df.info()

# Identify the data types involved
df.dtypes

# Statistical properties of numerical variables
df.describe()

# Statistical properties of categorical variables: unique values and their frequency
categorical_stats = {
    col: df[col].value_counts() for col in df.select_dtypes(include=[object]).columns
}
print(categorical_stats)

print(df.isnull().sum())

"""# Visualization

## 1. How many people graduate from each university every year?
"""

# Group and calculate the number of graduates per year for each university
graduates_per_year_university = df.groupby(['Academic Year', 'University'])['Number of Graduates (Headcount)'].sum().reset_index()

# Create a plot
plt.figure(figsize=(14, 8))

# Create a line plot for each university
for university in graduates_per_year_university['University'].unique():
    uni_data = graduates_per_year_university[graduates_per_year_university['University'] == university]
    plt.plot(uni_data['Academic Year'], uni_data['Number of Graduates (Headcount)'], marker='o', label=university)

# Set the chart title and labels
plt.title('Number of Graduates per Year by University')
plt.xlabel('Academic Year')
plt.ylabel('Number of Graduates')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

# Display the chart
plt.show()

"""## 2. The proportion of full-time employment among graduates from each university per year"""

# 1. Filter full-time employment data
ft_employment_data = df[df['Employment Situation'] == 'FT employment']

# 2. Calculate the number of full-time employed graduates per year for each university
ft_employment_per_year = ft_employment_data.groupby(['Academic Year', 'University'])['Number of Graduates (Headcount)'].sum().reset_index()
ft_employment_per_year.rename(columns={'Number of Graduates (Headcount)': 'FT Employment'}, inplace=True)

# 3. Calculate the total number of graduates per year for each university
total_graduates_per_year = df.groupby(['Academic Year', 'University'])['Number of Graduates (Headcount)'].sum().reset_index()
total_graduates_per_year.rename(columns={'Number of Graduates (Headcount)': 'Total Graduates'}, inplace=True)

# 4. Merge the two datasets and calculate the ratio
employment_ratio = pd.merge(ft_employment_per_year, total_graduates_per_year, on=['Academic Year', 'University'])
employment_ratio['FT Employment Ratio'] = employment_ratio['FT Employment'] / employment_ratio['Total Graduates']

# 5. Plot the FT employment ratio per year for each university
plt.figure(figsize=(14, 8))

for university in employment_ratio['University'].unique():
    uni_data = employment_ratio[employment_ratio['University'] == university]
    plt.plot(uni_data['Academic Year'], uni_data['FT Employment Ratio'], marker='o', label=university)

# Set the chart title and labels
plt.title('FT Employment Ratio per Year by University')
plt.xlabel('Academic Year')
plt.ylabel('FT Employment Ratio')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

# Display the chart
plt.show()

"""## 3. The chart of educational qualification distribution among graduates from each university over the past decade"""

# Get the list of unique universities
universities = df['University'].unique()

# Create a pie chart for each university
for university in universities:
    # Filter data for the current university
    uni_data = df[df['University'] == university]

    # Group by level of study and calculate the number of graduates
    level_counts = uni_data.groupby('Level of study')['Number of Graduates (Headcount)'].sum()

    # Create a pie chart
    plt.figure(figsize=(5, 5))
    plt.pie(level_counts, labels=level_counts.index, autopct='%1.1f%%', startangle=140)

    # Set the chart title
    plt.title(f'Graduate Distribution by Level of Study for {university}')

    # Display the chart
    plt.tight_layout()
    plt.show()

"""##  4. Comparing employment situations among different universities"""

# Compare employment situations among different universities
employment_distribution = df.groupby(['University', 'Employment Situation'])['Number of Graduates (Headcount)'].sum().unstack()

# Create a bar chart for employment situations between universities
employment_distribution.plot(kind='bar', figsize=(12, 8))

# Set the chart title and labels
plt.title('Employment Situation Distribution for Each University')
plt.xlabel('University')
plt.ylabel('Number of Graduates')
plt.xticks(rotation=45)
plt.legend(title='Employment Situation')
plt.tight_layout()
plt.show()

"""## 5. Career choices among graduates from different universities"""

# Determine the occupation fields that absorb the most graduates
total_occupation_counts = df.groupby('Occupation')['Number of Graduates (Headcount)'].sum().sort_values(ascending=False)

# Create a bar chart for the top occupation fields that absorb the most graduates
plt.figure(figsize=(10, 8))
total_occupation_counts.head(10).plot(kind='barh')
plt.title('Top Occupations Absorbing the Most Graduates')
plt.xlabel('Number of Graduates')
plt.ylabel('Occupation')
plt.tight_layout()
plt.show()

# Analyze the differences in career choices among graduates from different universities
universities = df['University'].unique()

# Create a bar chart for the occupation distribution for each university
for university in universities:
    uni_data = df[df['University'] == university]
    occupation_counts = uni_data.groupby('Occupation')['Number of Graduates (Headcount)'].sum().sort_values()

    plt.figure(figsize=(10, 8))
    occupation_counts.plot(kind='barh')
    plt.title(f'Occupation Distribution for {university}')
    plt.xlabel('Number of Graduates')
    plt.ylabel('Occupation')
    plt.tight_layout()
    plt.show()

"""## 6. The proportion of different universities in a specific industry"""

# Choice specific industries
industries = [
    "Engineers",
    "Medical and Health Workers",
    "Teaching Profession",
    "Accountants and Auditors",
    "Business Professionals",
    "Authors, Journalists and Related Writers",
    "System Analysts and Computer Programmers",
    'Architects and Surveyors'
]

# Create a pivot table for industries and universities
pivot_table = df.pivot_table(
    values='Number of Graduates (Headcount)',
    index='University',
    columns='Occupation',
    aggfunc='sum',
    fill_value=0
)

# Filter columns to include only the industries of interest
filtered_table = pivot_table[industries]

# Plot a heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(filtered_table, annot=True, fmt='d', cmap='YlGnBu', cbar_kws={'label': 'Number of Graduates'})
plt.title('Heatmap of Graduate Distribution by University and Occupation')
plt.ylabel('University')
plt.xlabel('Occupation')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()