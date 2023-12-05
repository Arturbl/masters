import 'dart:async';
import 'dart:js_interop';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:app/sizing.dart';
import 'package:app/service/api.dart';

class CreateAccount extends StatefulWidget {
  @override
  _CreateAccountState createState() => _CreateAccountState();
}

class _CreateAccountState extends State<CreateAccount> {
  bool _visible = false;
  String _visibleText = 'Continue';
  CrossAxisAlignment _align = CrossAxisAlignment.end;
  String _erro1 = '';

  int _age = 0;
  String _gender = 'Male'; // Set a default value
  double _height = 0;
  double _weight = 0;

  final List<String> genderOptions = ['Male', 'Female'];

  TextEditingController _nomeController = TextEditingController();
  TextEditingController _senhaController =
      TextEditingController(text: "1234567956526");
  TextEditingController _senhaConfirmController =
      TextEditingController(text: "1234567956526");

  bool _checkNameAndEmail() {
    String nome = _nomeController.text;
    if (nome.isNotEmpty) {
      if (nome.length <= 10) {
        return true;
      }
      _setError('Username length cannot be longer than 10 characters');
      return false;
    }
    _setError('Check for missing fields');
    return false;
  }

  void _setError(String error) {
    if (mounted) {
      setState(() {
        _erro1 = error;
      });
      Timer(const Duration(seconds: 5), () {
        setState(() {
          _erro1 = '';
        });
      });
    }
  }

  void _verifyPasswordsMatch() async {
    String name = _nomeController.text;
    String pass = _senhaController.text;
    String confirmPass = _senhaConfirmController.text;
    if (pass.isNotEmpty && confirmPass.isNotEmpty) {
      if (pass.trim() == confirmPass.trim()) {
        if (pass.length >= 6) {
          if (_checkNameAndEmail()) {
            setState(() {
              _visible = true;
              _visibleText = '';
              _align = CrossAxisAlignment.stretch;
            });
          } else {
            _setError("Error in name");
          }
        } else {
          _setError('Password must have at least 6 characters');
        }
      } else {
        _setError('Passwords must match');
      }
    } else {
      _setError('Passwords must not be empty');
    }
  }

  void _submitForm() {
    if (_isFormValid()) {
      int heightInInt = (_height).toInt();
      int weightInInt = (_weight).toInt();
      Auth.registerNewUser(_nomeController.text, _senhaController.text, _age,
              _gender, heightInInt, weightInInt)
          .then((value) => {Navigator.of(context).pushNamed('/login')});
    } else {
      _setError('Please fill in all the fields');
    }
  }

  bool _isFormValid() {
    return _nomeController.text.isNotEmpty &&
        _senhaController.text.isNotEmpty &&
        _senhaConfirmController.text.isNotEmpty &&
        _age > 0 &&
        _height > 0 &&
        _weight > 0;
  }

