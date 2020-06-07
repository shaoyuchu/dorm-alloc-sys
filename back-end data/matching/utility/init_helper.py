import sys
import random
sys.path.insert(0, '../handler/')
from student_handler import Student
from room_handler import Room
from static.config import PREFERENCE_DICT, NATIONALITIES, LOCAL_NATIONALITY

def preprocess_df(df):
    df = df.rename({"學號":"ID","性別":"gender","區域志願1":"pref_1","區域志願2":"pref_2","區域志願3":"pref_3","戶籍地":"nationality"}, axis="columns")
    print(df.columns)
    df.replace(PREFERENCE_DICT, inplace=True)
    df.loc[df["nationality"] != "境外", 'nationality']= LOCAL_NATIONALITY
    df.replace({"男性":1, "女性":0}, inplace=True)
    
    #only for debug
    new_nationalities = []
    for stud_index in range(len(df)):
        if(df.iloc[stud_index]['nationality']!=LOCAL_NATIONALITY):
            new_nationalities.append(random.choice(NATIONALITIES))
        else:
            new_nationalities.append(df.iloc[stud_index]['nationality'])

    df["nationality"] = new_nationalities
    df["ID"] = [i for i in range(len(df))]
    print(df.head())
    print("There are {} students ".format(len(df)))
    return df

def df2object_student(df, gender):
    students_lis = []
    for i in range(len(df)):
        attris = dict(df.iloc[i])
        s = Student(_id=attris['ID'],nationality = attris['nationality'], preferences = [attris['pref_1'], attris['pref_2'], attris['pref_3']], gender=gender)
        students_lis.append(s)
    return students_lis

def df2object_rooms(ROOMNUM, room_quota):
    all_rooms_lis = []
    room_nums = [i for i in range(1, 1+ROOMNUM)]
    i = 0
    for _type in room_quota.keys():
        for num in range(room_quota[_type]):
            r = Room(gender=1, room_num=room_nums[i], _type = _type)
            all_rooms_lis.append(r)
            i+=1
    return all_rooms_lis

def object2df_student(studData, objs):
    IDs = []
    for obj in objs:
        IDs.append(obj._id)
    return studData[studData["ID"].isin(IDs)]