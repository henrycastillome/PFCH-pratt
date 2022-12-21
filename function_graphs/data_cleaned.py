"""data cleaned for critical flga """
import os
import pandas as pd  # primary data structure library

from dotenv import load_dotenv


load_dotenv()
mapbox_key = os.environ['apikey']


pd.options.mode.chained_assignment = None

DATA_PATH = '/Users/henrycastillomelo/Documents/Full stack Bootcamp/Course 7 Ptyhon for Data science, AI and else/remainings project pratt/DOHMH_New_York_City_Restaurant_Inspection_Results (1).csv'
restaurants_data = pd.read_csv(DATA_PATH)

restaurants_data.columns = list(map(str, restaurants_data.columns))


# droping unnecesary columns

restaurants_data.drop(['CAMIS', 'Police Precincts', 'City Council Districts', 'Borough Boundaries', 
                        'Community Districts', 'Zip Codes', 'Location Point', 'NTA', 'BBL', 'BIN', 'Census Tract',
                      'Council District', 'Community Board', 'PHONE', 'ZIPCODE', 'Latitude', 'Longitude',
                      'SCORE', 'GRADE', 
                      'ACTION', 'VIOLATION CODE', 'GRADE DATE', 'RECORD DATE', 'INSPECTION TYPE'], axis=1, inplace=True)


# renaming a columns
restaurants_data.rename(columns={'DBA': 'RESTAURANT'}, inplace=True)

restaurants_data.rename(columns={'BORO': 'BOROUGH'}, inplace=True)


# dropping NaN values
restaurants_data.dropna(subset=['RESTAURANT'], inplace=True)


print(restaurants_data['CUISINE DESCRIPTION'].value_counts())

# critical_data = restaurants_data[(restaurants_data['CRITICAL FLAG'] != 'Not Critical') & (
#     restaurants_data['CRITICAL FLAG'] != "Not Applicable")]

# restaurants_data.to_csv('restaurant_data_table.csv', index=False)
