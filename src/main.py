import pandas as pd
import re
from utils.immoweb_scraping_cleaning import split_url_info
from utils.immoweb_scraping_cleaning import clean_df

columns = [
    "Building condition",
    "Number of frontages",
    "Surroundings type",
    "Living area",
    "Living room surface",
    "Kitchen type",
    "Bedrooms",
    "Bathrooms",
    "Shower rooms",
    "Toilets",
    "Basement",
    "Furnished",
    "Terrace",
    "Elevator",
    "Swimming pool",
    "Energy class",
    "Heating type",
    "Price",
    "Flood zone type",
    "Garden",
    "zipcode",
    "building_type",
    "building_subtype",
    "municipality",
    'province'
]

df = pd.read_csv("assets/immoweb_properties_data.csv")
df = df[df["url"].str.contains("new-real-estate-project") == False]
df = split_url_info(df)
df = clean_df(df)
df = df[columns]
renaming_dict = {"Construction year": 'year_const',
    "Building condition" : 'status_build',
    "Number of frontages" : 'frontages',
    "Surroundings type" : 'surroundings',
    "Living area" : 'living_area',
    "Living room surface" : 'liv_room_surf',
    "Kitchen type" : 'kitchen_type',
    "Kitchen surface" :'kitchen_surf', 
    "Bedrooms" : 'bedrooms',
    "Bathrooms" : 'bathrooms',
    "Shower rooms" : 'showers',
    "Toilets": 'toilets',
    "Basement": 'basement',
    "Furnished": 'furnished',
    "Terrace": 'terrace',
    "Elevator": 'elevator',
    "Accessible for disabled people": 'disabled_access',
    "Swimming pool": 'swimming_pool',
    "Energy class": 'energy_class',
    "Heating type": 'heating',
    "Double glazing": 'double_glazing',
    "Price": 'price',
    "Address": 'address',
    "Covered parking spaces": 'covered_parking',
    "Flood zone type": 'flood_zone',
    "Neighbourhood or locality": 'locality',
    "Outdoor parking spaces": 'outdoor_parking',
    "Garden surface": 'garden_surf',
    "Terrace surface": 'terrace_surf',
    "Garden": 'garden',
    "Monthly charges": 'monthly_charges'}
df.rename(columns=renaming_dict, inplace=True)

df = df[[     
    'building_type', 
    'building_subtype',
    'price',
    'living_area',
    'frontages', 
    'bedrooms', 
    'bathrooms',
    'liv_room_surf', 
    'kitchen_type',  
    'showers', 
    'toilets', 
    'basement', 
    'terrace',
    'garden', 
    'elevator', 
    'swimming_pool',
    'status_build',
    'furnished',
    'energy_class', 
    'heating', 
    'flood_zone', 
    'surroundings',
    'zipcode', 
    'municipality', 
    'province' ]]




df.to_csv('assets/cleaned_data.csv')
