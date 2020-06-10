import 'dart:io';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:json_annotation/json_annotation.dart';
import 'package:file_utils/file_utils.dart';
import 'package:flutter/services.dart';

import 'package:flutter_file_dialog/flutter_file_dialog.dart';
import 'package:excel/excel.dart';
import 'package:testbed/pages/inputWidget.dart';
import 'package:file_chooser/file_chooser.dart';
import '../constant.dart';
import 'dormForm.dart';
import 'file_chooser.dart';
import './resultData/dormData.dart';

import 'testData.dart';
import './inputWidget.dart';

class Result extends StatefulWidget {
  @override
  _ResultState createState() => _ResultState();
}

class _ResultState extends State<Result> with SingleTickerProviderStateMixin {
  
  // deal with tab
  TabController controller;

  DormData dormData;
  InputWidget inputFileName;

  _ResultState()
  {
    // this.dormData = DormData(testData);
    this.inputFileName = InputWidget();
  }
  

  @override
  void initState() {
    super.initState();
    controller = new TabController(vsync: this, length: 4);
  }

  @override
  void dispose() {
    controller.dispose();
    super.dispose();
  }

  void _showDialog() {
    // flutter defined function
    showDialog(
      context: context,
      builder: (BuildContext context) {
        // return object of type Dialog
        return AlertDialog(
          title: new Text('儲存檔案名稱'),
          content: this.inputFileName,
          actions: <Widget>[
            // usually buttons at the bottom of the dialog
            new FlatButton(
              child: new Text('Close'),
              onPressed: () {
                Navigator.of(context).pop();
              },
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    // extract result data
    // final arguments = ModalRoute.of(context).settings.arguments as Map;
    // final result = arguments['result'];
    // print(result.keys);
    this.dormData = DormData(jsonDecode(testData));

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
        actions: <Widget>[
          Container(
            padding: EdgeInsets.all(10),
            child: RaisedButton(
              padding: EdgeInsets.all(0),
              onPressed: () {
                // this.dormData.saveData('/Users/shaoyu/Desktop/', 'result.xlsx');
                showSavePanel(suggestedFileName: '宿舍分配結果.xlsx').then((result) {
                  print(result.paths[0]);
                  this.dormData.saveData(result.paths[0]);
                });
              }, 
              child: Padding(
                padding: EdgeInsets.all(5.0),
                child: Text(
                  '匯出全部資料',
                  style: TextStyle(
                    color: Colors.black,
                    fontFamily: 'Noto_Sans_TC',
                    fontWeight: FontWeight.w300,
                    fontSize: 14.0,
                  ),
                ),
              ),
              color: Colors.amber[300],
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(18.0),
              ),
            )
          )
        ], 
        bottom: new TabBar(
          controller: controller,
          tabs: <Tab>[
            new Tab(text: chi_boyDorm),
            new Tab(text: chi_girlDorm),
            new Tab(text: chi_bot_boy),
            new Tab(text: chi_bot_girl),
          ]
        )


      ),
      
      // body
      body: TabBarView(
        controller: controller,
        children: <Widget>[
          dormData.dormData[boyDorm],
          dormData.dormData[girlDorm],
          dormData.dormData[bot_boy], 
          dormData.dormData[bot_girl]
        ]
      ),
      // bottomNavigationBar: Text(jsonDecode(testing)),
    );
  }

}