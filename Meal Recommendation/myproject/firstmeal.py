import pandas as pd
import numpy as np
import scipy.stats
from myproject.models import User, Breakfast, LunchDinner
from myproject import db
from collections import defaultdict

def query_to_dict(rset):
    result = defaultdict(list)
    for obj in rset:
        instance = db.inspect(obj)
        for key, x in instance.attrs.items():
            result[key].append(x.value)
    return result


def meal(cuisine,meal,calorie,hascancer,hasdiabetes,df2):
    if hascancer=='Y':
        for index,i in df2.iterrows():
            if (i['Fiber']>15) or (('high fiber') in i['soup']):
                continue
            else:
                df2.drop(index,inplace=True)
    if hasdiabetes=='Y':
        for index,i in df2.iterrows():
            if 'diabet' not in i['soup']:
                df2.drop(index,inplace=True)
    
    if hascancer!='Y' and hasdiabetes !='Y':
        for index,i in df2.iterrows():
            if cuisine not in i['soup']:
                df2.drop(index,inplace=True)
    
    for index,i in df2.iterrows():
        if (calorie+50>i['Calories'] and calorie-200<i['Calories']):
            continue
        else:
            df2.drop(index,inplace=True)
    lst=[]
    if meal=='breakfast':
        lst.append(int(df2.sample()['ID'].iloc[0]))
        return lst
    else:
        lst.append(int(df2.sample()['ID'].iloc[0]))
        temp=int(df2.sample()['ID'].iloc[0])
        while temp==lst[0]:
            temp=int(df2.sample()['ID'].iloc[0])
        lst.append(temp)
        return lst

def generatemeal(age,height,weight,exercise,sex,hascancer,hasdiabetes,cuisine):
    BMR=0
    if sex=='M':
      BMR = 13.397*weight + 4.799*height - 5.677*age + 88.362  
    else:
        BMR = 9.247*weight + 3.0988*height - 4.330*age + 447.593
#     print(BMR)
#  Sedentary (little or no exercise) : Calorie-Calculation = BMR x 1.2
# Lightly active (light exercise/sports 1-3 days/week) : Calorie-Calculation = BMR x 1.375
# Moderately active (moderate exercise/sports 3-5 days/week) : Calorie-Calculation = BMR x 1.55
# Very active (hard exercise/sports 6-7 days a week) : Calorie-Calculation = BMR x 1.725
# If you are extra active (very hard exercise/sports & a physical job) : Calorie-Calculation = BMR x 1.9
    calorie=BMR*exercise
    
    #instead of path add your code to import from sql
    dfb=pd.read_csv('myproject/data/Breakfast.csv',encoding='latin-1')
    rset = Breakfast.query.all()  
    dfb = pd.DataFrame(query_to_dict(rset))
    # dfb=pd.read_csv('Breakfast.csv')  
    dfb2=dfb.copy()
    breakfastlst=meal(cuisine,'breakfast',1/7*calorie,hascancer,hasdiabetes,dfb)
    
    dfl=pd.read_csv('myproject/data/LunchDinner.csv',encoding='latin-1')
    rset = LunchDinner.query.all()  
    dfl = pd.DataFrame(query_to_dict(rset))
    # dfl=pd.read_csv('LunchDinner.csv')
    dfl2=dfl.copy()

    lunchlst=meal(cuisine,'lunch',2/10*calorie,hascancer,hasdiabetes,dfl)
    breakfastlst.extend(lunchlst)
    
    dfb2.drop(columns=['soup'], inplace=True)
    dfl2.drop(columns=['soup'], inplace=True)
    
    dfm = dfb2.loc[dfb2['ID'] == breakfastlst[0]]
    
    print(dfm)
    for i in range(1,len(breakfastlst)):
        dfm = pd.concat([dfm, dfl2.loc[dfl2['ID'] == breakfastlst[i]]], ignore_index=True)
    lstDoc = dfm.to_dict('records')
    return lstDoc, breakfastlst
#     return breakfastlst