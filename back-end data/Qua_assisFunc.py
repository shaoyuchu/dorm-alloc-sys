from Qua_config import *
# assistant func 

def countBedNum(DormList):
    BedNum = {'男性':0,'女性':0}
    for index, row in DormList.iterrows():
        if('男' in row['dormName'] and row['is_disability']==0):
            BedNum['男性'] += 1
        elif('女' in row['dormName'] and row['is_disability']==0):
            BedNum['女性'] += 1
    return BedNum

def get_id_dict(id_list):
    index_value   = 1
    id_dict       = dict()
    for i in range(len(id_list)):
        for j in id_list[i]:
            if(j not in id_dict.keys()):
                id_dict[j]   =  i+1
    return id_dict

def get_audit_dict(id_dict):
    audit_dict = dict()
    for i in audit_list:
        audit_dict[i] = id_dict[i]
    return audit_dict

def get_str2int(id_dict, audit_dict, StudentList):
    
    id_index                           = [0 for i in range(len(StudentList))]
    willing_index                      = [0 for i in range(len(StudentList))]
    for index, row in StudentList.iterrows():
        # check if have special identity_type & audit status
        for i in id_col_name:
            if(str(row[i])!='nan' and row[i] in id_dict.keys() and id_dict[row[i]]>id_index[index]):
                if(i == '特殊身份別' or id_dict[row[i]] in list(audit_dict.values())):
                    if(row['審查狀態']=='通過'):
                        id_index[index]    = id_dict[row[i]]
                else:
                    id_index[index]    = id_dict[row[i]]
        # no special identity_type, check the habitation
        idDictNum = max(id_dict.values())
        if(id_index[index] == 0):
            if(row['戶籍地']=='桃園市'):
                id_index[index] = idDictNum + 2
            elif(row['戶籍地'] in last_order_habitation):
                id_index[index] = idDictNum + 3
            else:
                id_index[index] = idDictNum + 1
        # willing_index assign
        if(str(row['校內外意願'])!='nan'):
            willing_index[index]   = willing_InOutCam[str(row['校內外意願'])]
    StudentList['校內外意願'] = willing_index
    StudentList['id_index'] = id_index
    return StudentList

def assign_qualificaiton(df,BedNumDict):
    bedNum = BedNumDict[df.at[0,'性別']]
    id_count = df.groupby('id_index')['id_index'].count().tolist()
    curI = 0
    while(bedNum>0 and len(id_count)>0):
        if(bedNum-id_count[0]>=0):
            for i in range(id_count[0]):
                if(df.at[curI+i,'資格']==0):
                    df.at[curI+i,'資格'] = 1
                    bedNum -= 1
        else:
            RandomOrder = sample([i for i in range(id_count[0])],k=id_count[0]) if(id_count[0]<bedNum) else sample([i for i in range(id_count[0])],k=bedNum)
            for i in RandomOrder:
                df.at[curI+i,'資格'] = 1
                bedNum -= 1
                if(bedNum ==0 ):
                    break
        curI = curI + id_count[0]
        id_count = id_count[1:] 

    return df

def dealWithPreference(df):
    PfCol = ['區域志願1', '區域志願2', '區域志願3']
    for i, row in df.iterrows():
        for j in PfCol:
            if(str(row[j])=='nan'):
                df.at[i,j] = '一般區域'
    return df

def OrderAssign(df):
    df = df.sort_values('id_index').reset_index(drop = True)
    id_count            = df.groupby('id_index')['id_index'].count().tolist()
    curI                = 0
    OnListNum           = 1
    for idC in id_count:
        RandomOrder     = sample([i for i in range(idC)],k=idC)
        for i in RandomOrder:
            df.at[curI+i,'順位序號'] = OnListNum
            OnListNum           += 1
        curI            = curI + idC
    return df