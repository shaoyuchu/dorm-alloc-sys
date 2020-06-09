import 'dart:convert';
import 'dart:io';
import 'package:path/path.dart' as p;
import 'package:excel/excel.dart';
import '../../constant.dart';
import 'dormTable.dart';

class DormData{
  Map dormData;

  DormData(json)
  {
    this.dormData = new Map();

    for(int a = 0; a < dataName.length; a++) {
      this.dormData[dataName[a]] = DormTable(dataName[a], json[dataName[a]]);
    }
  }

  void saveData(folderPath, fileName)
  {
    String store_path = p.join(folderPath, fileName);
    var excel = Excel.createExcel();

    this.dormData.forEach((dormName, dormTable){
      dormTable.saveTable(excel);
    }); 

    // excel.delete("Sheet1");

    // excel.getDefaultSheet().then((String defaultSheetName) {
    //   excel.delete(defaultSheetName);
    // });

    excel.encode().then((onValue) {
      File(store_path)
      ..createSync(recursive: true)
      ..writeAsBytesSync(onValue);
  });

  }

}