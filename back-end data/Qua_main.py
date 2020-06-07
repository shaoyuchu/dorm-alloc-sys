import sys
import pandas as pd
import numpy as np
from pandas.api.types import CategoricalDtype
from random import *
from Qua_config import *
from Qua_mainFunc import *

# main

# get: studnet list from front-end
StudentList = pd.read_excel('BallotApplyUndergraduate.xls', header = 0)

#temp
StudentList['學號'] = [ str(i) for i in range(len(StudentList))]

# pass all id_type to front-end
AllIdType = GetAllIdType(StudentList)

# get: ordered id_type from front-end
# here i use ordered_idtype_List from config


# get: id_orderList, student list, dorm room list from front-end
DormList = pd.read_excel('DormRoom.xlsx', header = 0)
BoyQua, GirlQua, WaitDF = DivideDF(id_orderList, StudentList, DormList)
# give: BoyQua & GirlQua to algorithm part


# get: BoyQua & GirlQua form algorithm part
CampusBoy, CampusGirl, BotBoy, BotGirl = GetOutputDF(id_orderList,BoyQua, GirlQua, StudentList, WaitDF)


