import 'dart:io';

import 'package:bs_reminder/services/notification_service.dart'; // local file
import 'package:bs_reminder/services/photo_storage_service.dart';
import 'package:flutter/material.dart';//standard material design import
import 'package:flutter_local_notifications/flutter_local_notifications.dart';//for notifications
import 'package:timezone/timezone.dart' as tz; //timezone package
import 'package:timezone/data/latest.dart' as tzdata;// database initialization
import 'package:flutter_timezone/flutter_timezone.dart';//to get device timezone
import 'services/hc_meal_schedule_service.dart';//replace with actual
import 'services/meal_reminder_service.dart';//local file
import 'package:bs_reminder/widgets/photo_button_widget.dart';



void main() async {
  // makes sure connected to underlying platform i.e. Android
  // should call before inti platform related stuff like notifications
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize timezone
  tzdata.initializeTimeZones();

  // the notification init
  await initNotifications();
  // defensive rescheduling of notifications
  for (final reminder in hardcodedMealReminders) {
    await MealReminderScheduler.schedule(reminder);
    //debug print
    print("${reminder.meal} ${reminder.hour} : ${reminder.minute}");
  }

  // test of scheduled notification
  await notifications.zonedSchedule(
    103,
    'Test Reminder',
    'Tap to take a photo!',
    tz.TZDateTime.now(tz.local).add(const Duration(minutes: 1)), // 1 min from now
    const NotificationDetails(
      android: AndroidNotificationDetails(
        'meal_reminders',
        'Meal Reminders',
        importance: Importance.max,
        priority: Priority.high,
      ),
    ),
    androidScheduleMode: AndroidScheduleMode.exact,
    matchDateTimeComponents: DateTimeComponents.time,
    payload: 'breakfast',
  );
  //end test

  // standard runApp() call
  runApp(const MyApp());
}



// DEFAULT PROJECT FROM CREATION
class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        // This is the theme of your application.
        //
        // TRY THIS: Try running your application with "flutter run". You'll see
        // the application has a purple toolbar. Then, without quitting the app,
        // try changing the seedColor in the colorScheme below to Colors.green
        // and then invoke "hot reload" (save your changes or press the "hot
        // reload" button in a Flutter-supported IDE, or press "r" if you used
        // the command line to start the app).
        //
        // Notice that the counter didn't reset back to zero; the application
        // state is not lost during the reload. To reset the state, use hot
        // restart instead.
        //
        // This works for code too, not just values: Most code changes can be
        // tested with just a hot reload.
        colorScheme: .fromSeed(seedColor: Colors.deepPurple),
      ),
      home: const MyHomePage(title: 'Flutter Demo Home Page'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  List<File> _photos = []; //cant be final the way the init state is done

  void _onPhotoPicked(File? file) async {
    if (file == null) return;

    setState(() {
      _photos.insert(0, file); // insert at beginning
    });
    await PhotoStorageService.savePhotos(_photos); //saving all everytime? can we just append?
  }

  @override
  void initState() {
    super.initState();

    _loadPhotos();
  }

  Future<void> _loadPhotos() async {
    final photos = await PhotoStorageService.loadPhotos();
    setState(() {
      _photos = photos;
    });
  }

  @override
  Widget build(BuildContext context) {
    // This method is rerun every time setState is called, for instance as done
    // by the _incrementCounter method above.
    //
    // The Flutter framework has been optimized to make rerunning build methods
    // fast, so that you can just rebuild anything that needs updating rather
    // than having to individually change instances of widgets.
    return Scaffold(
      appBar: AppBar(
        // TRY THIS: Try changing the color here to a specific color (to
        // Colors.amber, perhaps?) and trigger a hot reload to see the AppBar
        // change color while the other colors stay the same.
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        // Here we take the value from the MyHomePage object that was created by
        // the App.build method, and use it to set our appbar title.
        title: Text(widget.title),
      ),
      body: Center(
        // Center is a layout widget. It takes a single child and positions it
        // in the middle of the parent.
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // testing out photo picking button
            PhotoButton(onPhotoPicked: (file) {
              if (file != null) {
                print('Photo picked: ${file.path}');//debug print
                _onPhotoPicked(file);//home page state setting func
              } else {
                print('No photo selected');//debug print
              }
            }
            ),
            Expanded(
                child: ListView.builder(
                  itemCount: _photos.length,
                    itemBuilder: (context, index) {
                      return Padding(
                        padding: const EdgeInsets.all(8),
                        child: Image.file(
                          _photos[index],
                          height: 200,
                          fit: BoxFit.cover,
                        ),
                      );
                    },
                ),
            )
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        backgroundColor: Colors.red,
        foregroundColor: Colors.blue,
        onPressed: () async { //setup as a lambda as it wants a callback
          await showPhotoReminder();
        },
        tooltip: 'sent notice',
        child: const Icon(Icons.add_a_photo),
      ),
    );
  }
}
