class Student:
    def __init__(self, _id, preferences, nationality, gender):
        super().__init__()
        self._id = _id
        #1x3 array of preferences (e.g. [“I”, “H”, “E”])
        self.preferences = preferences
        #string
        self.nationality = nationality
        #int (0:girl; 1:boy)
        self.gender = gender
        #room number
        self.room = -1
        #bed ABCD
        self.bed = ''
        self.arranged = False
        
    def getPref(self, priority):
        return self.preferences[priority]

    def setArranged(self, signal):
        self.arranged = signal

    def isArranged(self):
        return self.arranged

    def __str__(self):
        gender = "Male"
        if (self.gender==0):
            gender = "Famale"
        return "id: {}, nationality: {}, gender: {}, preferences: {}".format(self._id, self.nationality, self.gender, self.preferences)