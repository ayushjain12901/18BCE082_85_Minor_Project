from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.views import APIView
# from .models import Product
import json
from statistics import mean
import pandas as pd
# from .serializers import ProductSerializer
from pymongo import MongoClient
from .utils import *

def home(request):
    return render(request,'home.html')

def ag_data(request):
    if request.method == 'POST':
        commodity= request.POST['Commodity']
        state= request.POST['State']

        x = True
        data,count = get_db_handle(commodity, state) 
        return render(request, 'ag_data.html', {'x': x, 'data': data,'count':count})
    return render(request, 'ag_data.html')

def analytics(request):
    return render(request,'analytics.html')



def get_db_handle1(commodity,state):
    connect_string = 'mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false'
    client = MongoClient(connect_string)
    db_handle = client['agmarknet_data']
    dic={'_id':1,'District_Name':1,'Market_Name':1,'Commodity':1,'Variety':1,'Grade':1,'Min_Price':1,'Max_Price':1,'Modal_Price':1,'Date':1}
    
    collection_name = db_handle[state]    
    grade_list=['Small','Medium','Large','FAQ']
    grade_count=[]
    for i in grade_list:
        guj_details = collection_name.find({'Commodity':commodity,'Grade':i}).count()
        grade_count.append(guj_details)

    return grade_list,grade_count,sum(grade_count)


def commodity_grade(request):
    if request.method == 'POST':
        commodity= request.POST['Commodity']
        state= request.POST['State']

        x = True
        grade_list,grade_count,summ=get_db_handle1(commodity, state)
        chart=get_bargraph(grade_list,grade_count)    
        return render(request,'commodity_grade.html',{'chart':chart,'commodity':commodity,'state':state,'summ':summ})
    return render(request,'commodity_grade.html')

def get_db_handle(commodity,state):
    connect_string = 'mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false'
    client = MongoClient(connect_string)
    db_handle = client['agmarknet_data']
    dic={'_id':1,'District_Name':1,'Market_Name':1,'Commodity':1,'Variety':1,'Grade':1,'Min_Price':1,'Max_Price':1,'Modal_Price':1,'Date':1}

    if commodity!='None' and state!='None':
        collection_name = db_handle[state]    
        guj_details = collection_name.find({'Commodity':commodity})
        return guj_details,guj_details.count()

    elif commodity=='None' and state!=None:
        collection_name = db_handle[state]    
        guj_details = collection_name.find({})
        return guj_details,guj_details.count()
    
    elif commodity!='None' and state=='None':
        states=['Gujarat','WestBengal','Kerala','Jammu']
        dataa=[]
        for i in states:
            collection_name = db_handle[i]    
            guj_details = collection_name.find({'Commodity':commodity})
            dataa.extend(list(guj_details))
        return dataa,guj_details.count()
   

def get_db_handle2(commodity,state):
    connect_string = 'mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false'
    client = MongoClient(connect_string)
    db_handle = client['agmarknet_data']
    
    collection_name = db_handle[state]    
    var_list = list(collection_name.find({'Commodity':commodity}).distinct('Variety'))
    
    per=[]
    total=0
    for i in var_list:
        guj_details = collection_name.find({'Commodity':commodity,'Variety':i}).count()
        per.append(guj_details)
        total=total+guj_details

    for i in range(len(per)):
        per[i]=(per[i]/total)*100
    
    return var_list,per,sum(per)



def commodity_variety(request):
    if request.method == 'POST':
        commodity= request.POST['Commodity']
        state= request.POST['State']
        print('commodity_var')
        x = True
        var_list,var_count,summ=get_db_handle2(commodity,state)
        chart=get_piegraph(var_list,var_count)    
        return render(request,'commodity_variety.html',{'chart':chart,'commodity':commodity,'state':state,'summ':summ})
    return render(request,'commodity_variety.html')


def get_data(c):
    pass

def commodity_modal(request):
    connect_string = 'mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false'
    client = MongoClient(connect_string)
    db_handle = client['agmarknet_data']
    
    if request.method == 'POST':
        state= request.POST['State']
        commodity= request.POST['Commodity']
        x=True
        collection_name = db_handle[state]   
        mar_list = list(collection_name.find({'Commodity':commodity}).distinct('Market_Name'))
        return render(request,'commodity_modal.html',{'x':x, 'mar':mar_list,'state':state,'commodity':commodity})
        print(var_list)
        # print(Mar_list)
    return render(request,'commodity_modal.html')

def commodity_modal1(request):
    connect_string = 'mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false'
    client = MongoClient(connect_string)
    db_handle = client['agmarknet_data']
    
    if request.method == 'POST':
        state= request.POST['State']
        commodity= request.POST['Commodity']
        market= request.POST['Market']
        charts=[]
        collection_name = db_handle[state]
        var_list= list(collection_name.find({'Commodity':commodity,'Market_Name':market}).distinct('Variety'))
        lod=[]
        print(var_list)
        for i in var_list:
            var_listt= list(collection_name.find({'Commodity':commodity,'Market_Name':market,'Variety':i},{'Modal_Price':1,'Date':True}))
            var_listt=list(var_listt)
            dataa=pd.DataFrame(var_listt)
            y=list(dataa['Modal_Price'])
            x=list(dataa['Date'])
            df=pd.DataFrame(zip(x,y),columns=['Date','Modal_Price'])
            lod.append(df)
            #print(df.head)
        if len(lod)<=1:
            pass
        else:
            df3=lod[0]
            for i in range(1,len(lod)):
                df3 = pd.merge(df3,lod[i], how='inner', left_on='Date',right_on='Date')
            print(df3.head())
            charts=get_plot(df3.iloc[:,0],df3.iloc[:,1:],var_list) 
        return render(request,'commodity_modal1.html',{'charts':charts})


    return render(request,'commodity_modal1.html')


def stats(request):
    connect_string = 'mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false'
    client = MongoClient(connect_string)
    db_handle = client['agmarknet_data']

    if request.method == 'POST':
        state= request.POST['State']
        commodity= request.POST['Commodity']
        collection_name = db_handle[state]
        var_list= list(collection_name.find({'Commodity':commodity}).distinct('Market_Name'))
        stats=[]
        x=True
        for i in var_list:
            min_max_data=list(collection_name.find({'Commodity':commodity,'Market_Name':i},{'Min_Price':True,'Max_Price':True,'Modal_Price':True}))
            df_data= pd.DataFrame(min_max_data)
            mini=min(list(df_data['Min_Price']))
            maxi=max(list(df_data['Max_Price']))
            modal=mean(list(df_data['Modal_Price']))
            l=[i,mini,maxi,modal]
            stats.append(l)
        return render(request,'stats_report.html',{'stats':stats,'x':x})


    return render(request,'stats_report.html')

   