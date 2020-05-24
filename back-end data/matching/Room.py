class Room:
    def __init__(self, gender, room_num, _type, dorm="Man1"):
        super().__init__()
        MAXROOMCAPACITY = 4
        #int (0:girl;1:boy)
        self.gender = gender
        #string
        self.dorm = dorm
        #int
        self.room_num = room_num
        #type: string (e.g. “I”, “H”, “E”, “C”)
        self.room_type = _type
        #array of student objects
        self.dwellers = []
    
    def addDweller(self, student):
        self.dwellers.append(student)

    def getDweller(self):
        return self.dwellers
    
    #return an array of dwellers’ nationalities
    def getDwellerNationality(self):
        if (len(self.dwellers)==0):
            return None
        else:
            return [dweller.nationality for dweller in self.dwellers]

    def getDwellerPreference(self):
        if (len(self.dwellers)==0):
            return None
        else:
            return [dweller.preference for dweller in self.dwellers]
    
    def setType(self, _type):
        self.room_type = _type

    def getType(self):
        return self.room_type

    def getNum(self):
        return self.room_num

    def isFull(self):
        return len(self.dwellers)==4

    def __getitem__(self, key):
        if(len(self.dwellers)==0):
            return IndexError
        else:
            return self.dwellers[key]

    def __setitem__(self, student):
        if(len(self.dwellers) > Room.MAXROOMCAPACITY):
            raise IndexError
        else:
            self.dwellers[key] = student
    
    def __str__(self):
        return "Dorm: {}\n\tRoom Number: {}\n\tRoom Type: {}".format(self.dorm, self.room_num, self.room_type)
