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
    home: Home(),
  ));
  
}

class Home extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(

      // app bar
      appBar: AppBar(
        title: Text('臺大宿舍抽籤系統'),
        centerTitle: false,
        backgroundColor: Colors.indigo[700],
      ),

      // body
      body: Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: <Widget>[
          // left panel
          Column(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: <Widget>[
              // left-up
              Container(
                color: Colors.indigo[100],
                padding: EdgeInsets.symmetric(vertical: 10.0, horizontal: 20.0),
                child: FlatButton.icon(
                  onPressed: () {
                    print('left-up button clicked');
                  },
                  icon: Icon(
                    Icons.cloud_upload,
                    color: Colors.indigo[50],
                  ),
                  label: Text(
                    'Import',
                    style: TextStyle(color: Colors.white),
                  ),
                  color: Colors.indigo,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(18.0),
                  ),
                ),
              ),
              // left-down
              Container(
                color: Colors.indigo[100],
                padding: EdgeInsets.symmetric(vertical: 10.0, horizontal: 20.0),
                child: FlatButton.icon(
                  onPressed: () {
                    print('left-down button clicked');
                  },
                  icon: Icon(
                    Icons.cloud_upload,
                    color: Colors.indigo[50],
                  ),
                  label: Text(
                    'Import',
                    style: TextStyle(color: Colors.white),
                  ),
                  color: Colors.indigo,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(18.0),
                  ),
                ),
              ),
            ],
          ),
          

          // right panel
          Container(
            color: Colors.indigo[100],
            padding: EdgeInsets.symmetric(vertical: 10.0, horizontal: 20.0),
            child: FlatButton.icon(
              onPressed: () {
                print('right button clicked');
              },
              icon: Icon(
                Icons.cloud_upload,
                color: Colors.indigo[50],
              ),
              label: Text(
                'Import',
                style: TextStyle(color: Colors.white),
              ),
              color: Colors.indigo,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(18.0),
              ),
            ),
          ),
        ],
      ),

      backgroundColor: Colors.white,

    );
  }
}