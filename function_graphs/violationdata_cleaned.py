"""Restaurant inspection dataset cleaned"""
import pandas as pd


pd.options.mode.chained_assignment = None

DATA_PATH='/Users/henrycastillomelo/Documents/Full stack Bootcamp/Course 7 Ptyhon for Data science, AI and else/Project Pratt/DOHMH_New_York_City_Restaurant_Inspection_Results (1).csv'
restaurants_data=pd.read_csv(DATA_PATH)

restaurants_data.columns = list (map(str, restaurants_data.columns))


#droping unnecesary columns

restaurants_data.drop(['CAMIS','Police Precincts', 'City Council Districts',
                        'Borough Boundaries', 'Community Districts', 'Zip Codes',
                        'Location Point', 'NTA', 'BBL', 'BIN', 'Census Tract',
                        'Council District', 'Community Board' ], axis=1, inplace=True)

#renaming a columns
restaurants_data.rename(columns={'DBA':'RESTAURANT'}, inplace=True)

#dropping NaN values
restaurants_data.dropna(subset=['VIOLATION DESCRIPTION'], inplace=True)
#total restaurants
print(restaurants_data.shape)

#creating a new dataframe with  violation description to create a w
violation=restaurants_data[['VIOLATION DESCRIPTION']]

#check colum types

print(all(isinstance(column, str) for column in violation.columns))

#shortening the violation to better visualization

violation.replace(to_replace='Non-food contact surface improperly constructed. Unacceptable material used. Non-food contact surface or equipment improperly maintained and/or not properly sealed, raised, spaced or movable to allow accessibility for cleaning on all sides, above and underneath the unit.',
                   value='Improper non-food contact surface' , inplace=True)

violation.replace(to_replace='Facility not vermin proof. Harborage or conditions conducive to attracting vermin to the premises and/or allowing vermin to exist.',
                   value='Not vermin proof ' , inplace=True)

violation.replace(to_replace='Food contact surface not properly washed, rinsed and sanitized after each use and following any activity when contamination may have occurred.',
                   value='Food contact surface not properly washed ' , inplace=True)

violation.replace(to_replace="Evidence of mice or live mice present in facility's food and/or non-food areas.",
                   value='Live mice present' , inplace=True)

violation.replace(to_replace='Food not protected from potential source of contamination during storage, preparation, transportation, display or service.',
                   value='Food not protected from contamination ' , inplace=True)

violation.replace(to_replace="Cold food item held above 41º F (smoked fish and reduced oxygen packaged foods above 38 ºF) except during necessary preparation.",
                   value='Cold food item held above 41º F' , inplace=True)

violation.replace(to_replace='Plumbing not properly installed or maintained; anti-siphonage or backflow prevention device not provided where required; equipment or floor not properly drained; sewage disposal system in disrepair or not functioning properly.',
                   value='Plumbing not properly installed or maintained ' , inplace=True)

violation.replace(to_replace="Filth flies or food/refuse/sewage-associated (FRSA) flies present in facility’s food and/or non-food areas.  Filth flies include house flies, little house flies, blow flies, bottle flies and flesh flies.  Food/refuse/sewage-associated flies include fruit flies, drain flies and Phorid flies.",
                   value="flies present in facility’s food" , inplace=True)

violation.replace(to_replace="Non-food contact surface or equipment made of unacceptable material, not kept clean, or not properly sealed, raised, spaced or movable to allow accessibility for cleaning on all sides, above and underneath the unit.",
                   value="Non-food equipment made of acceptable material" , inplace=True)

violation.replace(to_replace="Raw, cooked or prepared food is adulterated, contaminated, cross-contaminated, or not discarded in accordance with HACCP plan.",
                   value='Raw or cooked food contaminated'  , inplace=True)

violation.replace(to_replace="Establishment is not free of harborage or conditions conducive to rodents, insects or other pests.",
                   value=' Establishment is not free of harborage to  animals'  , inplace=True)


#sample size the first 5 highers values, counting them and converting to a frame


violation=violation['VIOLATION DESCRIPTION'].value_counts().to_frame().head(5)


#creating a new panda frame to take the total values in a new column and rename the column
violation_data=pd.DataFrame(violation)

#reseting the index to rename the columns

VIOLATION_DATA=violation_data.reset_index()
#renaming the columns

violation_data.rename(columns={'index':'VIOLATION', 'VIOLATION DESCRIPTION':'Total'}, inplace=True)

#setting the violation as index

violation_data.set_index("VIOLATION", inplace=True)
