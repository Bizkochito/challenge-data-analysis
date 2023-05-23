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
    "Garden surface",
    "Terrace surface",
    "Garden",
]

old_csv = pd.read_csv("assets/immoweb_properties_data.csv")

good_csv = old_csv[old_csv["url"].str.contains("new-real-estate-project") == False]

new_columns = good_csv[columns]
missing_values = new_columns.isnull().sum()

purified_csv = new_columns.to_csv("assets/new.csv")
missing_values_csv = missing_values.to_csv("assets/missing_values.csv")


test = new_columns.dropna(subset=["Living area", "Bedrooms", "Price"])
abcd = test.fillna({"Furnished": "None", "Elevator": "None", "Swimming pool": "None"})


# removing Terrasse Surface columns by adding it to Terrace
abcd["Terrace"] = abcd["Terrace"].replace("Yes", 1).fillna(0)
abcd["Terrace surface"] = (
    abcd["Terrace surface"].str.extract(r"([0-9]{1,3})").astype(float)
)
abcd["Terrace"] = (
    abcd[["Terrace", "Terrace surface"]].sum(axis=1, skipna=False).fillna(0)
)

# remonving Garden Surface column by adding it to Garden
abcd["Garden"] = abcd["Garden"].replace("Yes", 1).fillna(0)
abcd["Garden surface"] = (
    abcd["Garden surface"].str.extract(r"([0-9]{2,5})").astype(float)
)
abcd["Garden"] = abcd[["Garden", "Garden surface"]].sum(axis=1, skipna=False).fillna(0)
abcd = abcd.drop(columns=["Terrace surface", "Garden surface"])

abcd["Price"] = abcd["Price"].str.extract(r"([0-9]{4,7})").astype(int)

abcd["Living room surface"] = (
    abcd["Living room surface"].str.extract(r"([0-9]{1,5})").astype(float)
)

abcd["Living area"] = abcd["Living area"].str.extract(r"([0-9]{1,5})").astype(int)

abcd = abcd.fillna("None")

abcd = abcd.replace(["Yes", "No"], [1, 0])

abcd.to_csv("assets/test.csv")

# new_columns.loc["Basement":"Monthly charges"]
