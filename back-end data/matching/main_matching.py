from matching_helper import separateGender, separateInternational, separare_local_IL, arrangeInternationalStudents, RoommatePair
# import Room
# import Student

PREFERENCE_DICT = {
    "國際區":"I",
    "健康作息區":"H",
    "節能減碳區":"E",
    "乾淨整潔區":"C",
    "運動休閒區":"S",
    "一般區":"G",
}

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
#shuffle student data [UPDATE]
#read student data
#   initialize student objects. local students' nationalities are 'local'
#   s = Student(id, preferences, nationality, gender)
#   All_students.append(s)
#read room data
#   initialize room data
#   r = Room(gender, room_num)
#   Rooms.append(r)

#分性別
females, males = separateGender(All_students)
#分本地跟國際生
males_internationl, males_local = separateInternational(males)
females_internationl, females_local = separateInternational(males)


Matching(males_internationl, males_local)
Matching(females_internationl, females_local)
# input males_local first

def Matching(international_S, local_students):
    #決定國際房數量
    num_rooms_I = international_S//3
    if (international_S%3 != 0):
        num_rooms_I+=1
    local_student_quota = num_rooms_I * Room.MAXROOMCAPACITY - len(international_S)

    #選住在國際區的本地學生. Array
    local_I, local_L = separare_local_IL(local_student_quota, local_students)
    #安排住在國際區的國際學生的房間
    Rooms, Room_pointer = arrangeInternationalStudents(inter_I, Rooms, num_rooms_I)
    #安排住在國際區的本地學生的房間
    Rooms = RoommatePair(local_I, Rooms, Room_pointer, preferenceArray)
    #安排住在非國際區的本地學生的房間
    Rooms = RoommatePair(local_L, Rooms)


# num_internationl_students: len(Males_internationl), len(females_internationl)
# local_students: males_local/females_local


