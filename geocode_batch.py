#Geocoding 

#Generating Access token
import requests
from collections import defaultdict
import csv
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

def geocode(sub):
    
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
    index = [0]
    geo_df = pd.DataFrame()
    for i in range(len(sub)):
            #print(i)
            r.params = {'address':str(sub.iloc[i]['address'])+", Mumbai "+str(sub.iloc[i]['pin'])}
            s=r.get(url3)
            if s.status_code!=200:
                continue
            else :
                try:
                    s = s.json()
                    geo_df = geo_df.append(pd.DataFrame(s).T)

                except :
                    continue
    geo_df = geo_df.reset_index(drop=True)
    return(geo_df)