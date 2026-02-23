#!/usr/bin/env python3
"""
MTK Tool Plugin - MediaTek Device Utilities
"""

import subprocess
import json
from typing import Dict, Any

class MTKTool:
    """MediaTek device tools"""
    
    def __init__(self):
        self.device_id = None
        
    def detect_chipset(self) -> Dict[str, Any]:
        """Detect MediaTek chipset"""
        try:
            result = subprocess.run(
                ['adb', 'shell', 'getprop', 'ro.product.board'],
                capture_output=True, text=True, timeout=5
            )
            chipset = result.stdout.strip()
            return {
                'success': True,
                'chipset': chipset or 'Unknown',
                'is_mtk': 'mtk' in chipset.lower() or 'mediatek' in chipset.lower()
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def read_device_info(self) -> Dict[str, Any]:
        """Read full device information"""
        try:
            commands = {
                'brand': ['adb', 'shell', 'getprop', 'ro.product.brand'],
                'model': ['adb', 'shell', 'getprop', 'ro.product.model'],
                'device': ['adb', 'shell', 'getprop', 'ro.product.device'],
                'sdk': ['adb', 'shell', 'getprop', 'ro.build.version.sdk'],
                'android': ['adb', 'shell', 'getprop', 'ro.build.version.release'],
                'security_patch': ['adb', 'shell', 'getprop', 'ro.build.version.security_patch'],
                'build_id': ['adb', 'shell', 'getprop', 'ro.build.id'],
            }
            
            info = {}
            for key, cmd in commands.items():
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                info[key] = result.stdout.strip()
            
            return {'success': True, 'info': info}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def reboot_bootloader(self) -> Dict[str, Any]:
        """Reboot device to bootloader"""
        try:
            result = subprocess.run(
                ['adb', 'reboot', 'bootloader'],
                capture_output=True, text=True, timeout=10
            )
            return {'success': result.returncode == 0}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def reboot_recovery(self) -> Dict[str, Any]:
        """Reboot device to recovery"""
        try:
            result = subprocess.run(
                ['adb', 'reboot', 'recovery'],
                capture_output=True, text=True, timeout=10
            )
            return {'success': result.returncode == 0}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def flash_partition(self, partition: str, file: str) -> Dict[str, Any]:
        """Flash a partition (requires unlocked bootloader)"""
        try:
            result = subprocess.run(
                ['fastboot', 'flash', partition, file],
                capture_output=True, text=True, timeout=300
            )
            return {
                'success': result.returncode == 0,
                'output': result.stdout,
                'error': result.stderr
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

# Export functions for backend
def detect_mtk_device() -> Dict[str, Any]:
    """Detect if connected device is MediaTek"""
    tool = MTKTool()
    return tool.detect_chipset()

def get_device_info() -> Dict[str, Any]:
    """Get full device information"""
    tool = MTKTool()
    return tool.read_device_info()

if __name__ == '__main__':
    # Test
    print("MTK Tool Plugin")
    print("===============")
    result = detect_mtk_device()
    print(json.dumps(result, indent=2))
