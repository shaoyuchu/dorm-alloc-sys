# DORM MATCHING API DOCUMENT

### `[POST] /api/get_all_identities`
> get all identities from the given student file

Request
```
[
    [col1, col2, col3,...],
    [atr1, atr2, atr3,...].
    [atr1, atr2, atr3,...],
    ...
]
```

Response 200 OK Success
```
[
    identity1,
    identity2,
    identity3,
    identity4,
    ...
]
```
### `[POST] /api/match`
> return all matching results

Request
```
{
    "priority":[
        [identify1, identify2],
        [identify3],
        ...
    ],
    "student":[
        [col1, col2, col3,...],
        [atr1, atr2, atr3,...].
        [atr1, atr2, atr3,...],
    ],
    "beds":[
        [dormName, Room, Bed, Student_ID, is_disability,...],
        [atr1, atr2, atr3,...],
        [atr1, atr2, atr3,...],
    ]
}
```

Response 200 OK Success
```
{
    "men_campus_dorm": [
        [資格狀態,宿舍名稱,寢室,床位,系所名稱,學號,性別,姓名,身份別,校內外意願,區域志願1,區域志願2,區域志願3,戶籍地,國籍,是否需要安排身障房間],
        [atr1, atr2, atr3,...].
        [atr1, atr2, atr3,...],
        ...
    ],
    "women_campus_dorm": [
        [資格狀態,宿舍名稱,寢室,床位,系所名稱,學號,性別,姓名,身份別,校內外意願,區域志願1,區域志願2,區域志願3,戶籍地,國籍,是否需要安排身障房間],
        [atr1, atr2, atr3,...].
        [atr1, atr2, atr3,...],
        ...
    ],
    "men_BOT":[
        [順位序號,系所名稱,學號,性別,姓名,身份別,校內外意願,區域志願1,區域志願2,區域志願3,戶籍地,國籍,是否需要安排身障房間],
        [atr1, atr2, atr3,...].
        [atr1, atr2, atr3,...],
        ...
    ],
    "women_BOT":[
        [順位序號,系所名稱,學號,性別,姓名,身份別,校內外意願,區域志願1,區域志願2,區域志願3,戶籍地,國籍,是否需要安排身障房間],
        [atr1, atr2, atr3,...].
        [atr1, atr2, atr3,...],
        ...
    ]
}
```

## Backend Functions

### Main functions
Return all kinds of unique identities
input
```
def GetAllIdType(StudentList):
    ...
    return  AllIdType
```

Select dormatory qualification
input
```
def DivideDF(ordered_IdList, StudentList, DormList):
    ...
    return GirlQua, BoyQua, WaitDF
```

macthing students
```
 def matching(qualification_students):
     ...
     return matched_students
```
process data for frontend display use
```
def frontend_display_df(result):
    ...
    return display_result
```
> Campus

| 學號 | 資格 | 宿舍 | 房號 | 床位 | 性別 | id_name | 校內外意願 | 區域志願1 | 區域志願2 | 區域志願3 | 永久地址 | 是否需要安排身障房間 | 順位序號 |
| ---- | ---- | ---- | ---- | ---- | ---- | ------- | ---------- | --------- | --------- | --------- | -------- | -------------------- | -------- |
> BOT


| 性別 | 身份別 | 校內外意願 | 永久地址 | 是否需要安排身障房間 | 學號 | 順位序號 |
| ---- | ------ | ---------- | -------- | -------------------- | ---- | -------- |
process data for download use

```
def get_result_for_download():
    ...
    return campus_men, campus_women, bot_men, bot_woman
```
### Helper functions
merge the result back to the original dataframe
```
def matching_postprocess(qualification_students, waiting_students):
    ...
    return merged_result
```
