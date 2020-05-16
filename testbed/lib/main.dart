// Copyright 2018 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import 'dart:io' show Platform;
import 'dart:math' as math;

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import 'package:color_panel/color_panel.dart';
import 'package:file_chooser/file_chooser.dart';
import 'package:menubar/menubar.dart';
import 'package:path_provider/path_provider.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:url_launcher/url_launcher.dart' as url_launcher;
import 'package:window_size/window_size.dart' as window_size;

import 'keyboard_test_page.dart';

// The shared_preferences key for the testbed's color.
const _prefKeyColor = 'color';

void main() {
  // Try to resize and reposition the window to be half the width and height
  // of its screen, centered horizontally and shifted up from center.
  WidgetsFlutterBinding.ensureInitialized();
  window_size.getWindowInfo().then((window) {
    if (window.screen != null) {
      final screenFrame = window.screen.visibleFrame;
      final width = math.max((screenFrame.width / 2).roundToDouble(), 800.0);
      final height = math.max((screenFrame.height / 2).roundToDouble(), 600.0);
      final left = ((screenFrame.width - width) / 2).roundToDouble();
      final top = ((screenFrame.height - height) / 3).roundToDouble();
      final frame = Rect.fromLTWH(left, top, width, height);
      window_size.setWindowFrame(frame);
      window_size.setWindowTitle('Flutter Testbed on ${Platform.operatingSystem}');

      if (Platform.isMacOS) {
        window_size.setWindowMinSize(Size(800, 600));
        window_size.setWindowMaxSize(Size(1600, 1200));
      }
    }
  });

  runApp(MaterialApp(
    debugShowCheckedModeBanner: false,
    home: Home(),
  ));
  
}

class Home extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(

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
      Column(
        children: <Widget>[

          // three main panels
          Expanded(
            flex: 12,
            child: Container(
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                crossAxisAlignment: CrossAxisAlignment.center,
                children: <Widget>[
                  Expanded(
                    child: Container(
                      margin: EdgeInsets.symmetric(vertical: 50.0, horizontal: 30.0),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: <Widget>[
                          
                          // left-up panel
                          Expanded(
                            child: Container(
                              color: Colors.indigo[50],
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
                                        onPressed: () {
                                          print('left-up button clicked');
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
                          
                          // left-down panel
                          Expanded(
                            child: Container(
                              color: Colors.indigo[100],
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

                        ],
                      ),
                    ),
                  ),

                  // right panel
                  Expanded(
                    child: Container(
                      margin: EdgeInsets.symmetric(vertical: 50.0, horizontal: 30.0),
                      color: Colors.indigo[200],
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: <Widget>[

                          Text(
                            '選擇身份別優先序',
                            style: TextStyle(
                              color: Colors.black,
                              fontFamily: 'Noto_Sans_TC',
                              fontWeight: FontWeight.w300,
                              fontSize: 24.0,
                            ),
                          ),

                          // TODO: add list
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),

          // done button
          Expanded(
            flex: 1,
            child: Container(
              margin: EdgeInsets.symmetric(vertical: 5.0, horizontal: 30.0),
              child: FlatButton(
                onPressed: () {
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

      backgroundColor: Colors.white,
    );
  }
}