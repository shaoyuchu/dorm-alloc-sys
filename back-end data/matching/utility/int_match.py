from munkres import Munkres, print_matrix
import pandas as pd
import numpy as np
import random
import math
import argparse
import time

#self-defined
import sys
sys.path.insert(0, '../handler/')
from student_handler import Student
from room_handler import Room
from static.config import PREFERENCE_DICT, NATIONALITIES

all_room_types = list(PREFERENCE_DICT.keys())
all_room_types_symbol = sorted(list(PREFERENCE_DICT.values()))

seed = 30
random.seed(seed)

dataFrame_col = ['ID','pref_1', 'pref_2', 'pref_3','nationality']

#testing
def random_gen_preferences(num):
    data = []
    for s in range(num):
        s_prefs = []
        for pref in range(3):
            s_prefs.extend(random.choices(all_room_types_symbol))
        data.append(s_prefs)
    return data

def random_gen_studentData(STUDENTNUM):
    data = random_gen_preferences(STUDENTNUM)
    students = pd.DataFrame(data=data,columns=dataFrame_col[1:4])
    students[dataFrame_col[4]] = [random.choice(NATIONALITIES) for i in range(STUDENTNUM)]
    students.insert(loc=0, column = dataFrame_col[0], value = [random.randrange(100, 200) for i in range(STUDENTNUM)])
    return students


def get_freq(students_data, col):
    all_data = students_data[col].values
    unique_kind = np.unique(all_data)
    count = {}
    for kind in unique_kind:
        count[kind] =  np.count_nonzero(all_data == kind, axis=None)
    return count

def get_room_type_quota(students_data, ROOMNUM):
    # all_prefs = np.concatenate( (students_data['pref_1'].values, np.concatenate( (students_data['pref_2'].values, students_data['pref_3'].values), axis=None)),axis=None)
    # only consider the first priority when deciding # of rooms for each type
    count = get_freq(students_data, col  = 'pref_1')
    ratio ={key: round(count[key]/sum(count.values()),2) for key in count}
    result = {key: int(ratio[key] * ROOMNUM) for key in ratio}
    #if there are one more or less room, modify the # of rooms of the first type
    if (sum(result.values())> ROOMNUM):
        result[list(result.keys())[0]] -= 1
    elif (sum(result.values()) < ROOMNUM):
        result[list(result.keys())[0]] += 1
    return result

    
def get_country_by_pop(students_data):
    count = get_freq(students_data, col  = 'nationality')
    return sorted([(key, count[key]) for key in count], key=lambda tupl: tupl[1], reverse=True) 
    
def student_by_nation_df(df, gender, sortedNations):
    df_2d = pd.DataFrame()
    for nation, freq in sortedNations:
        nationgroup = df[df['nationality']==nation]
        students_lis = df2object_student(nationgroup, 1)
        df_2d[nation] = pd.Series(students_lis)
        # groupbyPrefs2 = list(nationgroup.groupby('pref_2'))
        # groupbyPrefs3 = list(nationgroup.groupby('pref_3'))
        # nationgroup['']
    return df_2d
    
def int_match(sortedNations, all_rooms_objs, student_by_nation_df):
    res=""
    for room in all_rooms_objs:
        print("matching Room:{}, Type:{}".format(room.getNum(), room.getType()))
        room_type = room.getType()
        priority = 0
        nation_index = 0
        picked_nation = set()

        #放不同國籍相同偏好
        while (priority<3):
            nation_index = 0
            while (nation_index < len(sortedNations)):
                end = False
                #select diff nationalities
                while(sortedNations[nation_index][0] in picked_nation):
                    nation_index+=1
                    if (nation_index >= len(sortedNations)):
                        end = True
                        break
                if (end):
                    break 
                nation = sortedNations[nation_index][0]
                nationgroup = student_by_nation_df[nation]
                for student in nationgroup:
                    if(pd.notnull(student)):
                        #select the same preference
                        if ( student.getPref(priority) == room_type and not student.isArranged()):
                            room.addDweller(student)
                            student.setArranged(True)
                            picked_nation.add(nation)
                            print("success arrange one student!")
                            break
                
                nation_index+=1
                if (nation_index >= len(sortedNations)):
                    break
                if (room.isFull()):
                    break
                
            if (room.isFull()):
                    break
            #if no one has that type as first priority, look for students' second priorities
            priority+=1
        
        #不管偏好，放不同國籍
        if (not room.isFull()):
            nation_index = 0
            while (nation_index < len(sortedNations)):
                #select diff nationalities
                end = False
                while(sortedNations[nation_index][0] in picked_nation):
                    nation_index+=1
                    if (nation_index >= len(sortedNations)):
                        end = True
                        break
                if (end):
                    break  
                nation = sortedNations[nation_index][0]
                nationgroup = student_by_nation_df[nation]
                for student in nationgroup:
                    #select the same preference
                    if(pd.notnull(student)):
                        if (not student.isArranged()):
                            room.addDweller(student)
                            student.setArranged(True)
                            picked_nation.add(nation)
                            print("success arrange one student!")
                            break
                nation_index+=1
                if (nation_index >= len(sortedNations)):
                    break
                if (room.isFull()):
                    break
        
        #同偏好、同國籍
        if (not room.isFull()):
            while (priority<3 & nation_index < len(sortedNations)): 
                nation = sortedNations[nation_index][0]
                nationgroup = student_by_nation_df[nation]
                for student in nationgroup:
                    #select the same preference
                    if(pd.notnull(student)):
                        if (student.getPref(priority) == room_type and not student.isArranged()):
                            room.addDweller(student)
                            student.setArranged(True)
                            picked_nation.add(nation)
                            print("success arrange one student!")
                            break
                nation_index+=1
                if (nation_index >= len(sortedNations)):
                    break
                if (room.isFull()):
                    break
                priority+=1
        
        #不管偏好、國籍，直接放進房間
        if not room.isFull():
            nation_index=0
            while (nation_index < len(sortedNations) and not room.isFull()):
                nation = sortedNations[nation_index][0]
                nationgroup = student_by_nation_df[nation]
                for student in nationgroup:
                    if(pd.notnull(student)):
                        #doens't have to match room type
                        if (not student.isArranged()):
                            room.addDweller(student)
                            student.setArranged(True)
                            picked_nation.add(nation)
                            print("success arrange one student!")
                            if (room.isFull()):
                                break
                nation_index+=1

        for dweller in room.getDweller():
            res+=(str(dweller))
            res+="\n"
        res+="\n"
    with open("int_match_result.txt", 'w') as f1:
        f1.write(res)
        f1.write("\n")

if __name__ == '__main__':
    s = time.time()
    desc = 'matching international students'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-n', help='number of rooms', default='100')
    args = parser.parse_args()
    ROOMNUM = int(args.n)
    STUDENTNUM = ROOMNUM * 4

    #gen data frame
    all_students_data = random_gen_studentData(STUDENTNUM)
    print(all_students_data.head())
    #initiate objects
    room_quota = get_room_type_quota(all_students_data, ROOMNUM)
    print((room_quota))
    #create objects
    all_rooms_objs = df2object_rooms(ROOMNUM, room_quota)
        
    all_students_objs = df2object_student(all_students_data, 1)


    sortedNations = get_country_by_pop(all_students_data)
    print(sortedNations)

    #TODo: read students objects 
    student_by_nation_df = student_by_nation_df(all_students_data, 1, sortedNations)
    print(student_by_nation_df.head())

    int_match(sortedNations, all_rooms_objs, student_by_nation_df)
    e = time.time()
    print(e-s)
