import 'dart:convert';
import 'package:http/http.dart' as http;

class Auth {
  static Future<String> registerNewUser(
    String username,
    String password,
    int age,
    String gender,
    int height,
    int weight,
  ) async {
    final apiUrl = 'http://localhost:8081/register';

    try {
      final response = await http.post(
        Uri.parse(apiUrl),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'username': username,
          'password': password,
          'age': age,
          'gender': gender,
          'height': height,
          'weight': weight,
        }),
      );

      if (response.statusCode == 200) {
        Map<String, dynamic> result = jsonDecode(response.body);
        if (result['result'] == true) {
          return "Registration successful";
        } else {
          return "Registration failed";
        }
      } else {
        return "Failed to register. Status code: ${response.statusCode}";
      }
    } catch (error) {
      return "Error: $error";
    }
  }

  static Future<String> login(String username, String password) async {
    final apiUrl = 'http://localhost:8081/login';

    try {
      final response = await http.post(
        Uri.parse(apiUrl),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'username': username,
          'password': password,
        }),
      );

      if (response.statusCode == 200) {
        bool result = jsonDecode(response.body);
        if (result) {
          return "Login successful";
        } else {
          return "Invalid username or password";
        }
      } else {
        return "Failed to login. Status code: ${response.statusCode}";
      }
    } catch (error) {
      return "Error: $error";
    }
  }

  static Future<Map<String, dynamic>> getHistory(
      String dateBegin, String dateEnd) async {
    final apiUrl = 'http://localhost:8081/history';

    try {
      final response = await http
          .get(Uri.parse('$apiUrl?dateBegin=$dateBegin&dateEnd=$dateEnd'));

      if (response.statusCode == 200) {
        Map<String, dynamic> historyData = jsonDecode(response.body);
        return historyData;
      } else {
        print("Failed to fetch history. Status code: ${response.statusCode}");
        return {'error': 'Failed to fetch history'};
      }
    } catch (error) {
      print("Error: $error");
      return {'error': 'An error occurred'};
    }
  }
}
