#!/usr/bin/env python3
"""
Enhanced WebSocket Server for Kn3aux-Code IDE
Real-time updates, notifications, and device monitoring
"""

from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_cors import CORS
import subprocess
import psutil
import threading
import time
import json
from datetime import datetime

app = Flask(__name__)
CORS(app, origins="*")
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading', logger=True, engineio_logger=True)

# Global state
device_stats = {
    'battery': 87,
    'cpu': 34,
    'memory': 61,
    'network': '5G',
    'ip': '192.168.1.42',
    'storage': 73,
    'temperature': 42,
    'uptime': '14h 32m'
}

connected_clients = []
notifications_queue = []
active_commands = {}

# ============== NOTIFICATION SYSTEM ==============
def add_notification(type, message, data=None):
    """Add notification to queue and broadcast"""
    notification = {
        'id': len(notifications_queue) + 1,
        'type': type,  # 'info', 'success', 'warning', 'error'
        'message': message,
        'data': data or {},
        'timestamp': datetime.now().isoformat()
    }
    notifications_queue.append(notification)
    # Keep only last 100 notifications
    if len(notifications_queue) > 100:
        notifications_queue.pop(0)
    
    # Broadcast to all clients
    socketio.emit('notification', notification)
    return notification

# ============== DEVICE STATS COLLECTOR ==============
def collect_stats():
    """Collect real-time device statistics"""
    global device_stats
    
    while True:
        try:
            # Battery (Android via ADB)
            try:
                battery_result = subprocess.run(
                    ['adb', 'shell', 'dumpsys', 'battery | grep level'],
                    shell=True, capture_output=True, text=True, timeout=3
                )
                if battery_result.returncode == 0:
                    battery_str = ''.join(battery_result.stdout.split())
                    if battery_str.isdigit():
                        device_stats['battery'] = int(battery_str)
            except:
                # Simulate battery drain
                device_stats['battery'] = max(10, device_stats['battery'] - 0.01)
            
            # CPU
            device_stats['cpu'] = psutil.cpu_percent(interval=0.5)
            
            # Memory
            device_stats['memory'] = psutil.virtual_memory().percent
            
            # Storage
            device_stats['storage'] = psutil.disk_usage('/').percent
            
            # Temperature (simulate)
            device_stats['temperature'] = 35 + (device_stats['cpu'] / 10)
            
            # Emit to all connected clients
            socketio.emit('device-stats', device_stats)
            
            # Check thresholds and send alerts
            if device_stats['battery'] < 20:
                add_notification('warning', f'Battery low: {device_stats["battery"]:.0f}%')
            if device_stats['cpu'] > 90:
                add_notification('warning', f'High CPU usage: {device_stats["cpu"]:.0f}%')
            if device_stats['memory'] > 90:
                add_notification('warning', f'High memory usage: {device_stats["memory"]:.0f}%')
            
            time.sleep(2)
        except Exception as e:
            print(f"Stats collection error: {e}")
            time.sleep(2)

# ============== WEBSOCKET EVENTS ==============
@socketio.on('connect')
def handle_connect():
    """Client connected"""
    client_id = request.sid
    connected_clients.append(client_id)
    
    # Send welcome notification
    emit('connected', {
        'client_id': client_id,
        'timestamp': datetime.now().isoformat(),
        'message': 'Connected to Kn3aux-Code WebSocket server'
    })
    
    # Send current stats
    emit('device-stats', device_stats)
    
    # Send queued notifications
    for notif in notifications_queue[-10:]:
        emit('notification', notif)
    
    # Broadcast to all
    broadcast_system_message(f'Client {client_id[:8]} connected')
    print(f'✓ Client connected: {client_id} (Total: {len(connected_clients)})')

@socketio.on('disconnect')
def handle_disconnect():
    """Client disconnected"""
    client_id = request.sid
    if client_id in connected_clients:
        connected_clients.remove(client_id)
    
    broadcast_system_message(f'Client {client_id[:8]} disconnected')
    print(f'✗ Client disconnected: {client_id} (Total: {len(connected_clients)})')

