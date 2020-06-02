from utility.helper import separateInternational, separare_local_IL, arrangeInternationalStudents, RoommatePair
from utility.loc_match import LocalRoommatePair
from utility.static.config import PREFERENCE_DICT

from app import app
from flask import request

@app.route("/api/match", methods=["GET", "POST"])
def match():
    if request.method == "POST":
        return macros_handler.create_macro(request.get_json())
    else:
        language = request.args.get("language")
        local = request.args.get("local")
        gender = request.args.get("gender")
        macro_name = request.args.get("name")
        if macro_name is not None:
          return macros_handler.get_all_macros_by_name(name=macro_name)
        else:
          return macros_handler.get_macros(language, local, gender)


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
#read student data
#   initialize student objects. local students' nationalities are 'local'
#   s = Student(id, preferences, nationality, gender)
#   All_students.append(s)
#read room data
#   initialize room data
#   r = Room(gender, room_num)
#   Rooms.append(r)

#input
#DataFrame1 (男生)
# ID, gender, 校內外意願, 區域志願1, 區域志願2, 區域志願3, 永久地址（國籍）, id_index(身障身==1)
#DataFrame2 (女生)
# ID, gender, 校內外意願, 區域志願1, 區域志願2, 區域志願3, 永久地址（國籍）, id_index(身障身==1)
#output
# ID, 宿舍, 床位



'''Student'''
#studData = preprocess_df(df)
studObjs = df2object_student(studData, gender)
intStuds, locStuds = separateInternational(studObjs)
locIntRoomStudQuota, intRoomNum = getIntRoomNum(intStuds)
locLocRoomStuds, locIntRoomStuds = selectLocIntRoomStuds(locIntRoomStudQuota, locStuds)

allIntRoomStuds = concate(intStuds, locLocRoomStuds)
allLocRoomStuds = locIntRoomStuds
''' intRoom'''
#select loc_studs 
roomTypeQuota = get_room_type_quota(intRoomNum, allIntRoomStuds)
intRoomsObjs = df2object_rooms(intRoomNum, roomTypeQuota)
sortedNations = get_country_by_pop(allIntRoomStuds)

studentByNationDF = student_by_nation_df(allIntRoomStuds, gender, sortedNations)

int_match(sortedNations, intRoomsObjs, studentByNationDF)

'''locRoom'''

'''match'''

def Matching(international_S, local_students):
    #決定國際房數量
    

    #選住在國際區的本地學生. Array
    local_I, local_L = separare_local_IL(local_student_quota, local_students)
    #安排住在國際區的國際學生的房間
    Rooms, Room_pointer = arrangeInternationalStudents(inter_I, Rooms, num_rooms_I)
    #安排住在國際區的本地學生的房間
    Rooms = RoommatePair(local_I, Rooms, Room_pointer, preferenceArray)
    #安排住在非國際區的本地學生的房間
    Rooms = LocalRoommatePair(local_L, Rooms, preferenceArray)


# num_internationl_students: len(Males_internationl), len(females_internationl)
# local_students: males_local/females_local


