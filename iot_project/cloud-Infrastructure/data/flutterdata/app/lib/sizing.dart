import 'package:flutter/cupertino.dart';
import 'package:responsive_builder/responsive_builder.dart';

class Sizing {
  static double fontSize = 16;

  static double getScreenWidth(BuildContext context) {
    final size = getDeviceType(MediaQuery.of(context).size);
    switch (size) {
      case DeviceScreenType.desktop:
        return MediaQuery.of(context).size.width * 0.50;
      case DeviceScreenType.tablet:
        return MediaQuery.of(context).size.width * 0.65;
      case DeviceScreenType.mobile:
        return MediaQuery.of(context).size.width * 0.85;
      default:
        return MediaQuery.of(context).size.width * 0.85;
    }
  }
}
