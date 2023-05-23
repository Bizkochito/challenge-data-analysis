import pandas as pd
import re
from utils.cleaning_gregoire import split_url_info


columns = [
    "Construction year",
    "Building condition",
    "Number of frontages",
    "Surroundings type",
    "Living area",
    "Living room surface",
    "Kitchen type",
    "Kitchen surface",
    "Bedrooms",
    "Bathrooms",
    "Shower rooms",
    "Toilets",
    "Basement",
    "Furnished",
    "Terrace",
    "Elevator",
    "Accessible for disabled people",
    "Swimming pool",
    "Energy class",
    "Heating type",
    "Double glazing",
    "Price",
    "Address",
    "Covered parking spaces",
    "Flood zone type",
    "Neighbourhood or locality",
    "Outdoor parking spaces",
    "Garden surface",
    "Terrace surface",
    "Garden",
    "Monthly charges",
]

base_csv = pd.read_csv(".\\assets\immoweb_properties_data.csv")

df = base_csv[base_csv["url"].str.contains("new-real-estate-project") == False]
df = split_url_info(df)

new_columns = df[columns]


"""
purified_csv = new_columns.to_csv(".\\assets\\new.csv")
new_columns.loc["Basement":"Monthly charges"]
"""