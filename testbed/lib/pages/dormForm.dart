import 'package:flutter/material.dart';
import '../constant.dart';
import 'testData.dart';
import './resultData/dormData.dart';
import './resultData/dormTable.dart';

// 暫時廢棄
class DormForm extends StatefulWidget {
  String dormName;
  DormTable dormTable;
  DormForm(this.dormName, this.dormTable);

  @override
  _FormState createState() => _FormState(this.dormName, this.dormTable);
}

class _FormState extends State<DormForm> {
  String dormName;
  DormTable dormTable;

  _FormState(this.dormName, this.dormTable);

  @override
  Widget build(BuildContext context) {
    return Container(
      child: SingleChildScrollView(
        scrollDirection: Axis.horizontal, 
        child: this.dormTable
      )
    );
  }
}


// class _FormState extends State<DormForm> {
//   String dormName;

//   // process the data column
//   final List<String> columnName = dataColumnNames;
//   List<DataColumn> dormColumns = [];
//   List<DataRow> dataRows = [];

//   _FormState(this.dormName)
//   {
//     for(int i = 0; i < this.columnName.length; i++)
//     {
//       this.dormColumns.add(DataColumn(
//         label: Text(this.columnName[i]),
//         numeric: false)
//         );
//     }
//       // process the data content

    
//     List<DataCell> dataCells = [];
//     for (int a = 0; a < testRow.length; a++)
//     {
//       dataCells.add(
//           DataCell(
//           Text(testRow[a]),
//           showEditIcon: false,
//           placeholder: false
//         )
//       );
//     }
//     this.dataRows.add(DataRow(
//       cells: dataCells));
//   }

//   // define the dataTable
//   Widget DormTable() => DataTable(
//       onSelectAll: (b) {},
//       sortColumnIndex: 1,
//       sortAscending: true,
//       columns: dormColumns,
//       rows: this.dataRows
//       );

//   @override
//   Widget build(BuildContext context) {
//     return Container(
//       child: SingleChildScrollView(
//         scrollDirection: Axis.horizontal, 
//         child: DormTable()
//       )
//     );
//   }
// }
