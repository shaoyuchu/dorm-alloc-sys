  import 'package:flutter/material.dart';
  import 'dormForm.dart';
  import '../constant.dart';

class Result extends StatefulWidget {
  @override
  _ResultState createState() => _ResultState();
}

class _ResultState extends State<Result> with SingleTickerProviderStateMixin {
  
  TabController controller;
  
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

  @override
  Widget build(BuildContext context) {
    // extract result data
    Map arguments = ModalRoute.of(context).settings.arguments as Map;
    Map result = arguments['result'];

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
        actions: <Widget>[Container(
            padding: EdgeInsets.all(10),
            child: RaisedButton(
            padding: EdgeInsets.all(0),
            onPressed: (){}, // !!! not yet set action
            child: Text('Export', style: TextStyle(fontSize: 14)),
            color: Colors.amber[300]
          ))], 
        bottom: new TabBar(
          controller: controller,
          tabs: <Tab>[
            new Tab(text: "男一舍"),
            new Tab(text: "大一女"),
            new Tab(text: "BOT長興宿舍"),
            new Tab(text: "BOT水源宿舍"),
          ]
        )


      ),
      
      // body
      body: TabBarView(
        controller: controller,
        children: <Widget>[
          DormForm(boyDorm),
          DormForm(girlDorm),
          DormForm(bot_CH), 
          DormForm(bot_SY)
        ]
      )

    );
  }
}



// class MyTabsState extends State<MyTabs> with SingleTickerProviderStateMixin {


//   TabController controller;

//   @override
//   void initState() {
//     super.initState();
//     controller = new TabController(vsync: this, length: 3);
//   }

//   @override
//   void dispose() {
//     controller.dispose();
//     super.dispose();
//   }

//   @override
//   Widget build(BuildContext context) {
//     return new Scaffold(
//       appBar: new AppBar(
//         title: new Text("Pages"), 
//         backgroundColor: Colors.deepOrange,
//         bottom: new TabBar(
//           controller: controller,
//           tabs: <Tab>[
//             new Tab(icon: new Icon(Icons.arrow_forward)),
//             new Tab(icon: new Icon(Icons.arrow_downward)),
//             new Tab(icon: new Icon(Icons.arrow_back)),
//           ]
//         )
//       ),
//       bottomNavigationBar: new Material(
//         color: Colors.deepOrange,
//         child: new TabBar(
//           controller: controller,
//           tabs: <Tab>[
//             new Tab(icon: new Icon(Icons.arrow_forward)),
//             new Tab(icon: new Icon(Icons.arrow_downward)),
//             new Tab(icon: new Icon(Icons.arrow_back)),
//           ]
//         )
//       ),
//       body: new TabBarView(
//         controller: controller,
//         children: <Widget>[
//           new first.First(),
//           new second.Second(),
//           new third.Third()
//         ]
//       )
//     );
//   }
// }