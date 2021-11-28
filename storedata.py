import pymongo
import pandas as pd
import json
import time


li=['WB_Onion.csv']
client = pymongo.MongoClient("mongodb://localhost:27017")

start_time= time.time()
for i in li:
    df = pd.read_csv(i)
    df['state'] = 'WB'
    df=df.iloc[:,1:11]
    df.columns=['District_Name','Market_Name','Commodity','Variety','Grade','Min_Price','Max_Price','Modal_Price','Date','state']

    print(df.head())
    data= df.to_dict(orient="records")
    db= client["agmarknet_data"]
    db.mix_data.insert_many(data)

totaltime=time.time()-start_time
print(totaltime)
