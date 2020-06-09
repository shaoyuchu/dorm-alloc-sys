import 'package:flutter/material.dart';

class InputWidget extends StatefulWidget {
  InputWidget({Key key}) : super(key: key)
  {
    this.fileName = '分配結果';
  }
  
  String fileName;

  @override
  _InputWidgetState createState() => _InputWidgetState();
}

class _InputWidgetState extends State<InputWidget> {
  final _formKey = GlobalKey<FormState>();
  final myController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: <Widget>[
          TextFormField(
            decoration: const InputDecoration(
              hintText: '請輸入檔名',
            ),
            validator: (value) {
              if (value.isEmpty) {
                return '輸入不可為空';
              }
              return null;
            },
            controller: myController,
          ),
          Padding(
            padding: const EdgeInsets.symmetric(vertical: 16.0),
            child: RaisedButton(
              onPressed: () {
                // Validate will return true if the form is valid, or false if
                // the form is invalid.
                if (_formKey.currentState.validate()) {
                  widget.fileName = myController.text;
                  Navigator.of(context).pop();
                }
              },
              child: Text('Submit')
            ),
          ),
        ],
      ),
    );
  }
}
