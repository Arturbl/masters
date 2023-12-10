import 'dart:async';

import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:app/service/api.dart';
import 'package:http/http.dart' as http;

class Home extends StatefulWidget {
  const Home({Key? key}) : super(key: key);

  @override
  State<Home> createState() => _HomeState();
}

class _HomeState extends State<Home> {
  DateTime? _startDate;
  DateTime? _endDate;
  List<dynamic> fitnessData = [];
  bool isRecording = false;

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
    Timer.periodic(Duration(seconds: 2), (Timer timer) async {
      try {
        final response =
            await http.get(Uri.parse('http://localhost:8081/health'));

        if (response.statusCode == 200) {
          print('Health check response: ${response.body}');
        } else {
          print(
              'Failed to fetch health data. Status code: ${response.statusCode}');
        }
      } catch (e) {
        print('Error during HTTP request: $e');
      }
    });
  }
}
