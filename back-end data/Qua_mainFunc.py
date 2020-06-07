from Qua_config import *
from Qua_assisFunc import *
import pandas as pd


# function 1

def GetAllIdType(StudentList):
    StudentList = pd.DataFrame(StudentList[1:], columns=StudentList[0])
    id_col_name  = ['身分別1','身分別2','身分別3','特殊身份別']
    column       = [str(x) for i in range(len(id_col_name)) for x in StudentList[id_col_name[i]].tolist() if str(x)!='None']
    return list(set(column))


# function 2

def DivideDF(ordered_IdList, StudentList, DormList):
    StudentList = pd.DataFrame(StudentList[1:], columns=StudentList[0])
    StudentList['學號'] = [str(i) for i in range(len(StudentList))] # TODO: remove!
    DormList = pd.DataFrame(DormList[1:], columns=DormList[0])

    StudentList = StudentList.drop(columns = Ori_ColumnToBeDrop)
    BedNumDict = countBedNum(DormList)
    
    # get get_str2int
    id_dict = get_id_dict(ordered_IdList)
    # audit_dict = get_audit_dict(id_dict)
    StudentList = get_str2int(id_dict, StudentList)
    
    # divide in-out campus
    StudentList = StudentList.sort_values(by = '校內外意願').reset_index(drop = True)
    InCamNum = len(StudentList)-StudentList.groupby('校內外意願').count()['性別'][3]
    
    InCam_df = StudentList.iloc[:InCamNum,:]
    InCam_df = InCam_df.sort_values(by = '性別').reset_index(drop = True)
    InCam_df['資格'] = [2 if (row['id_index']==1 and row['是否需要安排身障房間']=='是') else 0 for index,row in InCam_df.iterrows()]
    
    # incampus divide boy-girl
    GirlInCamNum = InCam_df.groupby(['性別']).size()['女性']
    GirlInCam = InCam_df.iloc[:GirlInCamNum,:].sort_values(by='id_index').reset_index(drop=True)
    BoyInCam = InCam_df.iloc[GirlInCamNum:,:].sort_values(by='id_index').reset_index(drop=True)

    
    # WaitDF
    WaitDF = StudentList.iloc[InCamNum:,:]
    
    
    # get qualification of boy&girl df
    GirlInCam = dealWithPreference(assign_qualificaiton(GirlInCam,BedNumDict))
    BoyInCam = dealWithPreference(assign_qualificaiton(BoyInCam,BedNumDict))
    GirlInCam = GirlInCam.sort_values(by='資格').reset_index(drop=True)
    BoyInCam = BoyInCam.sort_values(by='資格').reset_index(drop=True)
    
        
    # All-Wait DF
    QuaGirlGroup = GirlInCam.groupby('資格').count()
    NoQuaGirlNum = QuaGirlGroup['性別'][0]
    QuaBoyGroup = BoyInCam.groupby('資格').count()
    NoQuaBoyNum = QuaBoyGroup['性別'][0]
    WaitAllDf = [GirlInCam.iloc[:NoQuaGirlNum,:],BoyInCam.iloc[:NoQuaBoyNum],WaitDF]
    WaitDF = pd.concat(WaitAllDf)
    
    
    # Output Girl&Boy df
    GirlInCam = GirlInCam.iloc[NoQuaGirlNum:,:].drop(columns = AlgorithmNeedDrop).sort_values(by='id_index').reset_index(drop=True)
    BoyInCam = BoyInCam.iloc[NoQuaBoyNum:,:].drop(columns = AlgorithmNeedDrop).sort_values(by='id_index').reset_index(drop=True)
    

    
    # organize Wait df
    WaitDF = WaitDF.drop(columns=Wait_Drop)
    return BoyInCam, GirlInCam, WaitDF
    

    
