import 'dart:convert';
import 'dart:io';

void main() async {
  var process = await Process.start("venv/bin/python3", ["app/main.py"],
      mode: ProcessStartMode.inheritStdio);
  // var process = await Process.start("ls", ["-lh"]);
  print('process launched');
  // process.stdout.listen((event) {
  //   print(utf8.decode(event));
  // });
  // stdout.addStream(process.stdout);
}
