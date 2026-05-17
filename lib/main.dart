import 'package:flutter/material';
import 'package:chaquopy/chaquopy.dart';
import 'package:code_text_field/code_text_field.dart';
import 'package:highlight/languages/python.dart';
import 'package:flutter_highlight/themes/monokai-sublime.dart';

void main() {
  runApp(const PyroidFlutterApp());
}

class PyroidFlutterApp extends StatelessWidget {
  const PyroidFlutterApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      theme: ThemeData.dark(useMaterial3: true).copyWith(
        primaryColor: Colors.orange,
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.orange, brightness: Brightness.dark),
      ),
      home: const HomeScreen(),
    );
  }
}

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  late CodeController _codeController;
  String _terminalOutput = "Program çalıştırılmaya hazır...\n";
  String _currentScreen = "Editör";

  @override
  void initState() {
    super.initState();
    // Renkli Python kod editörü ayarı
    _codeController = CodeController(
      text: "import cv2\nimport numpy as np\n\nprint('Flutter Python Ortamı Hazır!')\nprint('OpenCV Sürümü:', cv2.__version__)",
      language: python,
    );
  }

  // Python kodunu çalıştıran fonksiyon
  void _runPython() async {
    setState(() { _terminalOutput = "Kod çalıştırılıyor...\n"; });
    
    // Chaquopy ile kodu arka planda infaz ediyoruz
    final result = await Chaquopy.executeCode(_codeController.text);
    
    setState(() {
      if (result['textOutput'] != null && result['textOutput'].toString().isNotEmpty) {
        _terminalOutput = result['textOutput'];
      } else if (result['error'] != null) {
        _terminalOutput = "[HATA]\n${result['error']}";
      } else {
        _terminalOutput = "Kod çalıştı ama çıktı üretmedi.";
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(_currentScreen == "Editör" ? "Pyroid Flutter Pro" : "PIP Paketleri"),
        actions: [
          if (_currentScreen == "Editör")
            IconButton(
              icon: const Icon(Icons.play_arrow, color: Colors.green, size: 30),
              onPressed: _runPython,
            ),
        ],
      ),
      // YAN MENÜ (Drawer)
      drawer: Drawer(
        child: ListView(
          padding: EdgeInsets.zero,
          children: [
            const DrawerHeader(
              decoration: BoxDecoration(color: Colors.orange),
              child: Text('Pyroid Ultra (Flutter)', style: TextStyle(fontSize: 24, color: Colors.black, fontWeight: FontWeight.bold)),
            ),
            ListTile(
              leading: const Icon(Icons.code),
              title: const Text('Kod Editörü'),
              onTap: () { setState(() { _currentScreen = "Editör"; }); Navigator.pop(context); },
            ),
            ListTile(
              leading: const Icon(Icons.box),
              title: const Text('PIP Paketleri'),
              onTap: () { setState(() { _currentScreen = "PIP"; }); Navigator.pop(context); },
            ),
          ],
        ),
      ),
      body: _currentScreen == "Editör" 
        ? Column(
            children: [
              // 1. Kod Editörü Alanı
              Expanded(
                flex: 6,
                child: Container(
                  color: const Color(0xFF232323),
                  child: CodeField(
                    controller: _codeController,
                    textStyle: const TextStyle(fontFamily: 'monospace', fontSize: 16),
                  ),
                ),
              ),
              const Divider(height: 2, color: Colors.orange),
              // 2. Terminal Alanı
              Expanded(
                flex: 4,
                child: Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(10),
                  color: Colors.black,
                  child: SingleChildScrollView(
                    child: Text(
                      _terminalOutput,
                      style: const TextStyle(color: Colors.lightGreenAccent, fontFamily: 'monospace', fontSize: 14),
                    ),
                  ),
                ),
              ),
            ],
          )
        : Center(
            child: Text("PIP Paket Yöneticisi çok yakında burada!", style: TextStyle(fontSize: 18, color: Colors.grey[400])),
          ),
    );
  }
}

