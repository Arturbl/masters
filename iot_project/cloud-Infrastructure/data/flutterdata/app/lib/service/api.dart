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
    final apiUrl = 'http://172.100.10.19:8081/register';

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

  static Future<String> signIn(String email, String password) async {
    // Implement sign-in logic here, if needed
    return "done";
  }
}
