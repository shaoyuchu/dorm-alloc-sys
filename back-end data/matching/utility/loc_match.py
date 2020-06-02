from matching_helper import categorize

def intoRoom(numOfSpaces, rooms, leftOver):
    for i in range(numOfSpaces):
        S = leftOver.pop()
        rooms[Room_pointer].addDweller(S)
        # How to record the bed number for each student
    return rooms

def groupRoommateWithTypes(group, rooms):
    leftOverTemp = []
    for types in group.keys():
        # See if there are still 4 people left in a type.
        while(len(group[types]) > 3):
            # Check if the room is totally empty.
            if rooms.getMemberNum(rooms[Room_pointer]) == 4:
                intoRoom(4, rooms, leftOverTemp)
            Room_pointer += 1
        if (len(group[types]) <= 3):
            leftOverTemp.append(group[types].pop())
    return leftOverTemp, rooms

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
              

              
              
              
              
              
              
              
              
              
              
              
              
              
              
              
              
              
              
              
              
              
              
              
              
              
              
        