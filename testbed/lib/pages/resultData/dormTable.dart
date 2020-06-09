import 'package:flutter/material.dart';
import 'package:flutter_material_pickers/flutter_material_pickers.dart';
import 'package:testbed/pages/resultData/dormData.dart';
import 'package:excel/excel.dart' hide DataTable;
import '../../constant.dart';
import '../../constant.dart';

class DormTable extends StatefulWidget{
  String tableName;
  List<List> dataRows = [];
  List<dynamic> dormData = [];
  var candidateValues = new Map();

  DormTable(this.tableName, dormData)
  {
    this.dormData = new List<dynamic>.from(dormData);

    // extract rows
    for(int i = 1; i < (this.dormData.length)-1; i++)
    {
      List dataCells = [];
      for(int j = 0; j < (this.dormData[i].length); j++)
      {
        dataCells.add(this.dormData[i][j]);
      }
      this.dataRows.add(dataCells);
    }

    // extract data Value
    for(int i = 0; i < this.dormData[0].length; i++) // create new Set for every column
    {
      this.candidateValues[this.dormData[0][i]] = new Set();
    }

    for(int i  = 0; i < this.dormData[0].length; i++) // update the Set for every column
    {
      for(int j = 1; j < this.dormData.length; j++)
      {
        this.candidateValues[this.dormData[0][i]].add(this.dormData[j][i]);
      }
    }
    for(int i  = 0; i < this.dormData[0].length; i++)
    {
      List temp = new List.from(this.candidateValues[this.dormData[0][i]].toList());
      this.candidateValues[this.dormData[0][i]] = temp;
    }
  }

  @override
  _TableState createState() => _TableState(this.tableName, this.dataRows, this.dormData, this.candidateValues);

  void saveTable(excel)
  {
    String sheetName = dorm_eng2chi[this.tableName];
    int lineIndex = 'A'.codeUnitAt(0);
    
    // store columns
    for(int i = 0; i < this.dataRows[0].length; i++)
    {
      int columnIndex = 'A'.codeUnitAt(0) + i;
      
      excel.updateCell(sheetName, CellIndex.indexByString(String.fromCharCode(columnIndex)+'1'), 
                      this.dormData[0][i]);
    }
    
    // store rows
    for(int i = 0; i < this.dataRows.length; i++)
    {
      for(int j = 0; j < this.dataRows[0].length; j++)
      {
        int columnIndex = 'A'.codeUnitAt(0) + j;
        int rowIndex = i + 2;
        // var cell = sheet.cell(CellIndex.indexByString(String.fromCharCode(columnIndex) + (rowIndex).toString()));
        // cell.value = this.dataRows[i][j];

        excel.updateCell(sheetName, CellIndex.indexByString(String.fromCharCode(columnIndex) + (rowIndex).toString()), 
                this.dataRows[i][j]);
      }
    }
  }
}

class _TableState extends State<DormTable> {
  // from statefulwidget
  String tableName;
  List<List> dataRows = [];
  List<dynamic> dormData = [];
  var candidateValues = new Map();

  // belong to state
  List<DataColumn> columnName = [];
  List<DataRow> displayRows = [];
  var selectedItem = new Map();
  
  _TableState(this.tableName, this.dataRows, this.dormData, this.candidateValues)
  { 
    // initialized selectedItem
    for(int i = 0; i < this.dormData[0].length; i++)
    {
      this.selectedItem[this.dormData[0][i]] = List.from(this.candidateValues[this.dormData[0][i]]);
    }
    // initialized displayRows, it must be later than the initialization of selecctedItem
    buildDisplayRows();

    // extract columns
    for(int i = 0; i < this.dormData[0].length; i++)
    {
      this.columnName.add(DataColumn(
        label: Row(
          children: <Widget> [
            GestureDetector(
              child: Text(this.dormData[0][i]),
              onTap: (){
                  showMaterialCheckboxPicker(
                    context: context,
                    title: this.dormData[0][i],
                    items: this.candidateValues[widget.dormData[0][i]],
                    selectedItems: this.selectedItem[widget.dormData[0][i]],
                    onChanged: (value) => setState((){
                      this.selectedItem[widget.dormData[0][i]] = value;
                      buildDisplayRows();
                      }),
                );
              },
            )
          ],), 
        

        numeric: false), 
        );
    }
  }

  void buildDisplayRows()
  {
    // initialized
    List<List> data = [];
    for(int i = 0; i < this.dataRows.length; i++)
    {
      List temp = new List.from(this.dataRows[i]);
      data.add(temp);
    }

    this.displayRows.clear();
    List colNames = new List.from(this.dormData[0]);
    for(int i = data.length-1; i >= 0; i--)
    {
      for(int j = 0; j < colNames.length; j++)
      {
        if(!this.selectedItem[colNames[j]].contains(data[i][j]))
        {
          data.removeAt(i);
          break;
        }
      }
    }

    for(int i = 0; i < data.length; i++)
    {
      List<DataCell> dataCells = [];
      for(int j = 0; j < (this.dormData[i].length); j++)
      {
        dataCells.add(
            DataCell(
            Text(data[i][j].toString()),
            showEditIcon: false,
            placeholder: false
          )
        );
      }
      this.displayRows.add(DataRow(
        cells: dataCells));
    }
  }



  @override
  Widget build(BuildContext context) {
    return Container(
      child: SingleChildScrollView(
        scrollDirection: Axis.vertical,
        child: SingleChildScrollView(
          scrollDirection: Axis.horizontal, 
          child: DataTable(
            onSelectAll: (b) {},
            sortColumnIndex: 1,
            sortAscending: true,
            columns: this.columnName,
            rows: this.displayRows
            )
          ),
      )
      );
  }
}