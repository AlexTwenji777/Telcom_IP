# -*- coding: utf-8 -*-
"""Moringa_Data_Science_Prep_W3_Independent_Project_2019_07_Alex_Twenji_DataReport.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18l7DNoFpqiE8g9yN0CLb33xEtzHp6i4m

In this week's independent project, you will be working as Data Scientist for MTN Cote d'Ivoire, a leading telecom company and you will be solving for the following research question.

Currently MTN Cote d'Ivoire would like to upgrade its technology infrastructure for its mobile users in Ivory Coast. Studying the given dataset, how does MTN Cote d'Ivoire go about the upgrade of its infrastructure strategy within the given cities?

**DATA PREPARATION**
"""

# importing libraries we will use

import pandas as pd
import numpy as np
from functools import reduce

# Setting ipython's maximum row and column displays
pd.set_option('display.max_columns', 50)

# Loading the datasets to our work environment
Telcom_read = pd.read_csv('Telcom_dataset.csv')
Telcom2_read = pd.read_csv('Telcom_dataset2.csv')
Telcom3_read = pd.read_csv('Telcom_dataset3.csv')
Location_read = pd.read_csv('cells_geo.csv')

# Previewing the datasets
# a) Telcom_read Dataset
Telcom_read.head()

# Observation: we'll need to clean the column headings by changing 'PRODUTC' to 'PRODUCT'
# & 'DATETIME' to 'DATE_TIME'

# b) Telcom2_read Dataset
Telcom2_read.head()

# Observation: we'll need to clean the column headings by changing 'DW_A_NUMBER'
# & 'DW_B_NUMBER' to 'DW_A_NUMBER_INT' & 'DW_B_NUMBER_INT' Respectively

# c) Telcom3_read Dataset
Telcom3_read.head()

# Observation: we'll need to clean the column headings by changing 'CELLID' to 'CELL_ID'
# and 'SIET_ID' to 'SITE_ID'

# d) Location_read Dataset
Location_read.head()

# notice the cleaning of data required. Suggestion is to split values along the ';' semi-colon

"""**DATA CLEANING**"""

# 1. Matching Telcom Datasets Column names as expected from the keys description table
# a) Telcom_read clean the column headings by changing 'PRODUTC' to 'PRODUCT'
# & 'DATETIME' to 'DATE_TIME'
Telcom_read.columns = ['PRODUCT', 'VALUE', 'DATE_TIME', 'CELL_ON_SITE', 'DW_A_NUMBER_INT',
                       'DW_B_NUMBER_INT', 'COUNTRY_A', 'COUNTRY_B', 'CELL_ID', 'SITE_ID']
Telcom_read.head()  # Previewing the table after the changes.

# b) Telcom2_read clean the column headings by changing 'DW_A_NUMBER'
#    & 'DW_B_NUMBER' to 'DW_A_NUMBER_INT' & 'DW_B_NUMBER_INT' Respectively
Telcom2_read.columns = ['PRODUCT', 'VALUE', 'DATE_TIME', 'CELL_ON_SITE', 'DW_A_NUMBER_INT',
                       'DW_B_NUMBER_INT', 'COUNTRY_A', 'COUNTRY_B', 'CELL_ID', 'SITE_ID']
Telcom2_read.head()

# c) Telcom3_read clean the column headings by changing 'CELLID' to 'CELL_ID'
#    and 'SIET_ID' to 'SITE_ID'
Telcom3_read.columns = ['PRODUCT', 'VALUE', 'DATE_TIME', 'CELL_ON_SITE', 'DW_A_NUMBER_INT',
                       'DW_B_NUMBER_INT', 'COUNTRY_A', 'COUNTRY_B', 'CELL_ID', 'SITE_ID']
Telcom3_read.head()

# 2. Cleaning Location_Read Data
Location_read[';VILLES;STATUS;LOCALISATION;DECOUPZONE;ZONENAME;LONGITUDE;LATITUDE;REGION;AREA;CELL_ID;SITE_CODE']
# Observation: The columns are not separated and neither is the data

# a)Separating the rows column-wise using the semicolon ':'
Location = Location_read[';VILLES;STATUS;LOCALISATION;DECOUPZONE;ZONENAME;LONGITUDE;LATITUDE;REGION;AREA;CELL_ID;SITE_CODE'].apply(lambda x: pd.Series([i for i in x.split(';')]))
Location
# Observation: The row-wise index column sems to be replicated since the data already had it's own indexing
# We can drop the second column of indexing.
# We have to manually add the column names provided in the datasheet.

# b) Adding Column Names
Location.columns = ['INDEX','VILLES', 'STATUS', 'LOCALISATION', 'DECOUPZONE', 'ZONENAME',
                    'LONGITUDE', 'LATITUDE', 'REGION','AREA', 'CELL_ID', 'SITE_CODE']
Location.head()

