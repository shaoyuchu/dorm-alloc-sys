import 'dart:io' show Platform;
import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/services.dart';

import 'package:file_chooser/file_chooser.dart';
import 'package:path_provider/path_provider.dart';
import 'file_chooser.dart';

class Home extends StatefulWidget {
  @override
  _HomeState createState() => _HomeState();
}

class _HomeState extends State<Home> {

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
                    '[ 步驟一 ] 匯入資料',
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

            // two main panels
            Expanded(
              flex: 10,
              child: Container(
                padding: EdgeInsets.symmetric(vertical: 0.0, horizontal: 150.0),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: <Widget>[
                    
                    Divider(
                      height: 5.0,
                      thickness: 3.0,
                      color: Colors.grey[300],
                    ),
                    
                    // up panel
                    Expanded(
                      child: Container(
                        color: Colors.white,
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: <Widget>[
                            Text(
                              '匯入學生資料',
                              style: TextStyle(
                                color: Colors.black,
                                fontFamily: 'Noto_Sans_TC',
                                fontWeight: FontWeight.w300,
                                fontSize: 24.0,
                              ),
                            ),
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              crossAxisAlignment: CrossAxisAlignment.center,
                              children: <Widget>[
                                Text(
                                  '尚未選擇檔案',
                                  style: TextStyle(
                                    color: Colors.grey[700],
                                    fontFamily: 'Noto_Sans_TC',
                                    fontWeight: FontWeight.w100,
                                    fontSize: 12.0,
                                  ),
                                ),
                                FlatButton.icon(
                                  onPressed: () async {
                                    String initialDirectory;
                                    if (Platform.isMacOS || Platform.isWindows) {
                                      initialDirectory = (await getApplicationDocumentsDirectory()).path;
                                    }
                                    final result = await showOpenPanel(
                                        allowsMultipleSelection: false,
                                        initialDirectory: initialDirectory);
                                    print('result');
                                    print(result.paths);
                                  },
                                  icon: Icon(
                                    Icons.cloud_upload,
                                    color: Colors.white,
                                  ),
                                  label: Text(
                                    '選擇檔案',
                                    style: TextStyle(
                                      color: Colors.white,
                                      fontFamily: 'Noto_Sans_TC',
                                      fontWeight: FontWeight.w100,
                                      fontSize: 12.0,
                                    ),
                                  ),
                                  color: Colors.indigo,
                                  shape: RoundedRectangleBorder(
                                    borderRadius: BorderRadius.circular(18.0),
                                  ),
                                ),
                              ],
                            ),
                          ],
                        ),
                      ),
                    ),

                    Divider(
                      height: 5.0,
                      thickness: 1.0,
                      color: Colors.grey[300],
                    ),
                    
                    // down panel
                    Expanded(
                      child: Container(
                        color: Colors.white,
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: <Widget>[
                            Text(
                              '匯入床位資料',
                              style: TextStyle(
                                color: Colors.black,
                                fontFamily: 'Noto_Sans_TC',
                                fontWeight: FontWeight.w300,
                                fontSize: 24.0,
                              ),
                            ),
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              crossAxisAlignment: CrossAxisAlignment.center,
                              children: <Widget>[
                                Text(
                                  '尚未選擇檔案',
                                  style: TextStyle(
                                    color: Colors.grey[700],
                                    fontFamily: 'Noto_Sans_TC',
                                    fontWeight: FontWeight.w100,
                                    fontSize: 12.0,
                                  ),
                                ),
                                FlatButton.icon(
                                  onPressed: () {
                                    print('left-down button clicked');
                                  },
                                  icon: Icon(
                                    Icons.cloud_upload,
                                    color: Colors.white,
                                  ),
                                  label: Text(
                                    '選擇檔案',
                                    style: TextStyle(
                                      color: Colors.white,
                                      fontFamily: 'Noto_Sans_TC',
                                      fontWeight: FontWeight.w100,
                                      fontSize: 12.0,
                                    ),
                                  ),
                                  color: Colors.indigo,
                                  shape: RoundedRectangleBorder(
                                    borderRadius: BorderRadius.circular(18.0),
                                  ),
                                ),
                              ],
                            ),
                          ],
                        ),
                      ),
                    ),

                    Divider(
                      height: 5.0,
                      thickness: 3.0,
                      color: Colors.grey[300],
                    ),

                  ],
                ),
              ),
            ),

            // done button
            Expanded(
              flex: 2,
              child: Container(
                padding: EdgeInsets.symmetric(vertical: 15.0),
                child: FlatButton(
                onPressed: () {
                  // Navigator.pushReplacementNamed(context, '/priority');
                  Navigator.pushNamed(context, '/priority');
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
          ],
        ),
      ),

    );
  }
}