@socketio.on('run-command')
def handle_command(data):
    """Execute terminal command"""
    client_id = request.sid
    command = data.get('command', '')
    
    if not command:
        emit('command-result', {
            'success': False,
            'error': 'No command provided',
            'command': command
        })
        return
    
    # Add to active commands
    cmd_id = f"{client_id}_{int(time.time())}"
    active_commands[cmd_id] = {
        'command': command,
        'started': datetime.now().isoformat(),
        'status': 'running'
    }
    
    # Notify command started
    emit('command-started', {
        'cmd_id': cmd_id,
        'command': command,
        'timestamp': datetime.now().isoformat()
    })
    
    add_notification('info', f'Command started: {command[:50]}')
    
    # Execute command
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=60
        )
        
        active_commands[cmd_id]['status'] = 'completed'
        active_commands[cmd_id]['output'] = result.stdout
        active_commands[cmd_id]['error'] = result.stderr
        
        # Send result
        emit('command-result', {
            'cmd_id': cmd_id,
            'command': command,
            'success': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr,
            'returncode': result.returncode,
            'timestamp': datetime.now().isoformat()
        })
        
        # Notify completion
        if result.returncode == 0:
            add_notification('success', f'Command completed: {command[:50]}')
        else:
            add_notification('error', f'Command failed: {command[:50]}')
            
    except subprocess.TimeoutExpired:
        active_commands[cmd_id]['status'] = 'timeout'
        emit('command-result', {
            'cmd_id': cmd_id,
            'command': command,
            'success': False,
            'error': 'Command timed out (60s limit)',
            'timestamp': datetime.now().isoformat()
        })
        add_notification('error', f'Command timeout: {command[:50]}')
        
    except Exception as e:
        active_commands[cmd_id]['status'] = 'error'
        emit('command-result', {
            'cmd_id': cmd_id,
            'command': command,
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        })
        add_notification('error', f'Command error: {str(e)}')

@socketio.on('subscribe-room')
def handle_subscribe(data):
    """Subscribe to a room (e.g., device-specific updates)"""
    room = data.get('room')
    if room:
        join_room(room)
        emit('room-joined', {'room': room})

@socketio.on('unsubscribe-room')
def handle_unsubscribe(data):
    """Unsubscribe from a room"""
    room = data.get('room')
    if room:
        leave_room(room)
        emit('room-left', {'room': room})

@socketio.on('ping')
def handle_ping():
    """Heartbeat ping"""
    emit('pong', {
        'timestamp': datetime.now().isoformat(),
        'latency_ms': 0
    })

# ============== BROADCAST FUNCTIONS ==============
def broadcast_system_message(message):
    """Broadcast system message to all clients"""
    socketio.emit('system-message', {
        'message': message,
        'timestamp': datetime.now().isoformat()
    })

def broadcast_to_room(room, event, data):
    """Broadcast to specific room"""
    socketio.emit(event, data, room=room)

# ============== REST API ENDPOINTS ==============
@app.route('/api/ws/status')
def ws_status():
    """WebSocket server status"""
    return jsonify({
        'connected_clients': len(connected_clients),
        'active_commands': len([c for c in active_commands.values() if c['status'] == 'running']),
        'notifications_count': len(notifications_queue),
        'device_stats': device_stats,
        'uptime': device_stats['uptime'],
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/notifications')
def get_notifications():
    """Get recent notifications"""
    limit = request.args.get('limit', 20, type=int)
    return jsonify(notifications_queue[-limit:])

@app.route('/api/commands/active')
def get_active_commands():
    """Get active/running commands"""
    return jsonify({
        'active': [c for c in active_commands.values() if c['status'] == 'running'],
        'total': len(active_commands)
    })

@app.route('/api/broadcast', methods=['POST'])
def broadcast():
    """Broadcast custom message to all clients"""
    data = request.json
    message = data.get('message', '')
    event = data.get('event', 'custom-event')
    
    socketio.emit(event, {
        'message': message,
        'timestamp': datetime.now().isoformat()
    })
    
    return jsonify({'success': True, 'broadcasted': True})

# ============== START SERVER ==============
if __name__ == '__main__':
    print("╔══════════════════════════════════════════════════════════╗")
    print("║     KN3AUX-CODE Enhanced WebSocket Server                ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print("")
    print("📡 WebSocket: ws://localhost:5000/socket.io/")
    print("🌐 REST API: http://localhost:5000/api/ws/status")
    print("📊 Notifications: Real-time enabled")
    print("📈 Stats Collection: Active (2s interval)")
    print("")
    
    # Start stats collection thread
    stats_thread = threading.Thread(target=collect_stats, daemon=True)
    stats_thread.start()
    
    # Start Flask server
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)
