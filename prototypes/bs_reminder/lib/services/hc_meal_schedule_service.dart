import 'package:bs_reminder/models/meal_reminders.dart';

// hard-coded meal schedule to start
const List<MealReminder> hardcodedMealReminders = [
  MealReminder(
    meal: MealType.breakfast,
    hour: 10,
    minute: 59,
    enabled: true,
  ),
  MealReminder(
    meal: MealType.lunch,
    hour: 10,
    minute: 58,
    enabled: true,
  ),
  MealReminder(
    meal: MealType.dinner,
    hour: 10,
    minute: 57,
    enabled: true,
  ),
];
