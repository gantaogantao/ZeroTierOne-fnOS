#!/usr/bin/env python3
import os
import json
import subprocess
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# 配置
PORT = 9994
UI_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ui')
ZT_CLI = None
ZT_HOME = None

def init_paths():
    global ZT_CLI, ZT_HOME
    # 从环境变量获取路径
    trim_appdest = os.environ.get('TRIM_APPDEST', '')
    trim_pkgvar = os.environ.get('TRIM_PKGVAR', '')
    
    print(f"DEBUG: TRIM_APPDEST={trim_appdest}")
    print(f"DEBUG: TRIM_PKGVAR={trim_pkgvar}")
    
    if trim_appdest:
        ZT_CLI = os.path.join(trim_appdest, 'zerotier', 'zerotier-cli')
    if trim_pkgvar:
        ZT_HOME = os.path.join(trim_pkgvar, 'zerotier-one')
    
    # 备用路径
    if not ZT_CLI or not os.path.exists(ZT_CLI):
        ZT_CLI = '/usr/bin/zerotier-cli'
    if not ZT_HOME:
        ZT_HOME = '/var/lib/zerotier-one'
    
    print(f"DEBUG: ZT_CLI={ZT_CLI}")
    print(f"DEBUG: ZT_HOME={ZT_HOME}")
    print(f"DEBUG: ZT_CLI exists={os.path.exists(ZT_CLI)}")
    if ZT_HOME:
        print(f"DEBUG: ZT_HOME exists={os.path.exists(ZT_HOME)}")

def is_zt_running_by_check():
    """通过检查进程或端口来判断 ZeroTier 是否在运行"""
    # 方法1: 检查 9993 端口
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('127.0.0.1', 9993))
        sock.close()
        if result == 0:
            return True
    except:
        pass
    
    # 方法2: 检查进程
    try:
        result = subprocess.run(['pgrep', '-f', 'zerotier-one'], capture_output=True, text=True, timeout=2)
        if result.returncode == 0 and result.stdout.strip():
            return True
    except:
        pass
    
    return False

def run_zt_cmd(args):
    """运行 ZeroTier 命令"""
    try:
        env = os.environ.copy()
        if ZT_HOME:
            env['ZT_HOME'] = ZT_HOME
            print(f"DEBUG: Running with ZT_HOME={ZT_HOME}")
        
        print(f"DEBUG: Running command: {ZT_CLI} {' '.join(args)}")
        
        result = subprocess.run(
            [ZT_CLI] + args,
            capture_output=True,
            text=True,
            env=env,
            timeout=10
        )
        
        print(f"DEBUG: Return code: {result.returncode}")
        print(f"DEBUG: stdout: {result.stdout[:100]}")
        print(f"DEBUG: stderr: {result.stderr[:100]}")
        
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        print(f"DEBUG: Exception: {e}")
        return False, '', str(e)

def get_networks():
    """获取已加入的网络列表"""
    networks = []
    try:
        success, stdout, stderr = run_zt_cmd(['-j', 'listnetworks'])
        if success:
            nets = json.loads(stdout)
            for net in nets:
                networks.append({
                    'nwid': net.get('nwid', ''),
                    'name': net.get('name', ''),
                    'status': net.get('status', 'UNKNOWN'),
                    'type': net.get('type', ''),
                    'mac': net.get('mac', ''),
                    'mtu': net.get('mtu', 0),
                    'dhcp': net.get('dhcp', False),
                    'assignedAddresses': net.get('assignedAddresses', [])
                })
            print(f"DEBUG: Got {len(networks)} networks from CLI")
    except Exception as e:
        print(f"DEBUG: get_networks exception: {e}")
    
    return networks

def is_zt_running():
    """检查 ZeroTier 是否在运行"""
    # 先用快速方法检查
    if is_zt_running_by_check():
        return True
    
    # 再用 zerotier-cli 检查
    try:
        success, stdout, stderr = run_zt_cmd(['status'])
        running = success and ("ONLINE" in stdout or "OK" in stdout)
        print(f"DEBUG: is_zt_running (CLI)={running}")
        return running
    except Exception as e:
        print(f"DEBUG: is_zt_running exception: {e}")
        return False

class ZeroTierHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=UI_DIR, **kwargs)
    
    def do_GET(self):
        print(f"DEBUG: GET {self.path}")
        if self.path == '/api/status':
            self.send_api_status()
        elif self.path == '/' or self.path == '/index.html':
            super().do_GET()
        elif self.path.startswith('/images/'):
            super().do_GET()
        else:
            # 其他路径也尝试提供静态文件
            super().do_GET()
    
    def do_POST(self):
        print(f"DEBUG::POST: {self.path}")
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        if self.path == '/api/join':
            self.send_api_join(data)
        elif self.path == '/api/leave':
            self.send_api_leave(data)
    
    def send_api_status(self):
        status = {
            'running': is_zt_running(),
            'networks': get_networks()
        }
        print(f"DEBUG: Sending status: {status}")
        self.send_json(status)
    
    def send_api_join(self, data):
        network_id = data.get('networkId', '')
        print(f"DEBUG: Joining network: {network_id}")
        if not network_id or len(network_id) != 16:
            self.send_json({'success': False, 'error': 'Invalid Network ID'})
            return
        
        success, stdout, stderr = run_zt_cmd(['join', network_id])
        if success:
            self.send_json({'success': True})
        else:
            self.send_json({'success': False, 'error': stderr or 'Failed to join network'})
    
    def send_api_leave(self, data):
        network_id = data.get('networkId', '')
        print(f"DEBUG: Leaving network: {network_id}")
        if not network_id or len(network_id) != 16:
            self.send_json({'success': False, 'error': 'Invalid Network ID'})
            return
        
        success, stdout, stderr = run_zt_cmd(['leave', network_id])
        if success:
            self.send_json({'success': True})
        else:
            self.send_json({'success': False, 'error': stderr or 'Failed to leave network'})
    
    def send_json(self, data):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def log_message(self, format, *args):
        # 禁用默认日志，用我们自己的
        pass

def main():
    init_paths()
    print(f"Starting ZeroTier Web UI on port {PORT}")
    print(f"UI_DIR: {UI_DIR}")
    
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, ZeroTierHandler)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        httpd.shutdown()

if __name__ == '__main__':
    main()
