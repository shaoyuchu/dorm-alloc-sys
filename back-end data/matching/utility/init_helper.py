from handler.student_hanlder import Student
from handler.room_hanlder import Room

def df2object_student(df, gender):
    students_lis = []
    for i in range(len(df)):
        attris = dict(df.iloc[i])
        s = Student(id=attris['ID'],nationality = attris['nationality'], preferences = [attris['pref_1'], attris['pref_2'], attris['pref_3']], gender=gender)
        students_lis.append(s)
    return students_lis

def get_freq(students_data, col):
    all_data = students_data[col].values
    unique_kind = np.unique(all_data)
    count = {}
    for kind in unique_kind:
        count[kind] =  np.count_nonzero(all_data == kind, axis=None)
    return count

def get_room_type_quota(roomNum, students_data):
    # all_prefs = np.concatenate( (students_data['pref_1'].values, np.concatenate( (students_data['pref_2'].values, students_data['pref_3'].values), axis=None)),axis=None)
    # only consider the first priority when deciding # of rooms for each type
    count = get_freq(students_data, col  = 'pref_1')
    ratio ={key: round(count[key]/sum(count.values()),2) for key in count}
    result = {key: int(ratio[key] * roomNum) for key in ratio}
    #if there are one more or less room, modify the # of rooms of the first type
    if (sum(result.values())> roomNum):
        result[list(result.keys())[0]] -= 1
    elif (sum(result.values()) < roomNum):
        result[list(result.keys())[0]] += 1
    return result

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

def getIntRoomNum(int_stud):
    intRoomNum = len(int_stud)//MAX_INT_STUD_PER_ROOM
    if (intRoomNum%MAX_INT_STUD_PER_ROOM != 0):
        intRoomNum+=1
    locStudQuota = intRoomNum * Room.MAXROOMCAPACITY - len(int_stud)
    return locStudQuota, intRoomNum