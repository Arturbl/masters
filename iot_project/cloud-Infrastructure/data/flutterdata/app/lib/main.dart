import 'package:flutter/material.dart';
import 'package:app/login.dart';
import 'package:app/home.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(MaterialApp(
    debugShowCheckedModeBanner: false,
    title: 'Xtream',
    theme: ThemeData(
      primarySwatch: Colors.blue,
    ),
    home: App(),
  ));
}

class App extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Home();
  }
}
