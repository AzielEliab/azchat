import 'package:flutter/material.dart';

import 'theme.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const AzChatApp());
}

const String limitation =
    'AZChat mints spendable handles, opens ephemeral rooms, and carries '
    'an agent bus. Mesh hop default off. Not SMTP. Not AZMail. '
    'Do not bridge. Stranger room_pull is 404. Hosted rooms appear on the '
    'all-rooms list. A private room requires a passphrase to join and is '
    'not end-to-end encryption. Author: Aziel Eliab.';

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
  final _title = TextEditingController(text: 'hall');
  final _passphrase = TextEditingController();
  bool _private = false;
  String _status = 'Offline scaffold. Live list, host, and passphrase join run on the Worker and azchat ui. Mesh stays off.';
  int _handles = 0;
  int _rooms = 0;

  @override
  void dispose() {
    _labelA.dispose();
    _labelB.dispose();
    _text.dispose();
    _title.dispose();
    _passphrase.dispose();
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
      _status = 'Pairwise room counted locally. It is not on the all-rooms list. Mesh stays off.';
    });
  }

  void _hostRoom() {
    if (_handles < 1) {
      setState(() => _status = 'Mint a handle before hosting. This scaffold does not open a live room.');
      return;
    }
    if (_private && _passphrase.text.trim().isEmpty) {
      setState(() => _status = 'Private needs a passphrase. No room was counted. This scaffold does not check a passphrase.');
      return;
    }
    setState(() {
      _rooms += 1;
      _passphrase.clear();
      _status = _private
          ? 'Scaffold only. A live private room would require the passphrase to join and would not put that passphrase on the list. Not end-to-end encryption.'
          : 'Scaffold only. A live hosted room would appear on the all-rooms list. Not end-to-end encryption.';
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
          TextField(controller: _title, decoration: const InputDecoration(labelText: 'Room title')),
          const SizedBox(height: 12),
          TextField(
            controller: _passphrase,
            obscureText: true,
            decoration: const InputDecoration(labelText: 'Passphrase (private rooms only)'),
          ),
          SwitchListTile(
            contentPadding: EdgeInsets.zero,
            title: const Text('Private room — passphrase required to join'),
            subtitle: const Text('Not end-to-end encryption. Lamb Lens Service → Clarity → Peace.'),
            value: _private,
            onChanged: (value) => setState(() => _private = value),
          ),
          TextField(controller: _text, maxLines: 3, decoration: const InputDecoration(labelText: 'Room / bus text')),
          const SizedBox(height: 16),
          FilledButton(onPressed: _mint, child: const Text('New handle')),
          const SizedBox(height: 8),
          OutlinedButton(onPressed: _openRoom, child: const Text('Open room')),
          const SizedBox(height: 8),
          FilledButton(onPressed: _hostRoom, child: const Text('Host room')),
          const SizedBox(height: 8),
          const Text('All rooms: this scaffold has no live directory. Use the Worker or azchat ui to join from the list.'),
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
