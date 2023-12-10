import 'dart:async';
import 'dart:convert';
import 'dart:math';

import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:app/service/api.dart';
import 'package:http/http.dart' as http;

class Home extends StatefulWidget {
  final String username;
  const Home({Key? key, required this.username}) : super(key: key);

  @override
  State<Home> createState() => _HomeState();
}

class _HomeState extends State<Home> {
  DateTime? _startDate;
  DateTime? _endDate;
  List<dynamic> fitnessData = [];
  bool isRecording = false;
  DateTime? walkingStartTime;
  Duration totalWalkingTime = Duration.zero;
  double totalDistance = 0.0;
  double totalSpeed = 0.0;

  @override
  void initState() {
    super.initState();
    fetchDataForTimeFrame("2023-07-01", "2023-07-01");
  }

  Future<void> fetchDataForTimeFrame(String startDate, String endDate) async {
    try {
      Auth.getHistory(startDate, endDate)
          .then((result) => {setData(result['result'])});
    } catch (error) {
      // Handle errors
      print("Error fetching history: $error");
    }
  }

  void setData(List<dynamic> result) {
    print("result: ${result}");
    setState(() {
      fitnessData = result;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        automaticallyImplyLeading: false,
        title: const Text('Fitness Tracker'),
        actions: [
          IconButton(
            onPressed: () {
              // Add your logout logic here
              // Navigator.pushReplacementNamed(context, '/login');
            },
            icon: Icon(Icons.logout),
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Select Date Range:',
              style: TextStyle(
                fontSize: 20.0,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 16.0),
            Row(
              children: [
                ElevatedButton(
                  onPressed: () => _selectDate(context, true),
                  style: ElevatedButton.styleFrom(
                    primary: Colors.blue,
                    onPrimary: Colors.white,
                  ),
                  child: Text(
                    _startDate != null
                        ? 'Start Date: ${DateFormat('yyyy-MM-dd').format(_startDate!)}'
                        : 'Select Start Date',
                    style: TextStyle(fontSize: 16.0),
                  ),
                ),
                const SizedBox(width: 16.0),
                ElevatedButton(
                  onPressed: () => _selectDate(context, false),
                  style: ElevatedButton.styleFrom(
                    primary: Colors.blue,
                    onPrimary: Colors.white,
                  ),
                  child: Text(
                    _endDate != null
                        ? 'End Date: ${DateFormat('yyyy-MM-dd').format(_endDate!)}'
                        : 'Select End Date',
                    style: TextStyle(fontSize: 16.0),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16.0),
            if (!isRecording)
              Expanded(
                child: _buildDataTable(),
              ),
            if (walkingStartTime != null)
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Walking Details:',
                      style: TextStyle(
                        fontSize: 20.0,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 8.0),
                    Text(
                      'Start Time: ${DateFormat('yyyy-MM-dd HH:mm:ss').format(walkingStartTime!)}',
                      style: TextStyle(fontSize: 16.0),
                    ),
                    const SizedBox(height: 8.0),
                    Text(
                      'Total Time: ${formatDuration(totalWalkingTime)}',
                      style: TextStyle(fontSize: 16.0),
                    ),
                    const SizedBox(height: 8.0),
                    Text(
                      'Total Distance: ${totalDistance.toStringAsFixed(2)} meters',
                      style: TextStyle(fontSize: 16.0),
                    ),
                    const SizedBox(height: 8.0),
                    Text(
                      'Total Speed: ${totalSpeed.toStringAsFixed(2)} m/s',
                      style: TextStyle(fontSize: 16.0),
                    ),
                  ],
                ),
              ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          setState(() {
            isRecording = !isRecording;
            if (isRecording) {
              _startHttpRequest();
            } else {
              // Stop the HTTP request (if needed)
            }
          });
        },
        child: Icon(isRecording ? Icons.stop : Icons.play_arrow),
      ),
    );
  }

  Widget _buildDataTable() {
    return DataTable(
      columns: [
        DataColumn(label: Text('day')),
        DataColumn(label: Text('Calories Walking')),
        DataColumn(label: Text('Calories Running')),
        DataColumn(label: Text('Running Time')),
        DataColumn(label: Text('Walking Time'))
      ],
      rows: fitnessData.map((data) {
        return DataRow(
          cells: [
            DataCell(Text(data['day'])),
            DataCell(Text(data['calories_walking'].toString())),
            DataCell(Text(data['calories_running'].toString())),
            DataCell(Text(data['running'].toString())),
            DataCell(Text(data['walking'].toString()))
          ],
        );
      }).toList(),
    );
  }

  Future<void> _selectDate(BuildContext context, bool isStartDate) async {
    final DateTime? pickedDate = await showDatePicker(
      context: context,
      initialDate: DateTime.now(),
      firstDate: DateTime(1900),
      lastDate: DateTime.now(),
    );

    if (pickedDate != null) {
      setState(() {
        if (isStartDate) {
          _startDate = pickedDate;
        } else {
          _endDate = pickedDate;
        }
      });
      // Update your timeframe and reload data here
      // fetchDataForTimeFrame(_startDate, _endDate);
    }
  }

  void _startHttpRequest() {
    Timer.periodic(Duration(seconds: 1), (Timer timer) async {
      if (isRecording) {
        try {
          final uri = Uri.parse('http://localhost:8081/history-real-time')
              .replace(queryParameters: {'username': widget.username});

          final response = await http.get(uri);

          if (response.statusCode == 200) {
            processData(json.decode(response.body));
          } else {
            print(
                'Failed to fetch health data. Status code: ${response.statusCode}');
          }
        } catch (e) {
          print('Error during HTTP request: $e');
        }
      }
    });
  }

  void processData(Map<String, dynamic> data) {
    int activity = data["last_row"][0][1];
    final timestampString = data["last_row"][0][8];

    final timestamp =
        DateFormat('EEE, dd MMM yyyy HH:mm:ss').parse(timestampString);

    if (activity == 0) {
      if (walkingStartTime == null) {
        walkingStartTime = timestamp;
      }

      final deltaTime = DateTime.now().difference(walkingStartTime!);

      final accelerationX = data["last_row"][0][2] as double;
      final accelerationY = data["last_row"][0][3] as double;
      final accelerationZ = data["last_row"][0][4] as double;
      final speed = data["speed"];

      totalDistance += speed * deltaTime.inSeconds;
      totalSpeed = speed;

      totalWalkingTime = deltaTime;
      setState(() {});
    }
  }

  double calculateSpeed(
      double accelerationX, double accelerationY, double accelerationZ) {
    return sqrt(accelerationX * accelerationX +
        accelerationY * accelerationY +
        accelerationZ * accelerationZ);
  }

  String formatDuration(Duration duration) {
    String twoDigits(int n) => n.toString().padLeft(2, '0');
    String twoDigitMinutes = twoDigits(duration.inMinutes.remainder(60));
    String twoDigitSeconds = twoDigits(duration.inSeconds.remainder(60));
    return '$twoDigitMinutes:$twoDigitSeconds';
  }
}
