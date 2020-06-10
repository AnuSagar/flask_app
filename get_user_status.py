import pandas as pd
import requests
import time
import numpy as np

def haversine_distance(lat1, lon1, lat2, lon2):
    r = 6371
    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    delta_phi = np.radians(lat2 - lat1)
    delta_lambda = np.radians(lon2 - lon1)
    a = np.sin(delta_phi / 2)**2 + np.cos(phi1) * np.cos(phi2) *   np.sin(delta_lambda / 2)**2
    res = r * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))
    return np.round(res, 2)
    
#Geocoding 
def get_geocode(address) :
    #Generating Access token
    import requests
    from collections import defaultdict
    import csv
    import warnings
    warnings.filterwarnings('ignore')

    url2 = 'https://outpost.mapmyindia.com/api/security/oauth/token'
    url3 = 'https://atlas.mapmyindia.com/api/places/geocode?'

    outh_param = {'grant_type': 'client_credentials','client_id':'9lqokcL6ssAAF4mo1b8CxH53HS9tcBZa5ltzowyohPYQ64anPv43hBlBZkfSgAzlIjC_Az0r1AEUKQn3wNkkPg==',
             'client_secret':'ebEc8GH231ekzQXZTJ8w8GSwg7wcjqDpJhvKR16NgBaH1eePC9nyXsKaSoA5UPLNGllXRctvuqU6tmmHhCCLTj-3LustFdXz'}

    #use the 'auth' parameter to send requests with HTTP Basic Auth:

    r = requests.post(url=url2, data = outh_param,verify=False)
    access_token = r.json()['access_token']

    hed = {'Authorization':access_token}

    res = defaultdict(list)
    r = requests.Session()
    r.headers = hed
    r.verify=False

    #Gepcode data
    r.params = {'address':address}
    s=r.get(url3)
    if s.status_code!=200:
        print('error')
    else :
        try:
            s = s.json()
            geo_userdf = pd.DataFrame(s).T
        except:
            print('Address not geocoded')
    return(geo_userdf)        

def calc_status(address,geo_df):
    geo_userdf = get_geocode(address)
    distances_km = []
    for row in geo_df.itertuples(index=False):
        distances_km.append(
           haversine_distance(geo_userdf.iloc[0]['latitude'], geo_userdf.iloc[0]['longitude'], row.latitude, row.longitude)
       )
    geo_df['DistanceFromUserLoc'] = distances_km
    geo_df['DistanceFromUserLoc'] = geo_df['DistanceFromUserLoc']*1000
    #geo_df = geo_df.sort_values('DistanceFromUserLoc').reset_index(drop=True)
    #print(geo_df['DistanceFromUserLoc'].min())
    if geo_df['DistanceFromUserLoc'].min() <=100:
        status='red'
    elif (geo_df['DistanceFromUserLoc'].min() > 100) & (geo_df['DistanceFromUserLoc'].min() <=250):
        status = 'amber'
    else : status = 'green'    
    return 'STATUS : ' + str(status).upper() + ' | User is '+ str(geo_df['DistanceFromUserLoc'].min()) + ' meters away from containment zone'
    
def get_user_add_status(address):
    print('user address')
    #address = 'Omkar Alta monte, Malad East, Mumbai 400097'
    return calc_status(address,pd.read_csv('mumbai_400001.csv'))
    