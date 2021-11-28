#store image data in mongodb
from pymongo import MongoClient
from PIL import Image
import io
import os
import time
import pandas as pd

client = MongoClient()
db = client.agmarknet_dataaa
df= {}

rootdir = 'C:/Users/dell/PycharmProjects/Scraping/color'
l = []
for subdir, dirs, files in os.walk(rootdir):
    for file in dirs:
        start_time= time.time()
        #print(file)
        l.append(file)
        images = db['{}'.format(file)]
        #break
        directory = rootdir+'/'+ file

        # iterate over files in
        # that directory
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            # checking if it is a file
            if os.path.isfile(f):


                im = Image.open(f)
                im = im.convert('RGB')
                image_bytes = io.BytesIO()
                im.save(image_bytes, format='JPEG')

                image = {
                    'data': image_bytes.getvalue()
                }

                image_id = images.insert_one(image).inserted_id

        totaltime=time.time()-start_time
        df[file]=totaltime
        print(df)

print(df)

