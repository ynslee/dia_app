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

 // setup channel details for android notification setup
 const AndroidNotificationDetails androidDetails =
 AndroidNotificationDetails(
   'photo_channel', //channel ID - unique to our app, groups notification types
   'Photo Reminders', // ChannelName - this is shown to user in Notifications settings in phone
   importance: Importance.max, //causes sound and pop up, TODO: choose notice type
   priority: Priority.high //backwards compatibility option for older Android TODO: choose priority
 );

// test to show notification right away
// tie it to a button in app to test
Future<void> showPhotoReminder() async {
  await notifications.show(
    0, // notification ID, needs to be unique
    'Photo Reminder', // title on the notification card
    'Tap to take a picture', // text for notification card
    const NotificationDetails(
        android: androidDetails), // load details for notice channel
  );
}
