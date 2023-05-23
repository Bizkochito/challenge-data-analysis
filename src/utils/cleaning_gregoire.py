import re
import pandas as pd

df = pd.read_csv('assets/immoweb_test.csv')

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
    return extract_from_url(url)[1]
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


if __name__== "__main__":
    df = split_url_info(df)
    print(df.head())
