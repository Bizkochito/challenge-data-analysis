import pandas as pd
import re

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
    "Address",
    "Flood zone type",
    "Neighbourhood or locality",
    "Outdoor parking spaces",
    "Garden surface",
    "Terrace surface",
    "Garden",
    "Monthly charges",
]

old_csv = pd.read_csv("assets/immoweb_properties_data.csv")

good_csv = old_csv[old_csv["url"].str.contains("new-real-estate-project") == False]

new_columns = good_csv[columns]
missing_values = new_columns.isnull().sum()

purified_csv = new_columns.to_csv("assets/new.csv")
missing_values_csv = missing_values.to_csv("assets/missing_values.csv")


# new_columns.dropna()
# new_columns.fillna("None")
# new_columns.loc["Basement":"Monthly charges"]
