import 'package:flutter/material.dart';
import 'package:json_annotation/json_annotation.dart';
import 'package:file_utils/file_utils.dart';
import 'package:flutter/services.dart';
import 'package:flutter_material_pickers/flutter_material_pickers.dart';
import 'package:flutter_file_dialog/flutter_file_dialog.dart';
import 'dart:io';
import 'package:excel/excel.dart';
import 'package:testbed/pages/inputWidget.dart';
import 'dart:convert';
import '../constant.dart';
import '../constant.dart';
import '../constant.dart';
import '../constant.dart';
import '../constant.dart';
import '../constant.dart';
import '../constant.dart';
import '../constant.dart';
import 'dormForm.dart';
import './resultData/dormData.dart';

import 'testData.dart';
import './inputWidget.dart';

class Result extends StatefulWidget {
  @override
  _ResultState createState() => _ResultState();
}

class _ResultState extends State<Result> {
  
  // deal with tab
  // TabController controller;

  String selectedDorm = chi_boyDorm; 
  DormData dormData;
  InputWidget inputFileName;

  _ResultState()
  {
    // this.dormData = DormData(testData);
    this.inputFileName = InputWidget();
  }
  

  // @override
  // void initState() {
  //   super.initState();
  //   controller = new TabController(vsync: this, length: 4);
  // }

  // @override
  // void dispose() {
  //   controller.dispose();
  //   super.dispose();
  // }

  void _showDialog() {
    // flutter defined function
    showDialog(
      context: context,
      builder: (BuildContext context) {
        // return object of type Dialog
        return AlertDialog(
          title: new Text("儲存檔案名稱"),
          content: this.inputFileName,
          actions: <Widget>[
            // usually buttons at the bottom of the dialog
            new FlatButton(
              child: new Text("Close"),
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
    final arguments = ModalRoute.of(context).settings.arguments as Map;
    final result = arguments['result'];

    this.dormData = DormData(result);

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
            onPressed: (){
              showMaterialScrollPicker(
                context: context,
                title: "選擇宿舍",
                items: chi_dataName,
                selectedItem: this.selectedDorm, 
                onChanged: (value){
                    setState((){this.selectedDorm = value;});
                  }
                );
              },  
            child: Text('其他宿舍結果', style: TextStyle(fontSize: 14)),
            color: Colors.amber[300]
            ),
          ),
          // botton
          Container(
            padding: EdgeInsets.all(10),
            child: RaisedButton(
            padding: EdgeInsets.all(0),
            onPressed: (){
                this._showDialog();
              }, 
            child: Text('變更儲存檔名', style: TextStyle(fontSize: 14)),
            color: Colors.amber[300]
          )), 
          // botton
          Container(
            padding: EdgeInsets.all(10),
            child: RaisedButton(
            padding: EdgeInsets.all(0),
            onPressed: (){
                this.dormData.saveData('D:\\testDormExport', this.inputFileName.fileName+'.xlsx');
              }, 
            child: Text('匯出全部資料', style: TextStyle(fontSize: 14)),
            color: Colors.amber[300]
          ))], 
      ),
      
      // body
      body:Container(
        child: Text(dorm_chi2eng[this.selectedDorm])
        // child: this.dormData.dormData[dorm_chi2eng[this.selectedDorm]]
      )
    );
  }
}