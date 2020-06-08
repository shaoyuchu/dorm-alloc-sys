import sys
from match_helper import separateInternational, getIntRoomNum, selectLocIntRoomStuds, get_room_type_quota, assign_room_type, split_loc_int_rooms
from init_helper import df2object_student, df2object_rooms, preprocess_df,object2df_student
from loc_match import loc_match
from int_match import get_country_by_pop, student_by_nation_df, int_match
from static.config import PREFERENCE_DICT, logging

import pandas as pd

'''Main'''
#input
#DataFrame1 (男生)
# ID, gender, 校內外意願, 區域志願1, 區域志願2, 區域志願3, 永久地址（國籍）, id_index(身障身==1)
#DataFrame2 (女生)
# ID, gender, 校內外意願, 區域志願1, 區域志願2, 區域志願3, 永久地址（國籍）, id_index(身障身==1)
#output
# ID, 宿舍, 房號, 床位

def main_match(stud_df_male, stud_df_female, room_df):
        '''Split by gender'''
        studDataMale = preprocess_df(stud_df_male)
        studDataFemale = preprocess_df(stud_df_female)
        logging.info("Students: {}/{} (male/female)".format(len(studDataMale), len(studDataFemale)))
        
        '''Rooms'''
        maleRooms, femaleRooms = df2object_rooms(room_df)
        maleRooms = sorted(maleRooms, reverse=True)
        femaleRooms = sorted(femaleRooms, reverse=True)
        logging.info("Rooms: {}/{} (male/female)".format(len(maleRooms), len(femaleRooms)))

        '''Student'''
        match(studDataMale, maleRooms, gender=1)
        match(studDataFemale,femaleRooms, gender=0)

def match(studData, roomObjs, gender):
        #init stud and room objs
        studObjs = df2object_student(studData, gender)
        intStuds, locStuds = separateInternational(studObjs)
        #calculate num of int rooms  and num of loc studs in int rooms
        locIntRoomStudQuota, INTROOMNUM = getIntRoomNum(intStuds)
        #select loc studs in int rooms
        locLocRoomStuds, locIntRoomStuds = selectLocIntRoomStuds(locIntRoomStudQuota, locStuds)
        #split int and loc rooms
        intRoomsObjs, locRoomsObjs = split_loc_int_rooms(roomObjs,INTROOMNUM)

        allIntRoomStuds = intStuds+locIntRoomStuds
        TOTOALROOMNUM = len(roomObjs)
        LOCROOMNUM = TOTOALROOMNUM - INTROOMNUM

        g = "Male"
        if(gender==0):
                g = "Female"
        logging.info("——————Matching {}——————".format(g))
        logging.info("  Rooms")
        logging.info("          Int {}".format(INTROOMNUM))
        logging.info("          Loc {}".format(LOCROOMNUM))
        logging.info("  Students")
        logging.info("          Int {}".format(len(allIntRoomStuds)))
        logging.info("                  int studs {}".format(len(intStuds)))
        logging.info("                  loc studs {}".format(len(locIntRoomStuds)))
        logging.info("          Loc {}".format(len(locLocRoomStuds)))

        ''' IntRoom matching'''
        #trasform stud objs back to df
        int_room_stud_df = object2df_student(studData, allIntRoomStuds)
        #get type quota of the int rooms 
        roomTypeQuota = get_room_type_quota(int_room_stud_df, INTROOMNUM)
        # logging.info("Type: {}".format(roomTypeQuota))
        #assign types to int rooms
        intRoomsObjs = assign_room_type(intRoomsObjs, roomTypeQuota)
        #get country list ordered by its popularity
        sortedNations = get_country_by_pop(int_room_stud_df)
        # logging.info(sortedNations)
        #student by nationality df
        studentByNationDF = student_by_nation_df(int_room_stud_df, gender, sortedNations)

        arranged_int_studs_lis, all_int_rooms_objs = int_match(sortedNations, intRoomsObjs, studentByNationDF)

        # '''locRoom'''
        loc_room_stud_df = object2df_student(studData, locLocRoomStuds)
        roomTypeQuota = get_room_type_quota(loc_room_stud_df, LOCROOMNUM)
        # logging.info("Loc Rooms: {}".format(roomTypeQuota))
        locRoomsObjs = assign_room_type(locRoomsObjs, roomTypeQuota)
        arranged_loc_studs_lis, all_loc_rooms_objs = loc_match(locRoomsObjs, locLocRoomStuds)

        logging.info("——————Results——————")
        logging.info("  Rooms")
        logging.info("          Int {}/{} (arranged/all)" \
                .format(len(all_int_rooms_objs), INTROOMNUM))
        
        logging.info("          Loc: {}/{} (arranged/all)" \
                .format(len(all_loc_rooms_objs), LOCROOMNUM))
        
        logging.info("  Students")
        logging.info("          Int: {}/{} (arranged/all)" \
                .format(len(arranged_int_studs_lis), len(int_room_stud_df)))        
        logging.info("          Loc: {}/{} (arranged/all)" \
                .format(len(arranged_loc_studs_lis), len(loc_room_stud_df)))


# stud_df_male = pd.read_excel("../../BoyQua.xlsx")
# stud_df_female = pd.read_excel("../../GirlQua.xlsx")
# room_df = pd.read_excel("../../DormRoom.xlsx")
# main_match(stud_df_male, stud_df_female, room_df)