  @override
  void dispose() {
    _nomeController.dispose();
    _senhaController.dispose();
    _senhaConfirmController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        leading: IconButton(
          icon: Icon(
            Icons.arrow_back_ios,
            color: Colors.black,
          ),
          onPressed: () => Navigator.pop(context),
        ),
        titleSpacing: 0,
        title: Text(
          'Create new account',
          style: TextStyle(color: Colors.black),
        ),
        backgroundColor: Colors.blue,
      ),
      body: Container(
        width: MediaQuery.of(context).size.width,
        decoration: BoxDecoration(
          color: Colors.white,
        ),
        padding: const EdgeInsets.fromLTRB(30, 5, 30, 0),
        child: Center(
          child: SizedBox(
            width: Sizing.getScreenWidth(context),
            child: SingleChildScrollView(
              child: Column(
                crossAxisAlignment: _align,
                children: [
                  Visibility(
                    visible: !_visible,
                    child: TextField(
                      controller: _nomeController,
                      autofocus: true,
                      keyboardType: TextInputType.text,
                      decoration: InputDecoration(
                        filled: true,
                        fillColor: Colors.white,
                        hintText: 'Username',
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(30),
                        ),
                        focusedBorder: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(30),
                          borderSide: BorderSide(color: Colors.grey),
                        ),
                        prefixIcon: Icon(
                          Icons.person,
                          color: Colors.black,
                        ),
                      ),
                    ),
                  ),
                  Visibility(
                    visible: !_visible,
                    child: Padding(
                      padding: EdgeInsets.only(top: 10),
                      child: TextField(
                        obscureText: true,
                        controller: _senhaController,
                        decoration: InputDecoration(
                          filled: true,
                          fillColor: Colors.white,
                          hintText: 'Password',
                          focusedBorder: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(30),
                            borderSide: BorderSide(color: Colors.grey),
                          ),
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(30),
                          ),
                          prefixIcon: Icon(Icons.vpn_key, color: Colors.black),
                        ),
                      ),
                    ),
                  ),
                  Visibility(
                    visible: !_visible,
                    child: Padding(
                      padding: EdgeInsets.only(top: 10),
                      child: TextField(
                        obscureText: true,
                        controller: _senhaConfirmController,
                        decoration: InputDecoration(
                          filled: true,
                          fillColor: Colors.white,
                          hintText: 'Confirm password',
                          focusedBorder: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(30),
                            borderSide: BorderSide(color: Colors.grey),
                          ),
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(30),
                          ),
                          prefixIcon: Icon(Icons.vpn_key, color: Colors.black),
                        ),
                      ),
                    ),
                  ),
                  Visibility(
                    visible: _visible,
                    child: Container(
                      padding: EdgeInsets.all(16.0),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text('Personal Information:'),
                          SizedBox(height: 8.0),
                          TextFormField(
                            decoration: InputDecoration(
                              labelText: 'Age',
                              filled: true,
                              fillColor: Colors.white,
                              border: OutlineInputBorder(
                                borderRadius: BorderRadius.circular(30),
                              ),
                            ),
                            keyboardType: TextInputType.number,
                            onChanged: (value) {
                              setState(() {
                                _age = int.tryParse(value) ?? 0;
                              });
                            },
                          ),
                          const SizedBox(height: 16.0),
                          DropdownButtonFormField<String>(
                            value: _gender,
                            items: genderOptions.map((String value) {
                              return DropdownMenuItem<String>(
                                value: value,
                                child: Text(value),
                              );
                            }).toList(),
                            onChanged: (String? value) {
                              setState(() {
                                _gender = value!;
                              });
                            },
                            decoration: InputDecoration(
                              labelText: 'Gender',
                              filled: true,
                              fillColor: Colors.white,
                              border: OutlineInputBorder(
                                borderRadius: BorderRadius.circular(30),
                              ),
                            ),
                          ),
                          const SizedBox(height: 16.0),
                          TextFormField(
                            decoration: InputDecoration(
                              labelText: 'Height (cm)',
                              filled: true,
                              fillColor: Colors.white,
                              border: OutlineInputBorder(
                                borderRadius: BorderRadius.circular(30),
                              ),
                            ),
                            keyboardType: TextInputType.number,
                            onChanged: (value) {
                              setState(() {
                                _height = double.tryParse(value) ?? 0.0;
                              });
                            },
                          ),
                          TextFormField(
                            decoration: InputDecoration(
                              labelText: 'Weight (kg)',
                              filled: true,
                              fillColor: Colors.white,
                              border: OutlineInputBorder(
                                borderRadius: BorderRadius.circular(30),
                              ),
                            ),
                            keyboardType: TextInputType.number,
                            onChanged: (value) {
                              setState(() {
                                _weight = double.tryParse(value) ?? 0.0;
                              });
                            },
                          ),
                        ],
                      ),
                    ),
                  ),
                  Visibility(
                    visible: _visible,
                    child: ElevatedButton(
                      onPressed: () {
                        _submitForm();
                      },
                      child: Text('Submit'),
                    ),
                  ),
                  Padding(
                    padding: EdgeInsets.only(top: 15),
                    child: TextButton(
                      child: Text(
                        _visibleText,
                        style: TextStyle(
                          color: Colors.black,
                          fontSize: Sizing.fontSize,
                        ),
                      ),
                      onPressed: () {
                        if (!_visible) {
                          _verifyPasswordsMatch();
                        }
                      },
                    ),
                  ),
                  _erro1 != null
                      ? Center(
                          child: Text(
                            _erro1,
                            style: TextStyle(
                              color: Colors.red,
                              fontSize: Sizing.fontSize,
                            ),
                          ),
                        )
                      : Container(),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
