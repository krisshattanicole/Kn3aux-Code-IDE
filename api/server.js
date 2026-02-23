/**
 * JSON Server for Kn3aux-Code IDE
 * Provides REST API endpoints for the frontend
 */

const jsonServer = require('json-server');
const cors = require('cors');
const express = require('express');
const path = require('path');

const app = express();
const router = jsonServer.router('db.json');
const middlewares = jsonServer.defaults();

// Middleware
app.use(cors());
app.use(express.json());
app.use(middlewares);

// Custom routes
app.post('/api/auth/login', (req, res) => {
  const { username, password } = req.body;
  // Simulated login
  res.json({
    success: true,
    token: 'mock-jwt-token-' + Date.now(),
    user: { id: 1, username, email: username + '@example.com' }
  });
});

app.get('/api/devices', (req, res) => {
  res.json({
    devices: [
      { id: 1, name: 'Pixel 9 Pro', status: 'connected', battery: 87, signal: '5G' },
      { id: 2, name: 'Samsung A14', status: 'disconnected', battery: 0, signal: null }
    ]
  });
});

app.post('/api/commands/run', (req, res) => {
  const { command } = req.body;
  res.json({
    success: true,
    output: `Command executed: ${command}`,
    timestamp: new Date().toISOString()
  });
});

// Use default router
app.use(router);

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`╔══════════════════════════════════════════════════════════╗`);
  console.log(`║      KN3AUX-CODE JSON Server Starting                    ║`);
  console.log(`╚══════════════════════════════════════════════════════════╝`);
  console.log(``);
  console.log(`API running on: http://localhost:${PORT}`);
  console.log(`JSON Server: http://localhost:${PORT}/api`);
  console.log(``);
});
