import pandas as pd
import re

def fuses_terrace(abcd):
    # removing Terrasse Surface columns by adding it to Terrace
    abcd["Terrace"] = abcd["Terrace"].replace("Yes", 1).fillna(0)
    abcd["Terrace surface"] = abcd["Terrace surface"].str.extract(r"([0-9]{1,3})").astype(float)
    abcd["Terrace"] = abcd[["Terrace", "Terrace surface"]].sum(axis=1, skipna=False).fillna(0)
    return abcd

def fuses_garden(abcd):
    # remonving Garden Surface column by adding it to Garden
    abcd["Garden"] = abcd["Garden"].replace("Yes", 1).fillna(0)
    abcd["Garden surface"] = (
        abcd["Garden surface"].str.extract(r"([0-9]{2,5})").astype(float)
    )
    abcd["Garden"] = abcd[["Garden", "Garden surface"]].sum(axis=1, skipna=False).fillna(0)

    return abcd

def clean_price(abcd):
    abcd["Price"] = abcd["Price"].str.extract(r"([0-9]{4,7})").astype(float)
    return abcd

def clean_liv_room_surf(abcd):
    abcd["Living room surface"] = (
        abcd["Living room surface"].str.extract(r"([0-9]{1,5})").astype(float)
    )
    return abcd

def clean_liv_area(abcd):
    abcd["Living area"] = abcd["Living area"].str.extract(r"([0-9]{1,5})").astype(float)
    return abcd

def clean_df(abcd):
    abcd = fuses_terrace(fuses_garden(clean_price(clean_liv_area(clean_liv_room_surf(abcd)))))
    abcd = abcd.fillna("None")
    abcd = abcd.replace(["Yes", "No"], [1, 0])
    abcd = abcd.drop(columns=["Terrace surface", "Garden surface", "Address"])
    abcd['building_subtype'] = abcd['building_type']
    abcd['building_type'] = abcd['building_subtype'].apply(lambda x: 'house' if x in ['house', 'villa', 'mansion', 'manor-house', 'country-cottage', 'town-house', 'chalet', 'farmhouse'] else ('apartment' if x in ['apartment', 'loft', 'flat-studio', 'duplex', 'service-flat', 'apartment-block', 'triplex', 'penthouse', 'ground-floor', 'kot'] else 'other-property'))
    ranking_dict= {
        'Good':2, 
        'As new':3, 
        'To be done up':0, 
        'To renovate':1, 
        'Just renovated':3, 
        'To restore':1,
        'Installed':1,
        'Hyper equipped': 3, 
        'USA hyper equipped' : 3,
        'Semi equipped':2,
        'USA installed':1, 
        'Not installed':0, 
        'USA semi equipped':2, 
        'USA uninstalled':0
    }
    abcd.replace({'Kitchen type' : ranking_dict}, inplace=True)
    abcd.replace({"Building condition" : ranking_dict}, inplace=True)


    return abcd

# new_columns.loc["Basement":"Monthly charges"]

if __name__=='__main__':
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

    old_csv = pd.read_csv("../assets/immoweb_properties_data.csv")

    good_csv = old_csv[old_csv["url"].str.contains("new-real-estate-project") == False]

    new_columns = good_csv[columns]
    test = new_columns.dropna(subset=["Living area", "Bedrooms", "Price"])

    abcd = test.fillna({"Furnished": "None", "Elevator": "None", "Swimming pool": "None"})
    abcd = clean_df(abcd)

    abcd.to_csv("assets/test.csv")