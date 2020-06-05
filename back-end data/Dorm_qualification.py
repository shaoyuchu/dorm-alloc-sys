import sys
import pandas as pd
import numpy as np
from pandas.api.types import CategoricalDtype
from random import *
from qua_config import *

# 前面來的 ID_order 資料會是 list(list())



# distinguish type of identities
# the list that push to front
def ori_id_set(origin_df):
    id_col_name  = ['身分別1','身分別2','身分別3','特殊身份別']
    column       = [str(x) for i in range(len(id_col_name)) for x in origin_df[id_col_name[i]].tolist() if str(x)!='nan']
    return list(set(column))


# show the list to the front and get the arranged id_list order back
# assume we have the ordered list
def get_id_dict(id_list):
    index_value   = 1
    id_dict       = dict()
    for i in range(len(id_list)):
        if(id_list[i] not in id_dict.keys()):
            id_dict[id_list[i]]   =  index_value
            index_value           += 1
    return id_dict


# organized origin df
# didn't consider if identity need to be qualified

# 身心障礙、低收入戶、中低收入戶、離島、原住民、僑外、國際生、
# 外交人員子女、醫學系公費生、北北基及桃園以外的縣市、桃園

# exception: 
#    1. 身障生、中低收入戶、離島生、自選身份 四個要審核, 寫死了
#    2. 
def get_str2int(origin_df):
    id_list               = ori_id_set(origin_df)
    # sent id_list to front
    # receive order list from front
#     id_dict               = get_id_dict(id_list)

    # temp use default id_dict
    
    id_index                           = [0 for i in range(len(origin_df))]
    willing_index                      = [0 for i in range(len(origin_df))]
    for index, row in origin_df.iterrows():
        # check if have special identity_type & audit status
        for i in id_col_name:
            if(str(row[i])!='nan' and row[i] in id_dict.keys() and id_dict[row[i]]>id_index[index]):
                if(i == '特殊身份別' or row[i] in audit_list):
                    if(row['審查狀態']=='通過'):
                        id_index[index]    = id_dict[row[i]]
                else:
                    id_index[index]    = id_dict[row[i]]
        # no special identity_type, check the habitation
        if(id_index[index] == 0):
            id_index[index]        = len(id_dict) + 2 if row['戶籍地'] in last_order_habitation else len(id_dict)+1
        # willing_index assign
        if(str(row['校內外意願'])!='nan'):
            willing_index[index]   = willing_InOutCam[row['校內外意願']]
    origin_df['校內外意願']          = willing_index
    origin_df['id_index']          = id_index
    return origin_df


# select qualification function

# input the df that order by id_index
def assign_qualificaiton(df,bedNum =100):
    id_count                = df.groupby('id_index')['id_index'].count().tolist()
    curI                    = 0
    if(df.at[0,'id_index'] == 1):
        curI                = id_count[0]
        id_count            = id_count[1:]
    while(bedNum>0):
        if(len(id_count)>0):
            RandomOrder     = sample([i for i in range(id_count[0])],k=id_count[0]) if(id_count[0]<bedNum) else sample([i for i in range(id_count[0])],k=bedNum)
            for i in RandomOrder:
                df.at[curI+i,'資格'] = 1
                bedNum          -= 1
                if(bedNum ==0 ):
                    break
            curI            = curI + id_count[0]
            id_count        = id_count[1:] 
        else:
            break
    return df

# alOutCam

def alCamOrderAssign(df):
    id_count            = df.groupby('id_index')['id_index'].count().tolist()
    curI                = 0
    OnListNum           = 1
    for idC in id_count:
        RandomOrder     = sample([i for i in range(idC)],k=idC)
        for i in RandomOrder:
            df.at[curI+i,'資格'] = OnListNum
            OnListNum           += 1
        curI            = curI + idC
    return df
            

def MainFunc(origin_df):
    # execute
    # original data with deleted no needed column, id_type => int
    origin_df      = origin_df.drop(columns=Ori_ColumnToBeDrop)
    origin_df       = get_str2int(origin_df)

    
    # get inCampus df & alOutCam
    # organize df
    origin_df          = origin_df.sort_values(by = '校內外意願').reset_index(drop = True)
#     InCamNum           = len([i for i in origin_df['校內外意願'] if i != 3])
    InCamNum           = len(origin_df)-origin_df.groupby(['校內外意願']).size()[2]
    
    # inCam_df

    InCam_df           = origin_df.iloc[:InCamNum,:]
    InCam_df           = InCam_df.sort_values(by = '性別').drop(columns=InCam_ColumnToBeDrop).reset_index(drop = True)


    InCam_df['宿舍']    = 0
    InCam_df['房號']    = 0
    InCam_df['床位']    = 0
    InCam_df['資格']    = [2 if (row['id_index']==1) else 0 for index,row in InCam_df.iterrows()]
    GirlInCamNum       = InCam_df.groupby(['性別']).size()['女性']
    GirlInCam          = InCam_df.iloc[:GirlInCamNum,:].sort_values(by='id_index').reset_index(drop=True)
    BoyInCam           = InCam_df.iloc[GirlInCamNum:,:].sort_values(by='id_index').reset_index(drop=True)

    OutCam_Aldf        = origin_df.iloc[InCamNum:,:]


    # get qualification of boy&girl df
    GirlInCam  = assign_qualificaiton(GirlInCam,BedNum)
    BoyInCam  = assign_qualificaiton(BoyInCam,BedNum)
    GirlInCam          = GirlInCam.sort_values(by='資格').reset_index(drop=True)
    BoyInCam           = BoyInCam.sort_values(by='資格').reset_index(drop=True)


    # InCam_alDf
    alGirlNum          = GirlInCam.groupby('資格')['資格'].count().tolist()[0]
    alBoyNum           = BoyInCam.groupby('資格')['資格'].count().tolist()[0]
    twoAlDf            = [GirlInCam.iloc[:alGirlNum,:],BoyInCam.iloc[:alBoyNum]]
    InCam_Aldf         = pd.concat(twoAlDf)

    # Output Girl&Boy df
    GirlInCam          = GirlInCam.iloc[alGirlNum:,:]
    BoyInCam           = BoyInCam.iloc[alBoyNum:,:]


    # organize Alternative df
    InCam_Aldf         = InCam_Aldf.drop(columns=InCamAl_ColumnToBeDrop)


    OutCam_Aldf        = OutCam_Aldf.drop(columns=OutCamAl_ColumnToBeDrop)



    # add willingness=1 to OutCam
    InCam_Aldf         = InCam_Aldf.sort_values(by='校內外意願',ascending=False).reset_index(drop=True)
    willingness2Num    = InCam_Aldf.groupby('校內外意願')['校內外意願'].count().tolist()[1]
    will2_df           = InCam_Aldf.iloc[:willingness2Num,:]
    OutCam_Aldf        = OutCam_Aldf.append(will2_df)


    InCam_Aldf         = InCam_Aldf.sort_values(by='id_index').reset_index(drop=True)
    OutCam_Aldf        = OutCam_Aldf.sort_values(by='id_index').reset_index(drop=True)



    # alternative order giving
    OutCam_Aldf = alCamOrderAssign(OutCam_Aldf)
    InCam_Aldf  = alCamOrderAssign(InCam_Aldf)

    return GirlInCam, BoyInCam, InCam_Aldf, OutCam_Aldf


    # no need "是否需要安排身障房"
#test param
BedNum = 100
origin_df      = pd.read_csv('BallotApplyUndergraduate.csv', header = 0)



GirlInCam, BoyInCam, InCam_Aldf, OutCam_Aldf = MainFunc(origin_df)

