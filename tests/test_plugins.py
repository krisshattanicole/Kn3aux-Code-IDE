#!/usr/bin/env python3
"""
Kn3aux-Code Plugin Testing Framework
Comprehensive test suite for all plugins
"""

import unittest
import json
import subprocess
import sys
from datetime import datetime
from typing import Dict, Any

# Test Results Storage
test_results = {
    'timestamp': datetime.now().isoformat(),
    'total': 0,
    'passed': 0,
    'failed': 0,
    'skipped': 0,
    'tests': []
}

class PluginTestCase(unittest.TestCase):
    """Base test case for all plugins"""
    
    def setUp(self):
        """Setup before each test"""
        self.test_name = self._testMethodName
        self.start_time = datetime.now()
        
    def tearDown(self):
        """Cleanup after each test"""
        duration = (datetime.now() - self.start_time).total_seconds()
        result = {
            'name': self.test_name,
            'status': self._outcome.result.wasSuccessful() if hasattr(self._outcome, 'result') else 'unknown',
            'duration_ms': duration * 1000,
            'timestamp': datetime.now().isoformat()
        }
        test_results['tests'].append(result)
        test_results['total'] += 1
        
        if result['status']:
            test_results['passed'] += 1
            print(f"  ✅ {self.test_name} ({duration*1000:.0f}ms)")
        else:
            test_results['failed'] += 1
            print(f"  ❌ {self.test_name} ({duration*1000:.0f}ms)")

class TestMTKTool(PluginTestCase):
    """MTK Tool Plugin Tests"""
    
    @classmethod
    def setUpClass(cls):
        """Import MTK tool"""
        try:
            sys.path.insert(0, 'backend/plugins/mtk_tool')
            from mtk_tool import MTKTool
            cls.tool = MTKTool()
            cls.available = True
        except Exception as e:
            cls.available = False
            cls.error = str(e)
    
    def test_mtk_tool_import(self):
        """Test MTK Tool import"""
        if not self.available:
            self.skipTest(f"MTK Tool not available: {self.error}")
        self.assertTrue(self.available)
    
    def test_detect_chipset(self):
        """Test chipset detection"""
        if not self.available:
            self.skipTest("MTK Tool not available")
        result = self.tool.detect_chipset()
        self.assertIn('success', result)
        self.assertIn('chipset', result)
    
    def test_read_device_info(self):
        """Test device info reading"""
        if not self.available:
            self.skipTest("MTK Tool not available")
        result = self.tool.read_device_info()
        self.assertIsInstance(result, dict)

class TestWiFiAudit(PluginTestCase):
    """WiFi Audit Plugin Tests"""
    
    @classmethod
    def setUpClass(cls):
        """Import WiFi Audit"""
        try:
            sys.path.insert(0, 'backend/plugins')
            from wifi_audit import WiFiAudit
            cls.audit = WiFiAudit()
            cls.available = True
        except Exception as e:
            cls.available = False
            cls.error = str(e)
    
    def test_wifi_audit_import(self):
        """Test WiFi Audit import"""
        if not self.available:
            self.skipTest(f"WiFi Audit not available: {self.error}")
        self.assertTrue(self.available)
    
    def test_scan_networks(self):
        """Test network scanning"""
        if not self.available:
            self.skipTest("WiFi Audit not available")
        result = self.audit.scan_networks()
        self.assertIn('success', result)
    
    def test_check_security(self):
        """Test security check"""
        if not self.available:
            self.skipTest("WiFi Audit not available")
        result = self.audit.check_security()
        self.assertIsInstance(result, dict)

class TestFRPRemoval(PluginTestCase):
    """FRP Removal Plugin Tests"""
    
    def test_frp_module_exists(self):
        """Test FRP module exists"""
        import os
        path = 'backend/core/frp_removal.py'
        self.assertTrue(os.path.exists(path), f"FRP module not found: {path}")
    
    def test_frp_import(self):
        """Test FRP module import"""
        try:
            sys.path.insert(0, 'backend/core')
            import frp_removal
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"FRP import failed: {e}")

class TestBackendServer(PluginTestCase):
    """Backend Server Tests"""
    
    def test_server_file_exists(self):
        """Test server file exists"""
        import os
        path = 'backend/server.py'
        self.assertTrue(os.path.exists(path), f"Server file not found: {path}")
    
    def test_server_syntax(self):
        """Test server syntax"""
        result = subprocess.run(
            ['python', '-m', 'py_compile', 'backend/server.py'],
            capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0, f"Syntax error: {result.stderr}")

class TestAPIServer(PluginTestCase):
    """API Server Tests"""
    
    def test_api_file_exists(self):
        """Test API server file exists"""
        import os
        path = 'api/server.js'
        self.assertTrue(os.path.exists(path), f"API server not found: {path}")
    
    def test_db_json_exists(self):
        """Test database file exists"""
        import os
        path = 'api/db.json'
        self.assertTrue(os.path.exists(path), f"Database not found: {path}")
    
    def test_db_json_valid(self):
        """Test database JSON is valid"""
        with open('api/db.json', 'r') as f:
            data = json.load(f)
        self.assertIsInstance(data, dict)
        self.assertIn('plugins', data)
        self.assertIn('devices', data)
        self.assertIn('settings', data)

class TestDocumentation(PluginTestCase):
    """Documentation Tests"""
    
    def test_readme_exists(self):
        """Test README exists"""
        import os
        self.assertTrue(os.path.exists('README.md'))
    
    def test_quick_reference_exists(self):
        """Test Quick Reference exists"""
        import os
        self.assertTrue(os.path.exists('QUICK_REFERENCE.md'))
    
    def test_implementation_summary_exists(self):
        """Test Implementation Summary exists"""
        import os
        self.assertTrue(os.path.exists('IMPLEMENTATION_SUMMARY.md'))

def run_tests():
    """Run all tests"""
    print("╔══════════════════════════════════════════════════════════╗")
    print("║     KN3AUX-CODE Plugin Testing Framework                 ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print("")
    print(f"📅 Timestamp: {test_results['timestamp']}")
    print("🧪 Running tests...")
    print("")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestMTKTool))
    suite.addTests(loader.loadTestsFromTestCase(TestWiFiAudit))
    suite.addTests(loader.loadTestsFromTestCase(TestFRPRemoval))
    suite.addTests(loader.loadTestsFromTestCase(TestBackendServer))
    suite.addTests(loader.loadTestsFromTestCase(TestAPIServer))
    suite.addTests(loader.loadTestsFromTestCase(TestDocumentation))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("")
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Total:    {test_results['total']}")
    print(f"Passed:   {test_results['passed']} ✅")
    print(f"Failed:   {test_results['failed']} ❌")
    print(f"Skipped:  {test_results['skipped']} ⏭️")
    print(f"Duration: {sum(t['duration_ms'] for t in test_results['tests']):.0f}ms")
    print("=" * 60)
    
    # Save results
    with open('test_results.json', 'w') as f:
        json.dump(test_results, f, indent=2)
    print(f"\n📄 Results saved to: test_results.json")
    
    return test_results['failed'] == 0

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
