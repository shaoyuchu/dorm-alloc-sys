import sys
import random
sys.path.insert(0, '../handler/')
from student_handler import Student
from room_handler import Room
from static.config import PREFERENCE_DICT, NATIONALITIES, LOCAL_NATIONALITY, logging

def preprocess_df(df):
    df = df.rename({'學號':"ID",'性別':'gender','區域志願1': 'pref_1','區域志願2':'pref_2','區域志願3':'pref_3','戶籍地':'nationality','資格':'disability'}, axis="columns")
    logging.debug(df.columns)
    #replace preference columns with symbols
    df.replace(PREFERENCE_DICT, inplace=True)
    df.loc[df["nationality"] != "境外", 'nationality']= LOCAL_NATIONALITY
    df.replace({"男性":1, "女性":0}, inplace=True)
    
    #TODO: remove 身障生, 資格==2
    df = df[df['disability']==1]
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
    return df

def df2object_student(df, gender):
    students_lis = []
    for i in range(len(df)):
        attris = dict(df.iloc[i])
        s = Student(_id=attris['ID'],nationality = attris['nationality'], preferences = [attris['pref_1'], attris['pref_2'], attris['pref_3']], gender=gender)
        students_lis.append(s)
    return students_lis

def df2object_rooms(room_df):
    male_rooms_dict = {}
    female_rooms_dict = {}
    for index in range(len(room_df)):
        gender = 1
        container = male_rooms_dict
        if ("女" in room_df.loc[index]['dormName']):
            container = female_rooms_dict
            gender = 0
        room_num = room_df.loc[index]['Room']
        if (room_df.loc[index]['is_disability']==0):
            # add bed into the existing room
            if (container.get(room_num)):
                if (container[room_num].getDorm() == room_df.loc[index]['dormName']):
                    container[room_num].setAvail(room_df.loc[index]['Bed'])
            # add s new room
            else:
                r = Room(gender=gender, room_num=room_df.loc[index]['Room'], _type = '', available_beds=room_df.loc[index]['Bed'], dorm=room_df.loc[index]['dormName'])
                container[r.getNum()] = r
    return list(male_rooms_dict.values()), list(female_rooms_dict.values())


def object2df_student(studData, objs):
    IDs = []
    for obj in objs:
        IDs.append(obj._id)
    return studData[studData["ID"].isin(IDs)]