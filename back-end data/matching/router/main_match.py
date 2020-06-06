import sys
sys.path.insert(0, '../utility/')
sys.path.insert(0, '../handler/')
from match_helper import separateInternational, getIntRoomNum, selectLocIntRoomStuds
from init_helper import df2object_student, df2object_rooms, preprocess_df,object2df_student
# from loc_match import LocalRoommatePair
from int_match import get_room_type_quota, get_country_by_pop, student_by_nation_df, random_gen_studentData, int_match
from static.config import PREFERENCE_DICT


import logging
logging.basicConfig(level=logging.DEBUG)
# pacakge for debug mode
# tutorial: https://titangene.github.io/article/python-logging.html
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
# ID, 宿舍, 床位

df = pd.read_excel("../../../../match_use.xls")
TOTOALROOMNUM = len(df)//4+1
gender = 1
'''Student'''
studData = preprocess_df(df)
studObjs = df2object_student(studData, gender)
intStuds, locStuds = separateInternational(studObjs)
logging.debug("{} {}".format(len(intStuds), len(locStuds)))
locIntRoomStudQuota, INTROOMNUM = getIntRoomNum(intStuds)
logging.debug("{}".format(locIntRoomStudQuota))
locLocRoomStuds, locIntRoomStuds = selectLocIntRoomStuds(locIntRoomStudQuota, locStuds)
logging.debug("{} {}".format(len(locLocRoomStuds), len(locIntRoomStuds)))

allIntRoomStuds = intStuds+locIntRoomStuds
LOCROOMNUM = TOTOALROOMNUM - INTROOMNUM

logging.debug("{} local rooms and {} internaitonal rooms".format(LOCROOMNUM, INTROOMNUM))
logging.debug("There are {} students in international rooms of which {} are inter studs and {} are local studs" \
        .format(len(allIntRoomStuds), len(intStuds), len(locIntRoomStuds)))
logging.debug("There are {} students in local rooms".format(len(locLocRoomStuds)))

''' IntRoom matching'''
#trasform stud objs back to df
int_room_stud_df = object2df_student(studData, allIntRoomStuds)
logging.debug(len(int_room_stud_df))
#get type quota of the int rooms 
roomTypeQuota = get_room_type_quota(int_room_stud_df, INTROOMNUM)
#create room objects
intRoomsObjs = df2object_rooms(INTROOMNUM, roomTypeQuota)
#get country list ordered by its popularity
sortedNations = get_country_by_pop(int_room_stud_df)
logging.debug((sortedNations))
exit()
#student by nationality df
studentByNationDF = student_by_nation_df(int_room_stud_df, gender, sortedNations)

int_match(sortedNations, intRoomsObjs, studentByNationDF)

# '''locRoom'''
# allLocRoomStuds = locIntRoomStuds

# '''match'''

# def Matching(international_S, local_students):
#     #決定國際房數量
    

#     #選住在國際區的本地學生. Array
#     local_I, local_L = separare_local_IL(local_student_quota, local_students)
#     #安排住在國際區的國際學生的房間
#     Rooms, Room_pointer = arrangeInternationalStudents(inter_I, Rooms, num_rooms_I)
#     #安排住在國際區的本地學生的房間
#     Rooms = RoommatePair(local_I, Rooms, Room_pointer, preferenceArray)
#     #安排住在非國際區的本地學生的房間
#     Rooms = LocalRoommatePair(local_L, Rooms, preferenceArray)


# num_internationl_students: len(Males_internationl), len(females_internationl)
# local_students: males_local/females_local