# 3) Dropping unrequired columns of data i.e. CELL_ON_SITE,DW_A_NUMBER_INT,DW_B_NUMBER_INT,
#    COUNTRY_A & COUNTRY_B from the Telcom Datasets
#    and dropping INDEX column on Location dataset

Telcom_read.head() # Invoking the Dataframe before further testing is required
Telcom = Telcom_read.drop(['CELL_ON_SITE', 'DW_A_NUMBER_INT', 'DW_B_NUMBER_INT', 'COUNTRY_A',
                  'COUNTRY_B'], axis= 1)
Telcom
# As can be seen, Telcom has data from 6th May 2012 - 7th May 2012

Telcom2_read.head()
Telcom_2 = Telcom2_read.drop(['CELL_ON_SITE', 'DW_A_NUMBER_INT', 'DW_B_NUMBER_INT', 'COUNTRY_A',
                  'COUNTRY_B'], axis= 1)
Telcom_2
# As can be seen, Telcom_2 has data from 7th May 2012 - 8th May 2012

Telcom3_read.head()
Telcom_3 = Telcom3_read.drop(['CELL_ON_SITE', 'DW_A_NUMBER_INT', 'DW_B_NUMBER_INT', 'COUNTRY_A',
                  'COUNTRY_B'], axis= 1)
Telcom_3
# As can be seen, Telcom_3 has data from 8th May 2012 - 9th May 2012
# All 3 Datasets seem to be between 23:00 hrs - 00:01 hrs

Location.head()
Geo_Location = Location.drop(['INDEX'], axis=1)
Geo_Location

# Sampling Data along the SITE_ID to check for NULL values
# Since the Telcom Datasets are similar, we'll use 1 to test this.
Telcom[Telcom['SITE_ID'].isnull()]
# Observation: Where there's no SITE_ID, There's no VALUE therefore we can assume
# there isn't infrastructure to be upgraded.

# From the above, we can make the data more compact by eliminating data with SITE_ID NULL values
Telcom1 = Telcom[Telcom['SITE_ID'].notnull()]
Telcom2 = Telcom_2[Telcom_2['SITE_ID'].notnull()]
Telcom3 = Telcom_3[Telcom_3['SITE_ID'].notnull()]
# Preview of Telcom3
Telcom3

# From the above, we got more insight, we can make our data better by getting rid of
# all data with VALUE 0, as this represents 0 customer engagement.
Telcom1 = Telcom1[Telcom1['VALUE'] != 0]
Telcom2 = Telcom2[Telcom2['VALUE'] != 0]
Telcom3 = Telcom3[Telcom3['VALUE'] != 0]
# Preview of new Telcom3
Telcom3

# From the data below, we can see irregularities in naming conventions of """Abidjan_EST"
# & "ASSINIE"""
Geo_Location

# The problem above was rectified as shown below, including all irregularities observed
# from the data.
Geo_Location.loc[Geo_Location['DECOUPZONE'] == '"""Abidjan_EST"', 'DECOUPZONE'] = 'Abidjan_EST'
Geo_Location.loc[Geo_Location['DECOUPZONE'] == '"""Abidjan_NORD"', 'DECOUPZONE'] = 'Abidjan_NORD'
Geo_Location.loc[Geo_Location['DECOUPZONE'] == '"""Abidjan_CENTRE"', 'DECOUPZONE'] = 'Abidjan_CENTRE'
Geo_Location.loc[Geo_Location['ZONENAME'] == '"ASSINIE"""', 'ZONENAME'] = 'ASSINIE'
Geo_Location.loc[Geo_Location['ZONENAME'] == '"KRIKOREA"""', 'ZONENAME'] = 'KRIKOREA'
Geo_Location

"""The Data Looks ready for Analysis from this point forward. The Data Preparation concluded with Data Cleaning to have appropriate Data for the analysis section

**DATA ANALYSIS**
"""

# 1. TELCOM DATASETS
# a) Analysing Product Use per Day
# Let's see the VALUE totals of each day first, before any other operation
print(Telcom1['VALUE'].sum())
print(Telcom2['VALUE'].sum())
print(Telcom3['VALUE'].sum())

# First we get the product use totals of each day.
Products_in_Telcom1 = Telcom1.groupby('PRODUCT')['VALUE'].sum()
for key, value in Products_in_Telcom1.iteritems():
  PRODUCT_NAME = key
  print(key, value)

Products_in_Telcom2 = Telcom2.groupby('PRODUCT')['VALUE'].sum()
for key, value in Products_in_Telcom2.iteritems():
  PRODUCT_NAME = key
  print(key, value)

Products_in_Telcom3 = Telcom3.groupby('PRODUCT')['VALUE'].sum()
for key, value in Products_in_Telcom3.iteritems():
  PRODUCT_NAME = key
  print(key, value)

# b) Analysing Date_Time Product Usage

