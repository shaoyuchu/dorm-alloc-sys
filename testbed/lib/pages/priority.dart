import 'package:flutter/material.dart';

class Priority extends StatefulWidget {
  @override
  _PriorityState createState() => _PriorityState();
}

class _PriorityState extends State<Priority> {
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
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: <Widget>[

            // title
            Expanded(
              flex: 2,
              child: Container(
                padding: EdgeInsets.symmetric(horizontal: 150.0),
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
                        fontSize: 12.0,
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