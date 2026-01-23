import 'dart:io';
import 'dart:convert';
import 'package:path_provider/path_provider.dart';

class PhotoStorageService {
  static const String _filename = 'photos.json';

  static Future<File> _getStorageFile() async {
    final dir = await getApplicationDocumentsDirectory();
    return File('${dir.path}/$_filename');
  }

  static Future<List<File>> loadPhotos() async {
    try {
      final file = await _getStorageFile();
      if (!await file.exists()) return [];

      final contents = await file.readAsString();
      final List<dynamic> paths = jsonDecode(contents);

      return paths
          .map((path)=> File(path as String))
          .where((file) => file.existsSync())
          .toList();
    } catch (_) {
      return []; //return empty list if there is error for now
    }
  }

  static Future<void> savePhotos(List<File> photos) async {
    final file = await _getStorageFile();
    final paths = photos.map((f) => f.path).toList();

    await file.writeAsString(jsonEncode(paths));
  }

  static Future<void> deletePhoto(File photo, List<File> photoList) async {
    try {
      if (await photo.exists()) {
        await photo.delete();
      }
    } catch (_) {
      //add error behavior later
    }
    await savePhotos(photoList);
  }
}