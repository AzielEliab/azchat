import 'package:flutter/material.dart';

import 'theme.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const AzChatApp());
}

const String limitation =
    'AZChat mints spendable handles, opens ephemeral rooms, and carries '
    'an agent bus. Mesh hop default off. Not SMTP. Not AZMail. '
    'Do not bridge. Stranger room_pull is 404. Author: Aziel Eliab.';

class AzChatApp extends StatelessWidget {
  const AzChatApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AZChat',
      debugShowCheckedModeBanner: false,
      theme: buildAppTheme(),
      home: const WorkspacePage(),
    );
  }
}

class WorkspacePage extends StatefulWidget {
  const WorkspacePage({super.key});

  @override
  State<WorkspacePage> createState() => _WorkspacePageState();
}

class _WorkspacePageState extends State<WorkspacePage> {
  final _labelA = TextEditingController(text: 'agent-a');
  final _labelB = TextEditingController(text: 'agent-b');
  final _text = TextEditingController(text: 'handles spend');
  String _status = 'Offline scaffold. Mint conceptually — mesh stays off.';
  int _handles = 0;
  int _rooms = 0;

  @override
  void dispose() {
    _labelA.dispose();
    _labelB.dispose();
    _text.dispose();
    super.dispose();
  }

  void _mint() {
    setState(() {
      _handles += 1;
      _status = 'Handle ${_labelA.text.isEmpty ? "agent" : _labelA.text} minted locally. Token is spendable.';
    });
  }

  void _openRoom() {
    if (_handles < 2) {
      setState(() => _status = 'Need two live handles. Stranger room_pull is 404.');
      return;
    }
    setState(() {
      _rooms += 1;
      _status = 'Room opened. TTL sealed. Mesh stays off. ${_text.text}';
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('AZChat')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Text(
            'Handles spend. Rooms seal. Mesh stays off.',
            style: Theme.of(context).textTheme.titleMedium?.copyWith(
                  color: kGold,
                  fontStyle: FontStyle.italic,
                ),
          ),
          const SizedBox(height: 8),
          const Text(limitation),
          const SizedBox(height: 16),
          TextField(controller: _labelA, decoration: const InputDecoration(labelText: 'Handle A label')),
          const SizedBox(height: 12),
          TextField(controller: _labelB, decoration: const InputDecoration(labelText: 'Handle B label')),
          const SizedBox(height: 12),
          TextField(controller: _text, maxLines: 3, decoration: const InputDecoration(labelText: 'Room / bus text')),
          const SizedBox(height: 16),
          FilledButton(onPressed: _mint, child: const Text('New handle')),
          const SizedBox(height: 8),
          OutlinedButton(onPressed: _openRoom, child: const Text('Open room')),
          const SizedBox(height: 16),
          Text('Handles $_handles · Rooms $_rooms', style: const TextStyle(color: kGold)),
          const SizedBox(height: 8),
          Text(_status),
          const SizedBox(height: 12),
          const Text(limitation, style: TextStyle(fontSize: 12)),
        ],
      ),
    );
  }
}
