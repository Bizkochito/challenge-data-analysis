import re
import pandas as pd
import urllib.parse

def extract_from_url(url):
    list_url = url.split("/")
    building_type = list_url[5]
    municipality=list_url[7]
    zipcode= int(list_url[8])
    immoweb_id = int(list_url[9])
    return [building_type, municipality, zipcode, immoweb_id]

def get_id(url):
    return extract_from_url(url)[3]
def get_type(url):
    return extract_from_url(url)[0]
def get_municipality(url):
    return urllib.parse.unquote(extract_from_url(url)[1]).lower()
def get_zipcode(url):
    return extract_from_url(url)[2]

def split_url_info(df):
    df['id'] = df['url'].apply(get_id)
    df['building_type'] = df['url'].apply(get_type)
    df['municipality'] = df['url'].apply(get_municipality)
    df['zipcode'] = df['url'].apply(get_zipcode)
    df = df.set_index('id', drop = True)
    df = df.drop('url', axis = 1)
    return df


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

def discriminate_province(zipcode):
    short_zip= zipcode/100
    if short_zip<13:
        return 'Brussels Capital Region'
    if short_zip<15:
        return 'Walloon Brabant'
    if short_zip<20 or 29<short_zip<35 :
        return 'Flemish Brabant'
    if short_zip<30:
        return 'Antwerp'
    if short_zip<40:
        return 'Limburg'
    if short_zip<50:
        return 'Liège'
    if short_zip<60:
        return 'Namur'
    if short_zip<66 or 69<short_zip<80:
        return 'Hainaut'
    if short_zip<70:
        return 'Luxembourg'
    if short_zip<90:
        return 'West Flanders'
    else:
        return 'East Flanders'


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
        'USA uninstalled':0,
        'A' : 7,
        'B' : 6,
        'C' : 5,
        'D' : 4,
        'E' : 3,
        'F' : 2,
        'G' : 1,
        'Not specified':1, 
        'A+': 7.25, 
        'A++': 7.5
    }
    abcd.replace({'Kitchen type' : ranking_dict}, inplace=True)
    abcd.replace({"Building condition" : ranking_dict}, inplace=True)
    abcd.replace({'Energy class' : ranking_dict}, inplace=True)

    zip_codes = pd.read_csv('assets/zipcode-belgium.csv')
    codes_dict = dict(zip(zip_codes['postcode'], zip_codes['municipality']))

    abcd['group_zipcode'] =abcd['zipcode'].apply(lambda x: x - x%10)

    abcd['municipality'] = abcd['group_zipcode']
    abcd.replace({'municipality' : codes_dict}, inplace=True)
    abcd['province'] = abcd['zipcode'].apply(discriminate_province)

    return abcd



if __name__== "__main__":
    df = pd.read_csv('assets/immoweb_properties_data.csv')
    df = split_url_info(df)
    print(df.head())

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