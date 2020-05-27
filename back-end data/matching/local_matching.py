def LocalRoommatePair(students, rooms):
    #first preference
    group1 = categorize(students, 0)
    leftOver = []
    for types in group1.keys():
        while(len(group1[types]) > 3):
            if getMemberNum(rooms[Room_pointer]) == 4:
                for i in range(4):
                    S = group1[types].pop()
                    rooms[Room_pointer].addDweller(S)
                    # How to record the bed number for each student
            Room_pointer += 1
        if (len(group1[types]) <= 3):
            leftOver.append(group1[types].pop())
     
    #second preference
    group2 = categorize(leftOver, 1)
    leftOver = []
    for types in group2.keys():
        while(len(group2[types] > 3):
              if getMemberNum(rooms[Room_pointer]) == 4:
                for i in range(4):
                    S = group2[types].pop()
                    rooms[Room_pointer].addDweller(S)
                    # How to record the bed number for each student
            Room_pointer += 1
        if (len(group2[types]) <= 3):
            leftOver.append(group2[types].pop())
              
    #third preference
    group3 = categorize(leftOver, 2)
    leftOver = []
    for types in group3.keys():
        while(len(group3[types] > 3):
              if getMemberNum(rooms[Room_pointer]) == 4:
                for i in range(4):
                    S = group3[types].pop()
                    rooms[Room_pointer].addDweller(S)
                    # How to record the bed number for each student
            Room_pointer += 1
        if (len(group3[types]) <= 3):
            leftOver.append(group3[types].pop())

    #Deal with those who can't meet their preferences
    #what if len(leftOver) < rooms[]?
    while (len(leftOver) > 0):
        if getMemberNum(rooms[Room_pointer]) == 4:
            for i in range(4):
                S = leftOver.pop()
                rooms[Room_pointer].addDweller(S)
        else if getMemberNum(rooms[Room_pointer]) == 3:
            for i in range(3):
                S = leftOver.pop()
                rooms[Room_pointer].addDweller(S)
                # How to record the bed number for each student
        else if getMemberNum(rooms[Room_pointer]) == 2:
            for i in range(2):
                S = leftOver.pop()
                rooms[Room_pointer].addDweller(S)
                # How to record the bed number for each student
        else:
                S = leftOver.pop()
                rooms[Room_pointer].addDweller(S)
                # How to record the bed number for each student
        Room_pointer += 1
              

              
              
              
              
              
              
              
              
              
              
              
              
              
              
              
              
              
              
              
              
              
              
              
              
              
              
        