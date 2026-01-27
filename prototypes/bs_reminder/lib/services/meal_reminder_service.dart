import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:timezone/timezone.dart' as tz;

import 'package:bs_reminder/models/meal_reminders.dart';
import 'package:bs_reminder/services/notification_service.dart';

// want stable ids for each meal type, that way we can edit them in the future
class MealReminderScheduler {
  static int _notificationId(MealType meal) {
    switch (meal) {
      case MealType.breakfast:
        return 100;
      case MealType.lunch:
        return 101;
      case MealType.dinner:
        return 102;
    }
  }

  // set title of reminder
  static String _title(MealType meal) {
    switch (meal) {
      case MealType.breakfast:
        return 'Breakfast Reminder';
      case MealType.lunch:
        return 'Lunch Reminder';
      case MealType.dinner:
        return 'Dinner Reminder';
    }
  }

  // give the next date and time for the reminder to fire based on the
  // requested hour and minute
  // static = class func
  static tz.TZDateTime _nextInstance(int hour, int minute) {
    final now = tz.TZDateTime.now(tz.local);

    var scheduled =
    tz.TZDateTime(tz.local, now.year, now.month, now.day, hour, minute);
    // is today's reminder still to come or has the time passed and need to
    // be tomorrow?
    if (scheduled.isBefore(now)) {
      scheduled = scheduled.add(const Duration(days: 1));
    }
    //debug print statement
    print("Scheduled time: $scheduled");
    return scheduled;
  }

  // schedules one repeating meal reminder e.g. for dinner
  static Future<void> schedule(MealReminder reminder) async {
    if (!reminder.enabled) return;

    await notifications.zonedSchedule(
      _notificationId(reminder.meal),
      _title(reminder.meal),
      'Tap to take a photo of your meal',
      _nextInstance(reminder.hour, reminder.minute),
      const NotificationDetails( //set up channel
        android: AndroidNotificationDetails(
          'meal_reminders',
          'Meal Reminders',
          importance: Importance.max,
          priority: Priority.high,
          actions: <AndroidNotificationAction>[ //adds action to notification
            AndroidNotificationAction(
              'TAKE_PHOTO',
              'Take meal photo',
              showsUserInterface: true,
            )
          ]
        ),
      ),
      androidScheduleMode: AndroidScheduleMode.inexact, // does it need exact while idle? had to add extra permission in android manifest
      matchDateTimeComponents: DateTimeComponents.time, // makes repeat daily by matching on ly time
      payload: reminder.meal.name,
    );
  }
// id is used to control the notification.
// give at creation and then again at cancellation
// nothing bad happens by cancelling something that doesn't exist
  static Future<void> cancel(MealType meal) async {
    await notifications.cancel(_notificationId(meal));
  }
}


