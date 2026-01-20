
// add more for snacks or other?
enum MealType {
  breakfast,
  lunch,
  dinner,
}

class MealReminder {
  final MealType meal;
  final int hour;
  final int minute;
  final bool enabled;

  const MealReminder({
    required this.meal,
    required this.hour,
    required this.minute,
    required this.enabled,
  });
}
