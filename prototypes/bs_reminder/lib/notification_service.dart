import 'package:flutter_local_notifications/flutter_local_notifications.dart';

// create global notifications controller
final FlutterLocalNotificationsPlugin notifications =
FlutterLocalNotificationsPlugin();

//intialize notification system. call in main with app startup before runApp()
 Future<void> initNotifications() async {
   // type is from the plugin
   const AndroidInitializationSettings androidSettings =
   AndroidInitializationSettings('@mipmap/ic_launcher');
   // arg is the icon to show. we can change this later
   // this is the default location: android/app/src/main/res/mipmap

   // cross-platform settings initialization (just android for now)
   // pass in var from above as the android arg
   const InitializationSettings settings =
   InitializationSettings(android: androidSettings);

   // this is the global declared at top of file
   // initialize the settings made here to it
   await notifications.initialize(settings);
 }