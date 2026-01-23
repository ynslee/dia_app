import 'package:image_picker/image_picker.dart';
import 'dart:io';
import 'package:path_provider/path_provider.dart';

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

    // print('Photo path: ${photo.path}'); // debug printing for now
    final savedImage = _savePhoto(photo.path);
    return savedImage;
  }

  static Future<File?> _savePhoto(String photoPath) async {
    final Directory appDir = await getApplicationDocumentsDirectory();
    final String fileName = 'meal_${DateTime.now().millisecondsSinceEpoch}.jpg';

    final File savedImage = await File(photoPath).copy('${appDir.path}/$fileName');
    print('Saved image: ${savedImage.path}'); //debug print
    return savedImage;
  }
}

