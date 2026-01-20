import 'package:bs_reminder/models/meal_reminders.dart';

// hard-coded meal schedule to start
const List<MealReminder> hardcodedMealReminders = [
  MealReminder(
    meal: MealType.breakfast,
    hour: 11,
    minute: 40,
    enabled: true,
  ),
  MealReminder(
    meal: MealType.lunch,
    hour: 11,
    minute: 45,
    enabled: true,
  ),
  MealReminder(
    meal: MealType.dinner,
    hour: 11,
    minute: 50,
    enabled: true,
  ),
];
