def separateGender(All_students):
    female = []
    male = []
    for i in len(All_students):
        stu = All_students[i]
        if stu.Gender == 0:
            female.append(stu)
        else:
            male.append(stu)
    return female, male

def separateInternational(Gendered_students):
    international = []
    local = []
    for i in len(Gendered_students):
        stu = Gendered_students
        if stu.nationality != "local":
            international.append(stu)
        else:
            local.append(stu)
    return international, local


def takeoutStudent(priority, preference, local_students):
    left_local_students = []
    targeted_students = []
    for student in local_students:
        if (student.preferences[0] == preference):
            targeted_students.append(student)
        else:
            left_local_students.append(student)
    return targeted_students, left_local_students

def separare_local_IL(local_student_quota, local_students):
#功能：決定國際房數量
    local_I = []
    #選住國際區的本地生
    local_students_1I, local_students = takeoutStudent(0,"I", local_students)
    if local_student_quota - len(local_students_1I) > 0:
        local_I.extend(local_students_1I)
        #更新 quota
        local_student_quota -= len(local_students_1I) 
        #找出第二志願是國際的人
        local_students_2I, local_students= takeoutStudent(1,"I", local_students) 
        if local_student_quota - len(local_students_2I) > 0:
            local_I.extend(local_students_2I)
            local_student_quota -= len(local_students_2I)
            #找出第三志願是國際的人
            local_students_3I, local_students = takeoutStudent(2,"I", local_students) 
            if local_student_quota - len(local_students_3I) > 0:
                local_I.extend(local_students_3I)
                local_student_quota -= len(local_students_3I)
                while(local_student_quota > 0):
                    local_I.append(local_students.pop())
                    local_student_quota -=1
            else:
                while(local_student_quota > 0):
                    local_I.append(local_students.pop())
                    local_student_quota -=1
        else:
            while(local_student_quota > 0):
                local_I.append(local_students.pop())
                local_student_quota -=1
    else:
        while(local_student_quota > 0):
            local_I.append(local_students.pop())
            local_student_quota -=1
    return local_I, local_students


def allNationalities(studentArray):
    Nationalities = []
    for student in studentArray:
        Nationalities.append(student.nationality)
    return len(set(Nationalities))

def arrangeInternationalStudents(inter_I, Rooms, num_rooms_I):
    #功能：國際區國際生室友配對
    #至少還有2個不同國籍
    nationalities = [student.nationality for student in inter_I]
    countDict = {nation:nationalities.count(nation) for nation in nationalities}

    #room: 0 ~ num_rooms_I-1 are international rooms
    for nation in countDict.keys():
        ppl_per_room  = countDict[nation]//num_rooms_I
        if(ppl_per_room == 0):
            taken_rooms = countDict[nation]%num_rooms_I
            for room_index in range(taken_rooms):
                #take one dweller with that nationality
                Rooms[room_index].addDweller(None)
        #one room with more than one dwellers that has the same nationality
        else:
            #先填補完一輪
            for room_index in range(num_rooms_I):
                #take one dweller with that nationality
                student_A, student_B = takeInternationalMatch(inter_I, nationality, ppl_per_room)
                Rooms[room_index].addDweller(student_A)
                Rooms[room_index].addDweller(student_B)
            #把剩下的人放進
            taken_rooms = countDict[nation]%num_rooms_I
            for room_index in range(taken_rooms):
                #take one dweller with that nationality
                Rooms[room_index] = None 
                ppl_per_room-=1

# Students: local_I, local_L
# Priority: 0, 1, 2
# preferenceArray = [I, H, E, C, S, G]
def categorize(students, priority, preferenceArray):
    #功能：依志願分群
    group = {}
    for pref in preferenceArray:
        group[pref] = []
    for student in students:
        if (student.preference[priority] == "I"):
            group["I"].append(student)
        elif (student.preference[priority] == "H"):
            group["H"].append(student)
        elif (student.preference[priority] == "E"):
            group["E"].append(student)
        elif (student.preference[priority] == "C"):
            group["C"].append(student)
        elif (student.preference[priority] == "S"):
            group["S"].append(student)
        elif (student.preference[priority] == "G"):
            group["G"].append(student)
    return group



# Rooms: Rooms
# Students: local_I, local_L
def RoommatePair(students, Rooms, Room_pointer, preferenceArray):
    #功能：國際區本地生/非國際區 室友配對
    # 看第一志願
    group1 = categorize(students, 0, preferenceArray)
    #尚未被排入的學生
    leftOver = [] 
    for type in group1.keys():
        while(len(group1[type]) >1):
            first_S = group1[type].pop()
            second_S = group1[type].pop()
            Rooms[Room_pointer].addDweller(first_S)
            Rooms[Room_pointer].addDweller(second_S)
            Room_pointer +=1
        if (len(group1[type])==1):
            leftOver.append(group1[type].pop())
    #看第二志願
    group2 = categorize(leftOver, 1, preferenceArray)
    #尚未被排入的學生
    leftOver = []
    for type in group2.keys():
        while(len(group2[type]) >1):
            first_S = group2[type].pop()
            second_S = group2[type].pop()
            Rooms[Room_pointer].addDweller(first_S)
            Rooms[Room_pointer].addDweller(second_S)
            Room_pointer +=1
        if (len(group2[type])==1):
            leftOver.append(group2[type].pop())
    #第三志願
    group3 = categorize(leftOver, 2, preferenceArray)
    #尚未被排入的學生
    leftOver = [] 
    for type in group3.keys():
        while(len(group3[type]) >1):
            first_S = group3[type].pop()
            second_S = group3[type].pop()
            Rooms[Room_pointer].addDweller(first_S)
            Rooms[Room_pointer].addDweller(second_S)
            Room_pointer +=1
        if (len(group3[type])==1):
            leftOver.append(group3[type].pop())
    while(len(leftOver) > 0):
        if(len(leftOver) == 1):
            Rooms[Room_pointer].add(leftOver.pop())
        else:
            Rooms[Room_pointer].add(leftOver.pop())
            Rooms[Room_pointer].add(leftOver.pop())
            Room_pointer += 1
    return Rooms  

