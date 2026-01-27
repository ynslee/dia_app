import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'notification_router_service.dart';

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
    // add setting for handling responses to notification actions
   await notifications.initialize(
     settings,
     onDidReceiveNotificationResponse: _onNotificationResponse,
   );

   // Request notification permission on Android 13+
   //this is the part that make the pop-up happen on your phone to grant access
   final androidImplementation =
   notifications.resolvePlatformSpecificImplementation<AndroidFlutterLocalNotificationsPlugin>();

   if (androidImplementation != null) {
     // this allowed the notifications on button press to work
     final grantedGeneral = await androidImplementation.requestNotificationsPermission();
     // adding this permissions request allowed the timed notifications to work
     final grantedExact = await androidImplementation.requestExactAlarmsPermission();
   }
 }

 // pass to intialization of notification service
 // check action id of response
 void _onNotificationResponse(NotificationResponse response) {
   if (response.actionId == "TAKE_PHOTO") {
     //router to broadcast the take photo action
     NotificationRouterService.handleTakePhoto();
   }
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
