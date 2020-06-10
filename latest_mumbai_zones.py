import urllib.request
from tabula import read_pdf
import pandas as pd

def get_latest_data():
    
    print('-------Crawling mcgm.gov for latest zones update-----------')
    
    pincode_mumbai = pd.read_csv('mumbai_pincodes.csv')
    pincode_mumbai['Pincode']=pincode_mumbai['Pincode'].astype(str)
    
    url = 'https://stopcoronavirus.mcgm.gov.in/assets/docs/Containment-Zones.pdf'
    urllib.request.urlretrieve(url,'download.pdf')
    df = read_pdf('download.pdf',pages='all', stream=True,silent=False,guess=False)
    sub_df = pd.DataFrame()
    for ix in range(len(df)):
        #print(i)
        df1 = pd.DataFrame(df[ix])
        df1 = df1.drop([0,1,2],axis=0).reset_index(drop=True)
        df1.columns = ['Containment_zones']
        df1[['ward','no','pin','address']] = df1.Containment_zones.str.split(' ',3,expand=True)
        idx = df1[~(df1.pin.isin(pincode_mumbai['Pincode'].unique()))]
        if len(idx)>0 :
            for i in idx.index:
                if df1.iloc[i-1,4] ==None:
                    df1.iloc[i-1,4] = str(df1.iloc[i,4])
                else:
                    df1.iloc[i-1,4] = str(df1.iloc[i-1,4]) + ' ' + str(df1.iloc[i,4])
        df1 = df1.drop(idx.index,axis=0).reset_index(drop=True)
        sub_df = sub_df.append(df1,ignore_index=True)

    url = 'https://stopcoronavirus.mcgm.gov.in/assets/docs/Sealed-Buildings.pdf'
    urllib.request.urlretrieve(url,'download_apartment.pdf')
    df = read_pdf('download_apartment.pdf',pages='all', stream=True,silent=False,guess=False)
    sub_df_apartment = pd.DataFrame()
    for ix in range(len(df)):
        df1 = pd.DataFrame(df[ix])
        df1 = df1.drop([0,1,2],axis=0).reset_index(drop=True)
        df1.columns = ['Containment_zones']
        df1[['ward','no','pin','address']] = df1.Containment_zones.str.split(' ',3,expand=True)
        idx = df1[~(df1.pin.isin(pincode_mumbai['Pincode'].unique()))]
        if len(idx)>0 :
            for i in idx.index:
                if df1.iloc[i-1,4] ==None:
                    df1.iloc[i-1,4] = str(df1.iloc[i,4])
                else:
                    df1.iloc[i-1,4] = str(df1.iloc[i-1,4]) + ' ' + str(df1.iloc[i,4])
        df1 = df1.drop(idx.index,axis=0).reset_index(drop=True)
        sub_df_apartment = sub_df_apartment.append(df1,ignore_index=True)
    print('----------Data Extracted -----------')    
    return(sub_df,sub_df_apartment)