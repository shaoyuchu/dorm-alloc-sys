import sys
sys.path.insert(0, '../utility/')
sys.path.insert(0, '../handler/')
from match_helper import separateInternational, getIntRoomNum, selectLocIntRoomStuds, get_room_type_quota, split_rooms_gender, assign_room_type
from init_helper import df2object_student, df2object_rooms, preprocess_df,object2df_student
from loc_match import loc_match
from int_match import get_country_by_pop, student_by_nation_df, int_match
from static.config import PREFERENCE_DICT, logging

import pandas as pd



#array all students
All_students = []
#array 住國際區的國際生
inter_I = []
#array 住國際區的本地生
local_I = []
#array of room objects
Rooms = []
Room_pointer = 0
preferenceArray = ["I", "H", "E"," C", "S","G"]

'''Main'''
#input
#DataFrame1 (男生)
# ID, gender, 校內外意願, 區域志願1, 區域志願2, 區域志願3, 永久地址（國籍）, id_index(身障身==1)
#DataFrame2 (女生)
# ID, gender, 校內外意願, 區域志願1, 區域志願2, 區域志願3, 永久地址（國籍）, id_index(身障身==1)
#output
# ID, 宿舍, 房號, 床位


stud_df_male = pd.read_excel("../../BoyQua.xlsx")
stud_df_female = pd.read_excel("../../GirlQua.xlsx")
room_df = pd.read_excel("../../DormRoom.xlsx")

def main_match(stud_df_male, stud_df_female, room_df):
        '''Split by gender'''
        studDataMale = preprocess_df(stud_df_male)
        studDataFemale = preprocess_df(stud_df_female)
        logging.info("Students: {}/{} (male/female)".format(len(studDataMale), len(studDataFemale)))
        '''Rooms'''
        roomsObjs = df2object_rooms(room_df)
        roomsObjs = sorted(roomsObjs, reverse=True)
        maleRooms, femaleRooms = split_rooms_gender(roomsObjs)
        # res = ""
        # for room in roomsObjs:
        #         res+=str(room)
        #         res+="\n"
        # with open("out.txt",'w') as f1:
        #         f1.write(res)
        
        '''Student'''
        match(studDataMale, maleRooms, gender=1)
        match(studDataFemale,femaleRooms, gender=0)

def match(studData, roomObjs, gender):
        studObjs = df2object_student(studData, gender)
        intStuds, locStuds = separateInternational(studObjs)
        locIntRoomStudQuota, INTROOMNUM = getIntRoomNum(intStuds)
        locLocRoomStuds, locIntRoomStuds = selectLocIntRoomStuds(locIntRoomStudQuota, locStuds)

        allIntRoomStuds = intStuds+locIntRoomStuds
        TOTOALROOMNUM = len(roomObjs)
        LOCROOMNUM = TOTOALROOMNUM - INTROOMNUM

        logging.info("local rooms: {}; internaitonal rooms:{}".format(LOCROOMNUM, INTROOMNUM))
        logging.info("international rooms: {} ;{} international and {} local" \
                .format(len(allIntRoomStuds), len(intStuds), len(locIntRoomStuds)))
        logging.info("{} students in local rooms".format(len(locLocRoomStuds)))

        ''' IntRoom matching'''
        #trasform stud objs back to df
        int_room_stud_df = object2df_student(studData, allIntRoomStuds)
        #get type quota of the int rooms 
        roomTypeQuota = get_room_type_quota(int_room_stud_df, INTROOMNUM)
        #create room objects
        intRoomsObjs = assign_room_type(roomObjs, roomTypeQuota)
        #get country list ordered by its popularity
        sortedNations = get_country_by_pop(int_room_stud_df)
        logging.info((sortedNations))
        #student by nationality df
        studentByNationDF = student_by_nation_df(int_room_stud_df, gender, sortedNations)

        arranged_int_studs_lis, all_int_rooms_objs = int_match(sortedNations, intRoomsObjs, studentByNationDF)

        logging.info("Int Rooms: {}/{} (arranged/all)" \
                .format(INTROOMNUM, len(all_int_rooms_objs)))
        logging.info("Int Students: {}/{} (arranged/all)" \
                .format(len(arranged_int_studs_lis), len(int_room_stud_df)))

        # '''locRoom'''
        loc_room_stud_df = object2df_student(studData, locLocRoomStuds)
        roomTypeQuota = get_room_type_quota(loc_room_stud_df, LOCROOMNUM)
        locRoomsObjs = assign_room_type(LOCROOMNUM, roomTypeQuota)
        arranged_loc_studs_lis, all_loc_rooms_objs = loc_match(locRoomsObjs, locLocRoomStuds)

        logging.info("Loc Rooms: {}/{} (arranged/all)" \
                .format(len(all_loc_rooms_objs), LOCROOMNUM))
        logging.info("Loc Students: {}/{} (arranged/all)" \
                .format(len(arranged_loc_studs_lis), len(loc_room_stud_df)))


main_match(stud_df_male, stud_df_female, room_df)