/**
 * Kn3aux-Code Enhanced Console Logger
 * Professional logging system with levels, colors, and remote sync
 */

class Kn3auxLogger {
  constructor(options = {}) {
    this.prefix = options.prefix || '[KN3AUX]';
    this.colors = options.colors !== false;
    this.level = options.level || 'debug'; // debug, info, warn, error
    this.remoteSync = options.remoteSync || false;
    this.remoteUrl = options.remoteUrl || '/api/logs';
    this.logs = [];
    this.maxLogs = options.maxLogs || 1000;
    
    this.init();
  }

  init() {
    // Override console methods
    const originalLog = console.log;
    const originalWarn = console.warn;
    const originalError = console.error;
    const originalInfo = console.info;
    const originalDebug = console.debug;

    const self = this;

    console.log = function(...args) {
      self._log('log', args);
      originalLog.apply(console, args);
    };

    console.warn = function(...args) {
      self._log('warn', args);
      originalWarn.apply(console, args);
    };

    console.error = function(...args) {
      self._log('error', args);
      originalError.apply(console, args);
    };

    console.info = function(...args) {
      self._log('info', args);
      originalInfo.apply(console, args);
    };

    console.debug = function(...args) {
      self._log('debug', args);
      originalDebug.apply(console, args);
    };

    // Add custom methods
    console.kn3aux = {
      success: (...args) => self._log('success', args),
      api: (...args) => self._log('api', args),
      ws: (...args) => self._log('ws', args),
      device: (...args) => self._log('device', args),
      plugin: (...args) => self._log('plugin', args),
      command: (...args) => self._log('command', args),
      group: (label, fn) => self._group(label, fn),
      time: (label) => self._time(label),
      timeEnd: (label) => self._timeEnd(label),
      table: (data) => self._table(data),
      clear: () => self.clear(),
      export: () => self.export(),
      getLogs: () => self.getLogs()
    };

    console.log('%c[KN3AUX Logger] Enhanced logging system initialized', 'color: #34d399; font-weight: bold');
  }

  _getColor(level) {
    const colors = {
      log: '#94a3b8',
      debug: '#64748b',
      info: '#3b82f6',
      success: '#34d399',
      warn: '#fbbf24',
      error: '#ef4444',
      api: '#8b5cf6',
      ws: '#06b6d4',
      device: '#10b981',
      plugin: '#f59e0b',
      command: '#ec4899'
    };
    return colors[level] || colors.log;
  }

  _getIcon(level) {
    const icons = {
      log: '📝',
      debug: '🔍',
      info: 'ℹ️',
      success: '✅',
      warn: '⚠️',
      error: '❌',
      api: '🔌',
      ws: '📡',
      device: '📱',
      plugin: '🧩',
      command: '⚡'
    };
    return icons[level] || icons.log;
  }

  _log(level, args) {
    const timestamp = new Date().toISOString();
    const logEntry = {
      timestamp,
      level,
      message: args.map(a => typeof a === 'object' ? JSON.stringify(a) : String(a)).join(' '),
      data: args
    };

    // Store log
    this.logs.push(logEntry);
    if (this.logs.length > this.maxLogs) {
      this.logs.shift();
    }

    // Sync to remote if enabled
    if (this.remoteSync && ['error', 'warn'].includes(level)) {
      this._syncToRemote(logEntry);
    }
  }

  async _syncToRemote(logEntry) {
    try {
      await fetch(this.remoteUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(logEntry)
      });
    } catch (e) {
      // Silent fail for remote sync
    }
  }

  _group(label, fn) {
    console.group(`%c${label}`, `color: ${this._getColor('info')}; font-weight: bold`);
    try {
      fn();
    } finally {
      console.groupEnd();
    }
  }

  _timers = {};

  _time(label) {
    this._timers[label] = performance.now();
    console.log(`%c⏱ ${label}: Started`, 'color: #64748b');
  }

  _timeEnd(label) {
    const start = this._timers[label];
    if (start) {
      const duration = performance.now() - start;
      console.log(`%c⏱ ${label}: ${duration.toFixed(2)}ms`, 'color: #3b82f6');
      delete this._timers[label];
    }
  }

  _table(data) {
    if (Array.isArray(data) && data.length > 0) {
      console.log('%c📊 Data Table:', 'color: #8b5cf6; font-weight: bold');
      console.table(data);
    }
  }

  clear() {
    this.logs = [];
    console.clear();
    console.log('%c[KN3AUX Logger] Logs cleared', 'color: #64748b');
  }

  export() {
    const blob = new Blob([JSON.stringify(this.logs, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `kn3aux-logs-${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    URL.revokeObjectURL(url);
    console.log('%c[KN3AUX Logger] Logs exported', 'color: #34d399');
    return this.logs;
  }

  getLogs(filter = null) {
    if (!filter) return this.logs;
    return this.logs.filter(log => log.level === filter);
  }

  // Convenience methods
  success(...args) {
    this._log('success', args);
    const msg = args.join(' ');
    console.log(`%c${this._getIcon('success')} ${msg}`, `color: ${this._getColor('success')}; font-weight: 500`);
  }

  api(...args) {
    this._log('api', args);
    const msg = args.join(' ');
    console.log(`%c${this._getIcon('api')} API: ${msg}`, `color: ${this._getColor('api')}`);
  }

  ws(...args) {
    this._log('ws', args);
    const msg = args.join(' ');
    console.log(`%c${this._getIcon('ws')} WS: ${msg}`, `color: ${this._getColor('ws')}`);
  }

  device(...args) {
    this._log('device', args);
    const msg = args.join(' ');
    console.log(`%c${this._getIcon('device')} Device: ${msg}`, `color: ${this._getColor('device')}`);
  }

  plugin(...args) {
    this._log('plugin', args);
    const msg = args.join(' ');
    console.log(`%c${this._getIcon('plugin')} Plugin: ${msg}`, `color: ${this._getColor('plugin')}`);
  }

  command(...args) {
    this._log('command', args);
    const msg = args.join(' ');
    console.log(`%c${this._getIcon('command')} Command: ${msg}`, `color: ${this._getColor('command')}`);
  }
}

// Auto-initialize global logger
window.kn3auxLogger = new Kn3auxLogger({
  prefix: '[KN3AUX]',
  colors: true,
  level: 'debug',
  remoteSync: false
});

// Add to console for easy access
console.kn3auxLogger = window.kn3auxLogger;

// Usage examples (uncomment to test):
// console.kn3aux.success('System initialized');
// console.kn3aux.api('GET /api/plugins - 200 OK');
// console.kn3aux.ws('Connected to WebSocket');
// console.kn3aux.device('Pixel 9 Pro connected');
// console.kn3aux.plugin('MTK Tool v2.2.0 loaded');
// console.kn3aux.command('adb devices executed');
// console.kn3aux.time('Operation');
// setTimeout(() => console.kn3aux.timeEnd('Operation'), 1000);
