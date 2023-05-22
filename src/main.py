import pandas as pd
import re

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

old_csv = pd.read_csv(".\\assets\immoweb_properties_data.csv")

good_csv = old_csv[old_csv["url"].str.contains("new-real-estate-project") == False]

new_columns = good_csv[columns]

purified_csv = new_columns.to_csv(".\\assets\\new.csv")

new_columns.dropna()
new_columns.fillna("None")
new_columns.loc["Basement":"Monthly charges"]
