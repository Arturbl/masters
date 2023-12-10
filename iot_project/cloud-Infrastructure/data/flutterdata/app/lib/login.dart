import 'dart:async';
import 'package:flutter/material.dart';
import 'package:app/sizing.dart';
import 'package:app/service/api.dart';

class Login extends StatefulWidget {
  @override
  _LoginState createState() => _LoginState();
}

class _LoginState extends State<Login> {
  TextEditingController _usernameController =
      new TextEditingController(text: 'artur');
  TextEditingController _passwordController =
      new TextEditingController(text: 'artur');
  String _error1 = '';
  bool _loading = false;

  void _validadeUsernameAndPassword() async {
    setState(() {
      _loading = true;
    });
    String username = _usernameController.text;
    String password = _passwordController.text;
    if (username.isNotEmpty && password.isNotEmpty) {
      Auth.login(_usernameController.text, _passwordController.text)
          .then((value) => {
                if (value == 'Login successful')
                  {
                    Navigator.of(context)
                        .pushNamed('/home', arguments: username)
                  }
                else
                  {_setError(value)}
              });
    } else {
      _setError("Empty fields");
    }
  }

  void _setError(String error) {
    setState(() {
      _error1 = error;
      _loading = false;
    });
    Timer(Duration(seconds: 5), () {
      setState(() {
        _error1 = '';
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          // leading: IconButton(
          // icon: Icon(Icons.arrow_back_ios, color: PersonalizedColor.black,),
          // onPressed: () => Navigator.pop(context),
          // ),
          // titleSpacing: 0,
          automaticallyImplyLeading: false,
          title: Text(
            'Login',
          ),
        ),
        body: Container(
          width: MediaQuery.of(context).size.width,
          decoration: const BoxDecoration(
            color: Colors.white,
          ),
          padding: const EdgeInsets.all(30),
          child: Center(
              child: SizedBox(
            width: Sizing.getScreenWidth(
                context), // MediaQuery.of(context).size.width * 0.65,
            child: SingleChildScrollView(
              child: Column(
                // crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  TextField(
                    controller: _usernameController,
                    autofocus: true,
                    keyboardType: TextInputType.emailAddress,
                    decoration: InputDecoration(
                        filled: true,
                        fillColor: Colors.white,
                        hintText: 'username',
                        focusedBorder: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(30),
                            borderSide: BorderSide(color: Colors.grey)),
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(30),
                        ),
                        prefixIcon: Icon(Icons.person, color: Colors.black)),
                  ),
                  Padding(
                    padding: const EdgeInsets.only(top: 15),
                    child: TextField(
                      controller: _passwordController,
                      obscureText: true,
                      keyboardType: TextInputType.text,
                      decoration: InputDecoration(
                          filled: true,
                          fillColor: Colors.white,
                          hintText: 'Password',
                          focusedBorder: OutlineInputBorder(
                              borderRadius: BorderRadius.circular(30),
                              borderSide: const BorderSide(color: Colors.grey)),
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(30),
                          ),
                          prefixIcon: Icon(Icons.vpn_key, color: Colors.black)),
                    ),
                  ),
                  _error1 != null
                      ? Container(
                          //padding: EdgeInsets.only(top: 5),
                          child: Center(
                            child: Text(_error1,
                                style:
                                    TextStyle(color: Colors.red, fontSize: 14)),
                          ),
                        )
                      : Container(),
                  Padding(
                    padding: const EdgeInsets.only(top: 5),
                    child: TextButton(
                      child: _loading == false
                          ? Text(
                              'Login',
                              style: TextStyle(
                                  color: Colors.black,
                                  fontSize: Sizing.fontSize),
                            )
                          : CircularProgressIndicator(
                              color: Colors.black,
                            ),
                      onPressed: () {
                        _validadeUsernameAndPassword();
                      },
                    ),
                  ),
                  Padding(
                    padding: EdgeInsets.only(top: 8),
                    child: GestureDetector(
                      onTap: () {
                        String username = _usernameController.text;
                        Navigator.of(context).pushNamed('/createAccount');
                      },
                      child: const Center(
                        child: Text(
                          'Create new account',
                          style: TextStyle(color: Colors.blue),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          )),
        ));
  }
}
