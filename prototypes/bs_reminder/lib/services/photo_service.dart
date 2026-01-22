import 'package:image_picker/image_picker.dart';
import 'dart:io';

enum  PhotoSource {
  camera,
  gallery
}

class PhotoService {
  static final ImagePicker _picker = ImagePicker();

  /// Opens camera and returns the taken photo file (or null if cancelled)
  static Future<File?> pickPhoto(PhotoSource source) async {
    //set the source to camera or gallery based on param
    final ImageSource imageSource = source == PhotoSource.camera ? ImageSource.camera : ImageSource.gallery;
    // question mark after means it is null if user cancels
    final XFile? photo = await _picker.pickImage(
      source: imageSource,
      preferredCameraDevice: CameraDevice.rear,
      imageQuality: 90, // 0–100
    );

    if (photo == null) return null; //stop if the process was cancelled

    print('Photo path: ${photo.path}'); // debug printing for now
    return File(photo.path);
  } //convert Xfile to file

}

