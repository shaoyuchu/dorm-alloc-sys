// import 'dart:js';
import 'package:flutter/material.dart';

List<String> flatten(List<List<String>> li) {
  return li.expand((i) => i).toList();
}

class Priority extends StatefulWidget {
  @override
  _PriorityState createState() => _PriorityState();
}

class _PriorityState extends State<Priority> {

  List<String> identityPool = [
    '港澳生',
    '本國生',
    '原住民族籍',
    '邊疆生',
    '大陸來歸生',
    '外籍生',
    '外交人員子女學生',
    '蒙藏生',
    '僑生',
    '退伍軍人',
    '陸生',
    '交換生',
    '公費生',
    '奧林匹亞',
    '身心障礙',
    '離島地區生',
    '低收入戶',
    '中低收入戶',
  ];
  List<List<String>> identitySelected = [];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,

      // app bar
      appBar: AppBar(
        title: Text(
          '臺大宿舍抽籤系統',
          style: TextStyle(
            fontSize: 28.0,
            color: Colors.white,
            fontFamily: 'Noto_Sans_TC',
            fontWeight: FontWeight.w500,
          ),
        ),
        centerTitle: false,
        backgroundColor: Colors.indigo[700],
        elevation: 0.0,
      ),
      
      // body
      body: 
      Container(
        margin: EdgeInsets.symmetric(vertical: 30.0),
        padding: EdgeInsets.symmetric(horizontal: 120.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: <Widget>[

            // title
            Expanded(
              flex: 2,
              child: Container(
                child: Align(
                  alignment: Alignment.centerLeft,
                  child: Text(
                    '[ 步驟二 ] 選擇身份別優先序',
                    style: TextStyle(
                      color: Colors.black,
                      fontFamily: 'Noto_Sans_TC',
                      fontWeight: FontWeight.w700,
                      fontSize: 24.0,
                    ),
                  ),
                ),
              ),
            ),

            // identity selector
            Expanded(
              flex: 10,
              child: Container(
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    // identity pool
                    Expanded(
                      flex: 5,
                      child: Container(
                        color: Colors.grey[300],
                        child: ListView.builder(
                          itemCount: identityPool.length,
                          itemBuilder: (context, index) {
                            return Card(
                              child: ListTile(
                                title: Text(
                                  identityPool[index],
                                  style: TextStyle(
                                    color: Colors.black,
                                    fontFamily: 'Noto_Sans_TC',
                                    fontWeight: FontWeight.w500,
                                    fontSize: 15.0,
                                  ),
                                ),
                                trailing: IconButton(
                                  icon: Icon(Icons.add),
                                  iconSize: 18.0,
                                  color: flatten(identitySelected).contains(identityPool[index])? Colors.grey[300] : Colors.grey[600],
                                  splashColor: Colors.transparent,
                                  highlightColor: Colors.transparent,
                                  tooltip: flatten(identitySelected).contains(identityPool[index])? null : '新增',
                                  hoverColor: Colors.transparent,
                                  onPressed: () {
                                    if(flatten(identitySelected).contains(identityPool[index]) == false) {
                                      setState(() {
                                        identitySelected.add([identityPool[index]]);
                                        print('identitySelected $identitySelected');
                                      });
                                    }
                                  },
                                )
                              ),
                            );
                          },
                        ),
                      ),
                    ),

                    Expanded(
                      flex: 1,
                      child: SizedBox(),
                    ),

                    // selected and ordered identities
                    // TODO: send JSON list of list to backend
                    Expanded(
                      flex: 5,
                      child: Container(
                        color: Colors.grey[300],
                        child: ListView.builder(
                          itemCount: identitySelected.length,
                          itemBuilder: (contextLevel1, indexLevel1) {
                            return Card(
                              child: ListTile(
                                title: Row(
                                  mainAxisAlignment: MainAxisAlignment.spaceAround,
                                  crossAxisAlignment: CrossAxisAlignment.center,
                                  children: [
                                    // leading index
                                    Flexible(
                                      flex: 1,
                                      child: Text(
                                        '${indexLevel1+1}',
                                        style: TextStyle(
                                          color: Colors.grey[600],
                                          fontFamily: 'Noto_Sans_TC',
                                          fontWeight: FontWeight.w500,
                                          fontSize: 16.0,
                                        ),
                                      ),
                                    ),
                                    // card sets
                                    Flexible(
                                      flex: 5,
                                      child: ListView.builder(
                                        itemCount: identitySelected[indexLevel1].length,
                                        shrinkWrap: true,
                                        itemBuilder: (contextLevel2, indexLevel2) {
                                          return Card(
                                            child: ListTile(
                                              title: Text(
                                                identitySelected[indexLevel1][indexLevel2],
                                                style: TextStyle(
                                                  color: Colors.black,
                                                  fontFamily: 'Noto_Sans_TC',
                                                  fontWeight: FontWeight.w500,
                                                  fontSize: 15.0,
                                                ),
                                              ),
                                              // TODO: add trailing buttons
                                            ),
                                          );
                                        }
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            );
                          },
                        ),
                      ),
                    ),
                  ],
                ),
              )
            ),

            // done button
            Expanded(
              flex: 2,
              child: Container(
                padding: EdgeInsets.symmetric(vertical: 15.0),
                child: ButtonTheme(
                    height: 5.0,
                    child: FlatButton(
                    onPressed: () {
                      // Navigator.pushReplacementNamed(context, '/result');
                      Navigator.pushNamed(context, '/result');
                      print('done button clicked');
                    },
                    child: Text(
                      '完成',
                      style: TextStyle(
                        color: Colors.white,
                        fontFamily: 'Noto_Sans_TC',
                        fontWeight: FontWeight.w100,
                        fontSize: 14.0,
                      ),
                    ),
                    color: Colors.indigo,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(50.0),
                    ),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),

    );
  }
}