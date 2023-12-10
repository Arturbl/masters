import 'dart:async';
import 'dart:convert';
import 'dart:math';
import 'package:app/service/api.dart';
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
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
  String _noActivityMessage = '';
  String dateRangeText = 'Select a date range';

  void fetchDataForTimeFrame(String startDate, String endDate) {
    try {
      final client = http.Client();
      Auth.getHistory(startDate, endDate).then((result) {
        setData(result['result']);
        client.close();
      });
    } catch (error) {
      print("Error fetching history: $error");
    }
  }

  void setData(List<dynamic> result) {
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
              Navigator.pushReplacementNamed(context, '/login');
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
            ElevatedButton(
              onPressed: () {
                if (_startDate != null && _endDate != null) {
                  final startDateString =
                      DateFormat('yyyy-MM-dd').format(_startDate!);
                  final endDateString =
                      DateFormat('yyyy-MM-dd').format(_endDate!);
                  fetchDataForTimeFrame(startDateString, endDateString);
                  setState(() {
                    dateRangeText =
                        'Selected Date Range: $startDateString - $endDateString';
                  });
                } else {
                  // Handle case where dates are not selected
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      content: Text('Please select start and end dates.'),
                    ),
                  );
                }
              },
              style: ElevatedButton.styleFrom(
                primary: Colors.green,
                onPrimary: Colors.white,
              ),
              child: Text('Submit'),
            ),
            const SizedBox(height: 16.0),
            Text(
              dateRangeText,
              style: TextStyle(
                fontSize: 18.0,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 16.0),
            if (!isRecording)
              Expanded(
                child: _buildDataTable(),
              ),
            if (isRecording && walkingStartTime != null)
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
            Text(
              _noActivityMessage,
              style: TextStyle(fontSize: 16.0, color: Colors.red),
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
    return fitnessData.isNotEmpty
        ? SingleChildScrollView(
            child: DataTable(
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
            ),
          )
        : Container();
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
            if (json.decode(response.body)['last_row'].isNotEmpty) {
              processData(json.decode(response.body));
              setState(() {
                _noActivityMessage = '';
              });
            } else {
              setState(() {
                _noActivityMessage = 'No activities are currently occurring.';
              });
            }
          } else {
            setState(() {
              _noActivityMessage = 'Could not load data.';
            });
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

      totalDistance += speed;
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
