import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'create_account.dart';
import 'login.dart';
import 'home.dart';

class RouteGenerator {
  static Route<dynamic> generateRoute(RouteSettings settings) {
    final args = settings.arguments;

    switch (settings.name) {
      case '/createAccount':
        return MaterialPageRoute(builder: (context) => CreateAccount());
      case '/login':
        return MaterialPageRoute(builder: (context) => Login());
      case '/home':
        return MaterialPageRoute(builder: (context) => Home());
      default:
        return _errorRoute();
    }
  }

  static Route<dynamic> _errorRoute() {
    return MaterialPageRoute(builder: (context) {
      return Scaffold(
          appBar: AppBar(
            title: const Text('Route not found.'),
          ),
          backgroundColor: Colors.black,
          body: Center(
              child: Text("Route not found",
                  style: TextStyle(color: Colors.red))));
    });
  }
}
