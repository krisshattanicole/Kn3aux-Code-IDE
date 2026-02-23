# Kn3aux-Code IDE - Complete Setup Guide

## 🚀 Overview

Kn3aux-Code IDE is a next-generation autonomous mobile development environment with integrated security tools, device management, and cloud deployment capabilities.

**Version**: 5.0  
**Platform**: Termux/Android with Web Interface  
**Backend**: Python Flask + WebSocket  
**Frontend**: React + TailwindCSS

---

## 📦 Features

### Core Tools
- **Dashboard** - Real-time device monitoring and stats
- **Network Scanner** - Analyze network devices
- **Metasploit Integration** - Penetration testing
- **Reverse Engineering** - APK analysis tools
- **WiFi Audit** - Security testing
- **Web Tester** - Vulnerability scanning
- **Script Runner** - Custom automation
- **Root Assistant** - Device management
- **FRP Removal** - Factory reset protection bypass
- **APK Analyzer** - App modification tools
- **AI Agent** - Intelligent assistance
- **Backup Manager** - Device backup/restore
- **MTK Tool** - MediaTek device utilities

### New Features (v5.0)
- ✅ **GitHub OAuth Authentication**
- ✅ **Netlify Auto-Deployment**
- ✅ **JSON Server API**
- ✅ **Enhanced Plugin System**
- ✅ **Real-time WebSocket Updates**

---

## 🛠️ Installation

### Prerequisites
- Termux (Android)
- Python 3.10+
- Node.js 18+
- Git

### 1. Clone Repository
```bash
git clone https://github.com/krisshattanicole/Kn3aux-Code-IDE.git
cd Kn3aux-Code-IDE
```

### 2. Install Backend Dependencies
```bash
cd backend
pip install flask flask-socketio flask-cors psutil
```

### 3. Install Frontend Dependencies
```bash
cd frontend
npm install
```

### 4. Install API Server (Optional)
```bash
cd api
npm install
```

---

## 🚀 Quick Start

### Start Backend Server
```bash
cd backend
python server.py
```

### Start API Server (Optional)
```bash
cd api
npm start
```

### Access Dashboard
Open browser: `http://localhost:5000`

---

## 🔐 GitHub Login Setup

### 1. Create Firebase Project
1. Visit [Firebase Console](https://console.firebase.google.com)
2. Create new project
3. Enable Authentication → GitHub provider

### 2. Configure OAuth
1. Create GitHub OAuth App
2. Set callback: `https://YOUR_PROJECT.firebaseapp.com/__/auth/handler`
3. Add credentials to Firebase

### 3. Update Config
Edit `public/assets/config/firebase.config.js`:
```javascript
const defaultConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "your-project.firebaseapp.com",
  projectId: "your-project-id",
  // ... rest of config
};
```

### 4. Set Netlify Secrets
In GitHub Repository Settings → Secrets:
- `NETLIFY_AUTH_TOKEN`: Your Netlify token
- `NETLIFY_SITE_ID`: Your site ID

---

## 📡 API Endpoints

### JSON Server (Port 3000)
```
GET  /api/plugins          - List all plugins
GET  /api/devices          - Connected devices
POST /api/commands/run     - Execute command
GET  /api/logs             - System logs
GET  /api/settings         - App settings
```

### Flask Backend (Port 5000)
```
GET  /api/status           - Device stats
POST /api/frp/remove       - FRP bypass
POST /api/mtk/detect       - MTK detection
POST /api/backup/run       - Run backup
POST /api/terminal/run     - Terminal command
WS   /socket.io/           - WebSocket
```

---

## 🧩 Plugin Architecture

### Creating Plugins
```python
# backend/plugins/my_plugin.py
class MyPlugin:
    def execute(self, params):
        return {'success': True, 'data': params}
```

### Plugin Manager
```python
from backend.plugins.plugin_manager import PluginManager

manager = PluginManager()
manager.load_plugin('my_plugin')
result = manager.execute('my_plugin', {'key': 'value'})
```

---

## 🌐 Netlify Deployment

### Automatic Deployment
Push to `main` branch → GitHub Actions → Netlify

### Manual Deploy
```bash
npm install -g netlify-cli@17.38.0
cd frontend
npm run build
netlify deploy --prod --dir=dist
```

---

## 📊 Project Structure

```
Kn3aux-Code-IDE/
├── backend/
│   ├── core/
│   │   ├── device_intelligence.py
│   │   └── frp_removal.py
│   ├── plugins/
│   │   ├── mtk_tool/
│   │   ├── wifi_audit.py
│   │   └── plugin_manager.py
│   └── server.py
├── frontend/
│   ├── src/
│   │   └── pages/
│   │       └── Dashboard.jsx
│   ├── index.html
│   └── package.json
├── api/
│   ├── server.js
│   └── db.json
├── assets/
│   ├── ace/           # Editor
│   ├── bundle/        # Bundled JS/CSS
│   ├── templates/     # Project templates
│   └── workers/       # Web workers
├── pwa/
│   ├── index.html
│   └── sw.js
├── .github/
│   └── workflows/
│       └── netlify-deploy.yml
└── GITHUB_LOGIN_NETLIFY_SETUP.md
```

---

## 🔧 Configuration

### Environment Variables
```bash
# Backend
FLASK_PORT=5000
FLASK_DEBUG=false

# Frontend
VITE_API_URL=http://localhost:5000
VITE_WS_URL=ws://localhost:5000

# API Server
PORT=3000
```

### Settings (db.json)
```json
{
  "settings": {
    "theme": "dark",
    "language": "en",
    "autoBackup": true,
    "notifications": true,
    "debugMode": false
  }
}
```

---

## 🧪 Testing

### Run Tests
```bash
# Backend
cd backend
python -m pytest

# Frontend
cd frontend
npm test
```

### Test Plugins
```bash
cd backend/plugins
python mtk_tool.py
python wifi_audit.py
```

---

## 📝 Usage Examples

### Execute Command
```bash
curl -X POST http://localhost:5000/api/terminal/run \
  -H "Content-Type: application/json" \
  -d '{"command": "ls -la"}'
```

### Get Device Info
```bash
curl http://localhost:3000/api/devices
```

### List Plugins
```bash
curl http://localhost:3000/api/plugins
```

---

## 🐛 Troubleshooting

### Backend Won't Start
```bash
# Check Python version
python --version  # Should be 3.10+

# Install dependencies
pip install -r requirements.txt
```

### Frontend Build Fails
```bash
# Clear cache
rm -rf node_modules package-lock.json
npm install
npm run build
```

### WebSocket Connection Failed
- Check firewall settings
- Ensure backend is running
- Verify WS_URL configuration

---

## 📚 Documentation

- [GitHub Login Setup](GITHUB_LOGIN_NETLIFY_SETUP.md)
- [FRP Removal Guide](ASHELL-FRP-REMOVAL-GUIDE.md)
- [Quick Start](QUICKSTART.md)
- [Complete Setup](COMPLETE_SETUP_GUIDE.md)

---

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

---

## 📄 License

MIT License - See LICENSE file

---

## 👥 Credits

**Developed by**: Krisshatta Nicole  
**Repository**: https://github.com/krisshattanicole/Kn3aux-Code-IDE  
**Version**: 5.0 (2026)

---

## 📞 Support

- GitHub Issues: https://github.com/krisshattanicole/Kn3aux-Code-IDE/issues
- Email: support@kn3aux.com

---

**Happy Coding! 🚀**