Day_1_1st_hour = Telcom1[Telcom1['DATE_TIME'].map(lambda Time: '2012-05-06 23' in Time)] # get the 1st hour of first DataSheet
Day_1_2nd_hour = Telcom1[Telcom1['DATE_TIME'].map(lambda Time: '2012-05-07' in Time)] # get the remaining hour
print(Day_1_1st_hour.groupby('PRODUCT')['VALUE'].sum())
Day_1_2nd_hour.groupby('PRODUCT')['VALUE'].sum()

print(Telcom2)
Day_2_1st_hour = Telcom2[Telcom2['DATE_TIME'].map(lambda Time: '2012-05-07 23' in Time)] # get the 1st hour of second DataSheet
Day_2_2nd_hour = Telcom2[Telcom2['DATE_TIME'].map(lambda Time: '2012-05-08' in Time)] # get the remaining hour
print(Day_2_1st_hour.groupby('PRODUCT')['VALUE'].sum())
Day_2_2nd_hour.groupby('PRODUCT')['VALUE'].sum()

print(Telcom3)
Day_3_1st_hour = Telcom3[Telcom3['DATE_TIME'].map(lambda Time: '2012-05-08 23' in Time)] # get the 1st hour of third DataSheet
Day_3_2nd_hour = Telcom3[Telcom3['DATE_TIME'].map(lambda Time: '2012-05-09' in Time)] # get the remaining hour
print(Day_3_1st_hour.groupby('PRODUCT')['VALUE'].sum())
Day_3_2nd_hour.groupby('PRODUCT')['VALUE'].sum()

# c) Merging the 3 days along the 2 different timeframes

Hour_1 = pd.concat((Day_1_1st_hour, Day_2_1st_hour, Day_3_1st_hour), axis=0, ignore_index=True)
print('1st Hour sum: ', Hour_1['VALUE'].sum())

Hour_2 = pd.concat((Day_1_2nd_hour, Day_2_2nd_hour, Day_3_2nd_hour), axis=0, ignore_index=True)
print('2nd Hour sum: ', Hour_2['VALUE'].sum())

print('1st Hour Summary:\n',Hour_1['VALUE'].describe())
print('2nd Hour Summary:\n',Hour_2['VALUE'].describe())

# The result of the summations is as expected from the EVALUATION section of the CRISP-DM Repot.

# 2 Location Dataset
# a) Analysing In Service Stations
# First we get rid of the out of service station as the goal is to upgrade existing
# infrastructure, not to repair out of service ones.

# Location_Geo = Geo_Location[Geo_Location['STATUS'] == 'In Service']
# Location_Geo = Geo_Location.groupby(['VILLES'])

# This shows the top VILLES with most in service stations and therefore could be the priority list
Geo_Location['VILLES'].value_counts().head(50)

# b) Merging Location Dataset to Telecom Datasets
# First is determining whether SITE CODE on Location Dataset is similar to SITE ID on Telcom Datasets
Test = Geo_Location['SITE_CODE']
Telcom.loc[Telcom['SITE_ID'].isin(Test)]
Geo_Location[Geo_Location['SITE_CODE'] == '1b5540c02d']
# It proves to be true.

# Rename SITE_CODE to SITE_ID to match the Telcom Data SET

Geo_Location.columns = ['VILLES', 'STATUS', 'LOCALISATION', 'DECOUPZONE', 'ZONENAME',
                        'LONGITUDE', 'LATITUDE', 'REGION','AREA', 'CELL_ID', 'SITE_ID']
Geo_Location

# Merge both Hours Data into one
print(Hour_1)
print(Hour_2)
Telcom_hours = pd.concat((Hour_1, Hour_2), axis=0, ignore_index=True)
Telcom_hours

# Merging the 2 datasets Telecom and Location
Telecommunications = Telcom_hours.merge(Geo_Location, how= 'inner', on='SITE_ID')
# Drop unnecessary columns
Telecommunications = Telecommunications.drop(['CELL_ID_x', 'LONGITUDE', 'LATITUDE', 'CELL_ID_y'], axis= 1)
Telecommunications

# Summary of the Dataset
Telecommunications['VALUE'].describe()

# Determining the priority list from the 75th percentile.
Priority = Telecommunications[Telecommunications['VALUE'] > 50]
Priority = Priority.sort_values(by= 'VALUE', ascending=0)
Priority

Optimum_Priority = Priority.groupby('VILLES')['VALUE'].sum().sort_values(ascending=False)
Optimum_Priority.head(50)

"""RECOMMENDATION

The Priority list of the 100 top VILLES to be upgraded first was achieved. These Areas should have their infrastructure upgraded first as they are the areas with the most customer engagement, hence value for money as Return On Investment will be quicker.Voice and SMS infrastructure can be upgraded at the same time. They can be upgraded first as was determined by their extensive usage in the second time frame (after 00:00 hrs). The Data infrastructure can be upgraded later since it is used primarily in the first time frame (23:00 hrs - 00:00 hrs). If all products infrastructure need to be upgraded at the same time, the best time to upgrade would be along the first time frame i.e. before 00:00 hrs, since this will only affect the Data Product users, who are a much smaller contributor to the Network in general, as per the data given.
"""
