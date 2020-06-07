from match_helper import categorize, type_room_dict
import logging

def groupRoommateWithTypes(group, type2RoomDict):
    for types in group.keys():
        # See if there are still 4 people left in a type.
        while(len(group[types]) >= 4):
            # Check if there is still a room with that type
            if (len(type2RoomDict[types]) > 0):
                room = type2RoomDict[types][-1]
                room.setType(types)
                students = group[types][:4]
                for s in students:
                    room.addDweller(s)
                    # logging.debug("success arrange one student!")
                #remove room
                type2RoomDict[types].pop()
                type2RoomDict['finish'].append(room)
                
                group[types] = group[types][4:]
            else:
                break
    return group

def extract_studs(group):
    lis = []
    for key in group.keys():
        lis.extend(group[key])
    return lis

def loc_match(rooms, students):
    type2RoomDict = type_room_dict(rooms)
    roomPointer = 0
    for priority in range(3):
        group = categorize(students, priority)
        group = groupRoommateWithTypes(group, type2RoomDict)
        students = []
        for _type in group:
            students.extend(group[_type])
    
    rest = extract_studs(group)
    for _type in type2RoomDict.keys():
        if (_type != 'finish' and len(type2RoomDict[_type])>0):
            type2RoomDict[_type]#####HERE
            rest
    res=""
    for room in type2RoomDict['finish']:
        # print("matching Room:{}, Type:{}".format(room.getNum(), room.getType()))
        for dweller in room.getDweller():
            res+=(str(dweller))
            res+="\n"
        res+="\n"
    print(len(type2RoomDict['finish']))
    with open("loc_match_result.txt", 'w') as f1:
        f1.write(res)













def intoRoom(numOfSpaces, rooms, leftOver):
    for i in range(numOfSpaces):
        S = leftOver.pop()
        rooms[Room_pointer].addDweller(S)
        # How to record the bed number for each student
    return rooms




def LocalRoommatePair(students, rooms, preferenceArray):
    global Room_pointer
    #first preference
    group1 = categorize(students, 0, preferenceArray)
    # group1 =  {
    #     "I":[student1, student2],
    #     "C":[student3, student4],
    #     ...
    #  }
    leftOver = []
    leftOver, rooms = groupRoommateWithTypes(group1, rooms)
    
    #second preference
    group2 = categorize(leftOver, 1, preferenceArray)
    leftOver = []
    leftOver, rooms = groupRoommateWithTypes(group2, rooms)
              
    #third preference
    group3 = categorize(leftOver, 2, preferenceArray)
    leftOver = []
    leftOver, rooms = groupRoommateWithTypes(group3, rooms)

    #Deal with those who can't meet their preferences
    #what if len(leftOver) < rooms[]?
    while (len(leftOver) > 0):
        #4 beds are left
        if rooms.getMemberNum(rooms[Room_pointer]) == 4:
            rooms = intoRoom(4, rooms, leftOver)
        #3 beds left
        elif rooms.getMemberNum(rooms[Room_pointer]) == 3:
            rooms = intoRoom(3, rooms, leftOver)
        #2 beds letf
        elif rooms.getMemberNum(rooms[Room_pointer]) == 2:
            rooms = intoRoom(2, rooms, leftOver)
        else:
                S = leftOver.pop()
                rooms[Room_pointer].addDweller(S)
                # How to record the bed number for each student
        Room_pointer += 1
        return rooms
              

              
from static.config import PREFERENCE_DICT

from munkres import Munkres, print_matrix
import random
import pandas as pd
seed = 30
random.seed(seed)

ROOMNUM = 1516//4
all_room_types_symbol = list(PREFERENCE_DICT.values())
all_rooms = [ [str(random.choices(all_room_types_symbol))+"_"+str(i)+"_"+str(bed) for i in range(ROOMNUM)] for bed in range(4) ]

#first choice, second choice, third choice, not my choice
cost_table = [1, 5, 10, 100]

def compute_cost_matrix(students, all_rooms):
    
    init_cost = [cost_table[3] for i in range(ROOMNUM*4)]
    type_lis = [random.choices(all_room_types_symbol)[0] for i in range(ROOMNUM*4)]
    cost_matrix = pd.DataFrame()
    cost_matrix['type'] = type_lis
    for stud in students:
        not_in_priority = [_type for _type in all_room_types_symbol if _type not in stud.preferences]
        #replace with matching diff priorities cost
        cost_matrix[str(stud._id)] = cost_matrix['type'].replace( {stud.getPref(0):cost_table[0], \
                stud.getPref(1):cost_table[1], stud.getPref(2):cost_table[2]})
        #replace with no matching cost
        cost_matrix[str(stud._id)].replace(not_in_priority, cost_table[3], inplace=True)
    cost_matrix.drop(columns="type",inplace=True)

    return cost_matrix.transpose().to_numpy()


def loc_match_test(students):
    m = Munkres()
    cost_matrix = compute_cost_matrix(students, all_rooms)
    print(cost_matrix)
    indexes = m.compute(cost_matrix)
    print_matrix(cost_matrix, msg='Lowest cost through this matrix:')
    total = 0
    for row, column in indexes:
        value = cost_matrix[row][column]
        total += value
        print ("(%d, %d) -> %d"%(row, column, value))
    print ("total cost: %d"% (total))
           
              
              
              
              
              
              
              
              
              
              
              
              
              
              
              
              
              
              
              
              
              
              
              
              
        