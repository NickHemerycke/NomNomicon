import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Meal Planner',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: MealMenuScreen(),
    );
  }
}

class MealMenuScreen extends StatefulWidget {
  const MealMenuScreen({super.key});

  @override
  _MealMenuScreenState createState() => _MealMenuScreenState();
}

class _MealMenuScreenState extends State<MealMenuScreen> {
  final List<String> _menuItems = []; // The list that stores menu items.

  // Method to add a dish to the menu.
  void _addDish() {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text('Add a Dish'),
          content: TextField(
            onSubmitted: (value) {
              setState(() {
                _menuItems.add(value);
              });
              Navigator.of(context).pop();
            },
            autofocus: true,
            decoration: InputDecoration(
              labelText: 'Dish Name',
            ),
          ),
        );
      },
    );
  }

  // Method to remove a dish from the menu.
  void _removeDish(int index) {
    setState(() {
      _menuItems.removeAt(index);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Meal Planner'),
        actions: [
          IconButton(
            icon: Icon(Icons.add),
            onPressed: _addDish, // Add dish
          ),
        ],
      ),
      body: _menuItems.isEmpty
          ? Center(child: Text('No dishes added yet!'))
          : ListView.builder(
              itemCount: _menuItems.length,
              itemBuilder: (context, index) {
                return Dismissible(
                  key: Key(_menuItems[index]),
                  direction: DismissDirection.endToStart,
                  onDismissed: (direction) {
                    // Remove item on swipe.
                    _removeDish(index);
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(content: Text('Dish removed')),
                    );
                  },
                  background: Container(
                    color: Colors.red,
                    child: Align(
                      alignment: Alignment.centerRight,
                      child: Padding(
                        padding: const EdgeInsets.all(16.0),
                        child: Icon(Icons.delete, color: Colors.white),
                      ),
                    ),
                  ),
                  child: ListTile(
                    title: Text(_menuItems[index]),
                  ),
                );
              },
            ),
    );
  }
}