# function3
def GetOutputDF(id_orderList, BoyQua, GirlQua, StudentList, WaitDF):
    # BoyQua = pd.DataFrame(BoyQua[1:], columns=BoyQua[0])
    # GirlQua = pd.DataFrame(GirlQua[1:], columns=GirlQua[0])
    StudentList = pd.DataFrame(StudentList[1:], columns=StudentList[0])
    StudentList['學號'] = [str(i) for i in range(len(StudentList))] # TODO: remove!
    # WaitDF = pd.DataFrame(WaitDF[1:], columns=WaitDF[0])

    # Divide WaitDF => campus,BOT
    WaitDF = WaitDF.sort_values('校內外意願')
    WillGroupNum = WaitDF.groupby('校內外意願')
    CampusNum = WillGroupNum.count()['性別'][1] + WillGroupNum.count()['性別'][2]
    NotBotNum = len(WaitDF) - WillGroupNum.count()['性別'][2] - WillGroupNum.count()['性別'][3]
    
    Campus = WaitDF.iloc[:CampusNum,:].drop(columns = CampusWait_Drop_AsQua).sort_values('性別')
    Bot = WaitDF.iloc[NotBotNum:,:]
    
    # organize Campus
    Campus['資格'] = [0 for i in range(len(Campus))]
    CampusGirlNum = Campus.groupby('性別')['性別'].count().tolist()[0]
    CampusBoy = OrderAssign(Campus.iloc[CampusGirlNum:])
    CampusGirl = OrderAssign(Campus.iloc[:CampusGirlNum])
    
    BoyQua['順位序號'] = [0 for i in range(len(BoyQua))]
    GirlQua['順位序號'] = [0 for i in range(len(GirlQua))]
    
    CampusBoy = pd.concat([BoyQua,CampusBoy])
    CampusGirl = pd.concat([GirlQua,CampusGirl])
    
    # drop and merge
    CampusBoy = CampusBoy.drop(columns=Qua_Drop)
    CampusGirl = CampusGirl.drop(columns=Qua_Drop)
    StudentListMergeWithCampus = StudentList.drop(columns = Ori_DfDropForICampus)
    CampusBoy = pd.merge(CampusBoy,StudentListMergeWithCampus,on=['學號'])
    CampusGirl = pd.merge(CampusGirl,StudentListMergeWithCampus,on=['學號'])
    
    # BOT drop & merge & Divide => BotBoy, BotGirl
    StudentListMergeWithBot = StudentList.drop(columns = StudentList_Drop_ForMapBot)
    Bot = Bot.drop(columns=Bot_Drop_ForOutput)
    Bot = pd.merge(Bot,StudentListMergeWithBot,on=['學號'])
    
    Bot = Bot.sort_values('性別')
    BotGirlNum = Bot.groupby('性別')['性別'].count().tolist()[0]
    BotBoy = OrderAssign(Bot.iloc[BotGirlNum:])
    BotGirl = OrderAssign(Bot.iloc[:BotGirlNum])
    
    # id_index => str
    id_IndexStr = dict()
    for i in range(1,len(id_orderList)+1):
        id_IndexStr[i] = '00000000000000'
        for j in id_orderList[i-1]:
            if len(j)<len(id_IndexStr[i]):
                    id_IndexStr[i] = j
    id_IndexStr[len(id_IndexStr)+1] = '北北基及桃園以外的縣市'
    id_IndexStr[len(id_IndexStr)+1] = '桃園'
    id_IndexStr[len(id_IndexStr)+1] = '北北基'
    print(id_IndexStr)
    
    CampusBoy['id_index'] = [id_IndexStr[i] for i in CampusBoy['id_index']]
    CampusGirl['id_index'] = [id_IndexStr[i] for i in CampusGirl['id_index']]
    BotBoy['id_index'] = [id_IndexStr[i] for i in BotBoy['id_index']]
    BotGirl['id_index'] = [id_IndexStr[i] for i in BotGirl['id_index']]
    CampusBoy = CampusBoy.fillna('None')
    CampusGirl = CampusGirl.fillna('None')
    BotBoy = BotBoy.fillna('None')
    BotGirl = BotGirl.fillna('None')

    Campus_col = CampusBoy.columns.tolist()
    Bot_col = BotBoy.columns.tolist()

    CampusBoy = CampusBoy.values.tolist()
    CampusBoy.insert(0, Campus_col)
    CampusGirl = CampusGirl.values.tolist()
    CampusGirl.insert(0, Campus_col)
    BotBoy = BotBoy.values.tolist()
    BotBoy.insert(0, Bot_col)
    BotGirl = BotGirl.values.tolist()
    BotGirl.insert(0, Bot_col)

    return CampusBoy, CampusGirl, BotBoy, BotGirl
    
    # 永久地址=>國籍
