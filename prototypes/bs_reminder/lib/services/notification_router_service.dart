import 'dart:async';
import 'dart:io';

// creates broadcast of string that home page can subscribe to and
// take actions based on the string that is broadcast
// called by the notification action method for the notification service
class NotificationRouterService {
  static final _controller = StreamController<String>.broadcast();

  static Stream<String> get stream => _controller.stream;

  static void handleTakePhoto() {
    _controller.add('TAKE_PHOTO');
  }
}