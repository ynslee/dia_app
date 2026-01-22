import 'package:bs_reminder/services/photo_service.dart';
import 'package:flutter/material.dart';
import 'dart:io';

// take photo button

class PhotoButton extends StatelessWidget {
  final ValueChanged<File?> onPhotoPicked; //callback? button doesn't return a file but calls to a function when <T> is available?
  final String label;
  final IconData icon;

  const PhotoButton({
    super.key,
    required this.onPhotoPicked,
    this.label = 'Add photo',
    this.icon = Icons.add_a_photo,
  });

  @override
  Widget build(BuildContext context) {
    return ElevatedButton.icon(
      icon: Icon(icon),
      label: Text(label),
      onPressed: () async {
        final PhotoSource? photoSource = await _showSourceChooser(context);
        if (photoSource == null) return;
        final File? photoFile = await PhotoService.pickPhoto(photoSource);
        if (photoFile == null) return;
        onPhotoPicked(photoFile);
      },
    );
  }

  Future<PhotoSource?> _showSourceChooser(BuildContext context) async {
    final PhotoSource? source = await showModalBottomSheet<PhotoSource>( //not sure if I want bottom sheet
      context: context,
      builder: (_) { //the _ ignores the build context
        return SafeArea( //prevents UI overlapping, should use bottom sheet
          child: Column(
            mainAxisSize: MainAxisSize.min, // only use space needed
            children: [
              ListTile(
                leading: const Icon(Icons.camera_alt),
                title: const Text('Take photo'),
                onTap: () => Navigator.pop(context, PhotoSource.camera), // closes bottom sheet, second val is return arg
              ),
              ListTile(
                leading: const Icon(Icons.photo_library),
                title: const Text('Choose from gallery'),
                onTap: () => Navigator.pop(context, PhotoSource.gallery),
              ),
            ],
          ),
        );
      },
    );

    if (source == null) return null;

    return source;
  }
}

