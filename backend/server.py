#!/usr/bin/env python3
"""
KN3AUX-CODE Backend Server
Flask + WebSocket server for Dashboard
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import subprocess
import psutil
import threading
import time
import os

app = Flask(__name__, static_folder='../frontend/src', static_url_path='')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Global stats
device_stats = {
    'battery': 87,
    'cpu': 34,
    'memory': 61,
    'network': '5G',
    'ip': '192.168.1.42',
    'storage': 73
}

# Background stats collector
def collect_stats():
    global device_stats
    while True:
        try:
            # Get battery (Android)
            battery_result = subprocess.run(
                ['adb', 'shell', 'dumpsys', 'battery', '|', 'grep', 'level'],
                shell=True, capture_output=True, text=True
            )
            if battery_result.returncode == 0:
                try:
                    device_stats['battery'] = int(battery_result.stdout.split()[-1])
                except:
                    pass
            
            # CPU
            device_stats['cpu'] = psutil.cpu_percent(interval=1)
            
            # Memory
            device_stats['memory'] = psutil.virtual_memory().percent
            
            # Storage
            device_stats['storage'] = psutil.disk_usage('/').percent
            
            # Emit to WebSocket
            socketio.emit('device-stats', device_stats)
            
            time.sleep(2)
        except Exception as e:
            print(f"Stats error: {e}")
            time.sleep(2)

# Start stats thread
stats_thread = threading.Thread(target=collect_stats, daemon=True)
stats_thread.start()

# Routes
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'pages/Dashboard.jsx')

@app.route('/api/status')
def get_status():
    return jsonify(device_stats)

@app.route('/api/frp/remove', methods=['POST'])
def frp_remove():
    """FRP Removal endpoint"""
    try:
        result = subprocess.run(
            ['adb', 'shell', 'content', 'insert', '--uri', 
             'content://settings/secure', '--bind', 
             'name:s:user_setup_complete', '--bind', 'value:s:1'],
            capture_output=True, text=True, timeout=10
        )
        return jsonify({
            'success': result.returncode == 0,
            'message': 'FRP bypass attempted'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/mtk/detect', methods=['POST'])
def mtk_detect():
    """MTK Device Detection"""
    try:
        result = subprocess.run(
            ['adb', 'shell', 'getprop', 'ro.product.board'],
            capture_output=True, text=True
        )
        chipset = result.stdout.strip()
        return jsonify({
            'success': True,
            'chipset': chipset or 'Unknown',
            'message': f'Detected: {chipset}'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/backup/run', methods=['POST'])
def run_backup():
    """Run backup"""
    try:
        result = subprocess.run(
            ['bash', os.path.expanduser('~/kn3aux-code/backup-termux.sh')],
            capture_output=True, text=True, timeout=300
        )
        return jsonify({
            'success': result.returncode == 0,
            'output': result.stdout
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/terminal/run', methods=['POST'])
def run_terminal():
    """Run terminal command"""
    try:
        command = request.json.get('command', '')
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=60
        )
        return jsonify({
            'success': True,
            'output': result.stdout,
            'error': result.stderr
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# WebSocket events
@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('device-stats', device_stats)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('run-command')
def handle_command(data):
    command = data.get('command')
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=60
        )
        emit('command-result', {
            'command': command,
            'output': result.stdout,
            'success': True
        })
    except Exception as e:
        emit('command-result', {
            'command': command,
            'error': str(e),
            'success': False
        })

if __name__ == '__main__':
    print("╔══════════════════════════════════════════════════════════╗")
    print("║         KN3AUX-CODE Backend Server Starting              ║" )
    print("╚══════════════════════════════════════════════════════════╝")
    print("")
    print("Backend running on: http://localhost:5000")
    print("WebSocket: ws://localhost:5000")
    print("")
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
