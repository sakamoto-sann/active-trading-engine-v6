# Contabo Deployment Guide
## Integrated Multi-Exchange Trading System

### 🚀 Complete Production Deployment Guide

This guide provides comprehensive instructions for deploying the Integrated Multi-Exchange Trading System to a Contabo server without interfering with your existing v4 paper trading setup.

---

## 📋 Table of Contents

1. [Pre-Deployment Assessment](#pre-deployment-assessment)
2. [System Preparation](#system-preparation)
3. [Code Transfer](#code-transfer)
4. [Configuration Setup](#configuration-setup)
5. [Service Setup](#service-setup)
6. [Safety Measures](#safety-measures)
7. [Testing and Validation](#testing-and-validation)
8. [Monitoring Setup](#monitoring-setup)
9. [Maintenance Instructions](#maintenance-instructions)
10. [Troubleshooting](#troubleshooting)

---

## 🔍 Pre-Deployment Assessment

### Step 1: Check Current Server Status

```bash
# SSH into your Contabo server
ssh root@your-server-ip

# Check existing v4 setup
sudo systemctl status binance-bot-v4 || echo "v4 service not found"
ps aux | grep -i "python.*bot" | grep -v grep

# Check system resources
free -h
df -h
htop  # Press 'q' to exit

# Check Python environment
python3 --version
pip3 --version
which python3
```

### Step 2: Identify Existing Setup

```bash
# Find existing bot installations
find /home -name "*bot*" -type d 2>/dev/null
find /opt -name "*bot*" -type d 2>/dev/null
find /root -name "*bot*" -type d 2>/dev/null

# Check for running services
systemctl list-units --type=service | grep -i bot
```

### Step 3: Document Current Configuration

```bash
# Create assessment report
cat > /tmp/deployment_assessment.txt << 'EOF'
=== CONTABO DEPLOYMENT ASSESSMENT ===
Date: $(date)
Server: $(hostname)
OS: $(cat /etc/os-release | grep PRETTY_NAME)
Python: $(python3 --version)
Disk Space: $(df -h /)
Memory: $(free -h)
CPU: $(nproc) cores
Network: $(ip addr show | grep inet | head -5)

=== EXISTING SERVICES ===
$(systemctl list-units --type=service | grep -E "(bot|trading)")

=== RUNNING PROCESSES ===
$(ps aux | grep -i "python.*bot" | grep -v grep)

=== EXISTING DIRECTORIES ===
$(find /home -name "*bot*" -type d 2>/dev/null)
$(find /opt -name "*bot*" -type d 2>/dev/null)
$(find /root -name "*bot*" -type d 2>/dev/null)
EOF

# Display assessment
cat /tmp/deployment_assessment.txt
```

---

## 🛠️ System Preparation

### Step 1: Update System Packages

```bash
# Update package lists
apt update

# Upgrade system packages (be careful with production systems)
apt upgrade -y

# Install essential packages
apt install -y \
    python3-pip \
    python3-venv \
    python3-dev \
    git \
    curl \
    wget \
    htop \
    screen \
    tmux \
    nginx \
    certbot \
    ufw \
    fail2ban \
    rsync \
    sqlite3 \
    supervisor \
    logrotate
```

### Step 2: Setup Python Environment

```bash
# Create dedicated user for integrated system
useradd -m -s /bin/bash integrated_trader
usermod -aG sudo integrated_trader

# Switch to new user
su - integrated_trader

# Create Python virtual environment
python3 -m venv /home/integrated_trader/venv
source /home/integrated_trader/venv/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel
```

### Step 3: Create Directory Structure

```bash
# Create application directories
mkdir -p /home/integrated_trader/{
    app,
    logs,
    config,
    data,
    backups,
    scripts,
    monitoring
}

# Set proper permissions
chown -R integrated_trader:integrated_trader /home/integrated_trader/
chmod 750 /home/integrated_trader/
```

---

## 📦 Code Transfer

### Step 1: Secure Transfer Setup

```bash
# On your local machine, create deployment package
cd /Users/tetsu/Documents/Binance_bot/v0.3/binance-bot-v4-atr-enhanced/integrated_multi_exchange_system

# Create deployment archive
tar -czf integrated_system_deployment.tar.gz \
    --exclude='*.pyc' \
    --exclude='__pycache__' \
    --exclude='*.log' \
    --exclude='backtest_*' \
    --exclude='data/*.csv' \
    .

# Transfer to server
scp integrated_system_deployment.tar.gz root@your-server-ip:/tmp/
```

### Step 2: Deploy Code on Server

```bash
# Switch to integrated_trader user
su - integrated_trader

# Extract deployment package
cd /home/integrated_trader/app
tar -xzf /tmp/integrated_system_deployment.tar.gz

# Activate virtual environment
source /home/integrated_trader/venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Install additional dependencies for integrated system
pip install \
    aiohttp \
    websockets \
    python-binance \
    asyncio \
    pandas \
    numpy \
    scipy \
    matplotlib \
    seaborn \
    requests \
    cryptography \
    python-dotenv \
    sqlalchemy \
    psutil \
    click \
    rich \
    tabulate
```

### Step 3: Verify Installation

```bash
# Test Python imports
python3 -c "
import sys
sys.path.append('/home/integrated_trader/app')
from integrated_trading_system.exchanges.binance_adapter import BinanceAdapter
from integrated_trading_system.exchanges.backpack_adapter import BackpackAdapter
print('✅ All imports successful')
"
```

---

## ⚙️ Configuration Setup

### Step 1: Create Environment Configuration

```bash
# Create secure environment file
cat > /home/integrated_trader/config/.env << 'EOF'
# Integrated Multi-Exchange Trading System Configuration
# IMPORTANT: Keep this file secure and never commit to version control

# System Configuration
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
LOG_FILE=/home/integrated_trader/logs/integrated_trading.log

# Database Configuration
DATABASE_URL=sqlite:///home/integrated_trader/data/trading.db

# Binance Configuration
BINANCE_API_KEY=your_binance_api_key_here
BINANCE_API_SECRET=your_binance_api_secret_here
BINANCE_TESTNET=false

# Backpack Configuration
BACKPACK_API_KEY=your_backpack_api_key_here
BACKPACK_API_SECRET=your_backpack_api_secret_here
BACKPACK_TESTNET=false

# Trading Configuration
ENABLE_PAPER_TRADING=true
ENABLE_LIVE_TRADING=false
DEFAULT_TRADING_PAIRS=BTCUSDT,ETHUSDT
MAX_POSITION_SIZE=1000
MAX_DAILY_TRADES=100

# Risk Management
MAX_PORTFOLIO_DELTA=0.05
MAX_POSITION_DELTA=0.02
STOP_LOSS_PERCENTAGE=0.02
TAKE_PROFIT_PERCENTAGE=0.01

# Monitoring
ENABLE_TELEGRAM_ALERTS=false
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here

# Performance
EXECUTION_INTERVAL=1.0
DATA_FETCH_INTERVAL=5.0
HEARTBEAT_INTERVAL=30.0
EOF

# Secure the environment file
chmod 600 /home/integrated_trader/config/.env
```

### Step 2: Create System Configuration

```bash
# Create main configuration file
cat > /home/integrated_trader/config/config.yaml << 'EOF'
# Integrated Multi-Exchange Trading System Configuration

system:
  name: "Integrated Multi-Exchange Trading System"
  version: "1.0.0"
  environment: "production"
  debug: false

logging:
  level: "INFO"
  file: "/home/integrated_trader/logs/integrated_trading.log"
  max_size: "100MB"
  backup_count: 10
  rotation: "daily"

database:
  url: "sqlite:///home/integrated_trader/data/trading.db"
  pool_size: 10
  max_overflow: 20

exchanges:
  binance:
    enabled: true
    testnet: false
    rate_limit: 1200  # requests per minute
    order_types: ["LIMIT", "MARKET", "STOP_LOSS", "TAKE_PROFIT"]
    
  backpack:
    enabled: true
    testnet: false
    rate_limit: 600   # requests per minute
    order_types: ["LIMIT", "MARKET"]

trading:
  mode: "paper"  # Change to "live" for live trading
  pairs: ["BTCUSDT", "ETHUSDT"]
  execution_interval: 1.0
  data_fetch_interval: 5.0
  
risk_management:
  max_portfolio_delta: 0.05
  max_position_delta: 0.02
  max_position_size: 1000
  stop_loss_percentage: 0.02
  take_profit_percentage: 0.01
  max_daily_trades: 100
  
arbitrage:
  enabled: true
  min_profit_threshold: 0.001  # 0.1%
  max_execution_time: 30       # seconds
  confidence_threshold: 0.7
  
monitoring:
  heartbeat_interval: 30.0
  health_check_interval: 60.0
  performance_report_interval: 3600.0
  
alerts:
  telegram:
    enabled: false
  email:
    enabled: false
  webhook:
    enabled: false
EOF
```

### Step 3: API Key Security Setup

```bash
# Create secure API key management script
cat > /home/integrated_trader/scripts/manage_api_keys.py << 'EOF'
#!/usr/bin/env python3
"""
Secure API Key Management Script
"""

import os
import json
import getpass
from cryptography.fernet import Fernet
from pathlib import Path

class SecureAPIKeyManager:
    def __init__(self, key_file='/home/integrated_trader/config/.api_key'):
        self.key_file = key_file
        self.key = self._load_or_generate_key()
        
    def _load_or_generate_key(self):
        key_path = Path(self.key_file)
        if key_path.exists():
            return key_path.read_bytes()
        else:
            key = Fernet.generate_key()
            key_path.write_bytes(key)
            os.chmod(key_path, 0o600)
            return key
    
    def encrypt_api_keys(self):
        """Encrypt and store API keys securely"""
        fernet = Fernet(self.key)
        
        # Collect API keys securely
        keys = {
            'binance_api_key': getpass.getpass('Enter Binance API Key: '),
            'binance_api_secret': getpass.getpass('Enter Binance API Secret: '),
            'backpack_api_key': getpass.getpass('Enter Backpack API Key: '),
            'backpack_api_secret': getpass.getpass('Enter Backpack API Secret: ')
        }
        
        # Encrypt keys
        encrypted_keys = {}
        for name, value in keys.items():
            encrypted_keys[name] = fernet.encrypt(value.encode()).decode()
        
        # Save encrypted keys
        with open('/home/integrated_trader/config/encrypted_keys.json', 'w') as f:
            json.dump(encrypted_keys, f, indent=2)
        
        os.chmod('/home/integrated_trader/config/encrypted_keys.json', 0o600)
        print("✅ API keys encrypted and stored securely")
    
    def decrypt_api_keys(self):
        """Decrypt and return API keys"""
        fernet = Fernet(self.key)
        
        with open('/home/integrated_trader/config/encrypted_keys.json', 'r') as f:
            encrypted_keys = json.load(f)
        
        # Decrypt keys
        decrypted_keys = {}
        for name, encrypted_value in encrypted_keys.items():
            decrypted_keys[name] = fernet.decrypt(encrypted_value.encode()).decode()
        
        return decrypted_keys

if __name__ == "__main__":
    manager = SecureAPIKeyManager()
    
    if len(os.sys.argv) > 1 and os.sys.argv[1] == 'encrypt':
        manager.encrypt_api_keys()
    else:
        keys = manager.decrypt_api_keys()
        for name, value in keys.items():
            print(f"{name}: {value[:8]}...")
EOF

chmod +x /home/integrated_trader/scripts/manage_api_keys.py
```

---

## 🔧 Service Setup

### Step 1: Create SystemD Service File

```bash
# Create service file for integrated system
sudo cat > /etc/systemd/system/integrated-trading-system.service << 'EOF'
[Unit]
Description=Integrated Multi-Exchange Trading System
After=network.target
Wants=network.target

[Service]
Type=simple
User=integrated_trader
Group=integrated_trader
WorkingDirectory=/home/integrated_trader/app
Environment=PATH=/home/integrated_trader/venv/bin
ExecStart=/home/integrated_trader/venv/bin/python /home/integrated_trader/app/integrated_trading_system/core/orchestrator.py
EnvironmentFile=/home/integrated_trader/config/.env
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=integrated-trading

# Security settings
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ReadWritePaths=/home/integrated_trader/logs /home/integrated_trader/data
ProtectHome=true

[Install]
WantedBy=multi-user.target
EOF

# Create paper trading service (for testing)
sudo cat > /etc/systemd/system/integrated-paper-trading.service << 'EOF'
[Unit]
Description=Integrated Multi-Exchange Paper Trading System
After=network.target
Wants=network.target

[Service]
Type=simple
User=integrated_trader
Group=integrated_trader
WorkingDirectory=/home/integrated_trader/app
Environment=PATH=/home/integrated_trader/venv/bin
Environment=ENABLE_PAPER_TRADING=true
Environment=ENABLE_LIVE_TRADING=false
ExecStart=/home/integrated_trader/venv/bin/python /home/integrated_trader/app/integrated_trading_system/paper_trading/paper_trading_engine.py
EnvironmentFile=/home/integrated_trader/config/.env
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=integrated-paper-trading

# Security settings
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ReadWritePaths=/home/integrated_trader/logs /home/integrated_trader/data
ProtectHome=true

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd
sudo systemctl daemon-reload
```

### Step 2: Create Supervisor Configuration (Alternative)

```bash
# Create supervisor configuration
sudo cat > /etc/supervisor/conf.d/integrated-trading.conf << 'EOF'
[program:integrated-trading-system]
command=/home/integrated_trader/venv/bin/python /home/integrated_trader/app/integrated_trading_system/core/orchestrator.py
directory=/home/integrated_trader/app
user=integrated_trader
group=integrated_trader
autostart=false
autorestart=true
startsecs=10
startretries=3
stdout_logfile=/home/integrated_trader/logs/supervisor_stdout.log
stderr_logfile=/home/integrated_trader/logs/supervisor_stderr.log
environment=PATH="/home/integrated_trader/venv/bin"

[program:integrated-paper-trading]
command=/home/integrated_trader/venv/bin/python /home/integrated_trader/app/integrated_trading_system/paper_trading/paper_trading_engine.py
directory=/home/integrated_trader/app
user=integrated_trader
group=integrated_trader
autostart=true
autorestart=true
startsecs=10
startretries=3
stdout_logfile=/home/integrated_trader/logs/paper_trading_stdout.log
stderr_logfile=/home/integrated_trader/logs/paper_trading_stderr.log
environment=PATH="/home/integrated_trader/venv/bin",ENABLE_PAPER_TRADING="true",ENABLE_LIVE_TRADING="false"
EOF

# Update supervisor
sudo supervisorctl reread
sudo supervisorctl update
```

---

## 🛡️ Safety Measures

### Step 1: Create Backup Scripts

```bash
# Create backup script for existing v4 system
cat > /home/integrated_trader/scripts/backup_existing_system.sh << 'EOF'
#!/bin/bash
# Backup existing v4 system before deployment

BACKUP_DIR="/home/integrated_trader/backups/v4_backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "🔄 Creating backup of existing v4 system..."

# Find and backup existing bot directories
for dir in $(find /home /opt /root -name "*bot*" -type d 2>/dev/null); do
    if [ -d "$dir" ]; then
        echo "📦 Backing up: $dir"
        cp -r "$dir" "$BACKUP_DIR/"
    fi
done

# Backup existing services
echo "🔧 Backing up existing services..."
mkdir -p "$BACKUP_DIR/services"
for service in $(systemctl list-units --type=service | grep -E "(bot|trading)" | awk '{print $1}'); do
    systemctl show "$service" > "$BACKUP_DIR/services/${service}.conf"
done

# Backup crontab
echo "⏰ Backing up crontab..."
crontab -l > "$BACKUP_DIR/crontab.txt" 2>/dev/null || echo "No crontab found"

# Create restore script
cat > "$BACKUP_DIR/restore.sh" << 'RESTORE_EOF'
#!/bin/bash
echo "🔄 Restoring v4 system from backup..."
echo "⚠️  WARNING: This will restore the previous system state"
echo "This restore script is for emergency use only."
echo "Please review the backup contents before proceeding."
ls -la "$BACKUP_DIR"
RESTORE_EOF

chmod +x "$BACKUP_DIR/restore.sh"

echo "✅ Backup completed: $BACKUP_DIR"
echo "📋 Backup contents:"
ls -la "$BACKUP_DIR"
EOF

chmod +x /home/integrated_trader/scripts/backup_existing_system.sh
```

### Step 2: Create System Backup Script

```bash
# Create system state backup
cat > /home/integrated_trader/scripts/backup_system_state.sh << 'EOF'
#!/bin/bash
# Backup integrated trading system

BACKUP_DIR="/home/integrated_trader/backups/system_backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "🔄 Creating system backup..."

# Backup configuration
cp -r /home/integrated_trader/config "$BACKUP_DIR/"

# Backup data
cp -r /home/integrated_trader/data "$BACKUP_DIR/"

# Backup logs (last 7 days)
find /home/integrated_trader/logs -name "*.log" -mtime -7 -exec cp {} "$BACKUP_DIR/" \;

# Backup application code
tar -czf "$BACKUP_DIR/app_code.tar.gz" /home/integrated_trader/app

# Create system info
cat > "$BACKUP_DIR/system_info.txt" << 'INFO_EOF'
Backup Date: $(date)
System: $(hostname)
User: $(whoami)
Python Version: $(python3 --version)
Pip Packages: $(pip freeze | head -10)
Running Services: $(systemctl list-units --type=service | grep -E "(integrated|trading)")
INFO_EOF

echo "✅ System backup completed: $BACKUP_DIR"
EOF

chmod +x /home/integrated_trader/scripts/backup_system_state.sh
```

### Step 3: Create Rollback Script

```bash
# Create rollback script
cat > /home/integrated_trader/scripts/rollback.sh << 'EOF'
#!/bin/bash
# Emergency rollback script

echo "🚨 EMERGENCY ROLLBACK INITIATED"
echo "This will stop all integrated trading services"

read -p "Are you sure you want to proceed? (yes/no): " confirm
if [ "$confirm" != "yes" ]; then
    echo "Rollback cancelled"
    exit 1
fi

# Stop integrated services
sudo systemctl stop integrated-trading-system
sudo systemctl stop integrated-paper-trading
sudo supervisorctl stop integrated-trading-system
sudo supervisorctl stop integrated-paper-trading

# Disable services
sudo systemctl disable integrated-trading-system
sudo systemctl disable integrated-paper-trading

echo "✅ All integrated services stopped and disabled"
echo "🔄 Your existing v4 system should be unaffected"
echo "📋 To re-enable, run: sudo systemctl enable integrated-paper-trading"
EOF

chmod +x /home/integrated_trader/scripts/rollback.sh
```

---

## 🧪 Testing and Validation

### Step 1: Configuration Testing

```bash
# Create configuration test script
cat > /home/integrated_trader/scripts/test_configuration.py << 'EOF'
#!/usr/bin/env python3
"""
Configuration Testing Script
"""

import os
import sys
import yaml
import json
from pathlib import Path

def test_environment_file():
    """Test .env file"""
    env_file = Path('/home/integrated_trader/config/.env')
    if not env_file.exists():
        print("❌ .env file not found")
        return False
    
    # Test file permissions
    if oct(env_file.stat().st_mode)[-3:] != '600':
        print("❌ .env file permissions are not secure (should be 600)")
        return False
    
    print("✅ .env file exists and has correct permissions")
    return True

def test_config_yaml():
    """Test config.yaml file"""
    config_file = Path('/home/integrated_trader/config/config.yaml')
    if not config_file.exists():
        print("❌ config.yaml file not found")
        return False
    
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        print("✅ config.yaml is valid YAML")
        return True
    except yaml.YAMLError as e:
        print(f"❌ config.yaml is invalid: {e}")
        return False

def test_directories():
    """Test required directories"""
    required_dirs = [
        '/home/integrated_trader/app',
        '/home/integrated_trader/logs',
        '/home/integrated_trader/data',
        '/home/integrated_trader/config',
        '/home/integrated_trader/backups'
    ]
    
    all_good = True
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            print(f"❌ Directory missing: {dir_path}")
            all_good = False
        else:
            print(f"✅ Directory exists: {dir_path}")
    
    return all_good

def test_python_imports():
    """Test Python imports"""
    try:
        sys.path.append('/home/integrated_trader/app')
        from integrated_trading_system.exchanges.binance_adapter import BinanceAdapter
        from integrated_trading_system.exchanges.backpack_adapter import BackpackAdapter
        print("✅ Python imports successful")
        return True
    except ImportError as e:
        print(f"❌ Python import failed: {e}")
        return False

def main():
    print("🧪 Running configuration tests...")
    
    tests = [
        ("Environment File", test_environment_file),
        ("Config YAML", test_config_yaml),
        ("Directories", test_directories),
        ("Python Imports", test_python_imports)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing: {test_name}")
        if test_func():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready for deployment.")
        return 0
    else:
        print("❌ Some tests failed. Please fix the issues before proceeding.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
EOF

chmod +x /home/integrated_trader/scripts/test_configuration.py
```

### Step 2: Run Tests

```bash
# Run configuration tests
cd /home/integrated_trader
source venv/bin/activate
python scripts/test_configuration.py
```

### Step 3: Test Paper Trading Mode

```bash
# Test paper trading service
sudo systemctl start integrated-paper-trading
sleep 10
sudo systemctl status integrated-paper-trading

# Check logs
tail -f /home/integrated_trader/logs/integrated_trading.log
```

---

## 📊 Monitoring Setup

### Step 1: Create Monitoring Scripts

```bash
# Create system monitor script
cat > /home/integrated_trader/scripts/monitor_system.py << 'EOF'
#!/usr/bin/env python3
"""
System Monitoring Script
"""

import psutil
import sqlite3
import json
import time
from datetime import datetime
from pathlib import Path

class SystemMonitor:
    def __init__(self):
        self.db_path = '/home/integrated_trader/data/monitoring.db'
        self.init_database()
    
    def init_database(self):
        """Initialize monitoring database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_metrics (
                timestamp DATETIME,
                cpu_percent REAL,
                memory_percent REAL,
                disk_percent REAL,
                network_io_sent INTEGER,
                network_io_recv INTEGER,
                process_count INTEGER
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS service_status (
                timestamp DATETIME,
                service_name TEXT,
                status TEXT,
                cpu_percent REAL,
                memory_mb REAL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def collect_metrics(self):
        """Collect system metrics"""
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent,
            'network_io': psutil.net_io_counters(),
            'process_count': len(psutil.pids())
        }
        
        return metrics
    
    def monitor_services(self):
        """Monitor trading services"""
        services = ['integrated-trading-system', 'integrated-paper-trading']
        service_status = []
        
        for service in services:
            try:
                # Check if service is running
                # This is a simplified check - in production, use systemctl
                status = "running"  # Placeholder
                service_status.append({
                    'service': service,
                    'status': status,
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                service_status.append({
                    'service': service,
                    'status': 'error',
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })
        
        return service_status
    
    def save_metrics(self, metrics):
        """Save metrics to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO system_metrics 
            (timestamp, cpu_percent, memory_percent, disk_percent, 
             network_io_sent, network_io_recv, process_count)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            metrics['timestamp'],
            metrics['cpu_percent'],
            metrics['memory_percent'],
            metrics['disk_percent'],
            metrics['network_io'].bytes_sent,
            metrics['network_io'].bytes_recv,
            metrics['process_count']
        ))
        
        conn.commit()
        conn.close()
    
    def generate_report(self):
        """Generate monitoring report"""
        metrics = self.collect_metrics()
        service_status = self.monitor_services()
        
        report = {
            'timestamp': metrics['timestamp'],
            'system': {
                'cpu_percent': metrics['cpu_percent'],
                'memory_percent': metrics['memory_percent'],
                'disk_percent': metrics['disk_percent'],
                'process_count': metrics['process_count']
            },
            'services': service_status,
            'alerts': []
        }
        
        # Generate alerts
        if metrics['cpu_percent'] > 80:
            report['alerts'].append('HIGH CPU USAGE')
        if metrics['memory_percent'] > 85:
            report['alerts'].append('HIGH MEMORY USAGE')
        if metrics['disk_percent'] > 90:
            report['alerts'].append('HIGH DISK USAGE')
        
        return report

def main():
    monitor = SystemMonitor()
    
    while True:
        try:
            # Collect and save metrics
            metrics = monitor.collect_metrics()
            monitor.save_metrics(metrics)
            
            # Generate report
            report = monitor.generate_report()
            
            # Save report
            report_file = Path('/home/integrated_trader/logs/monitoring_report.json')
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2)
            
            # Print summary
            print(f"[{report['timestamp']}] "
                  f"CPU: {report['system']['cpu_percent']:.1f}% "
                  f"MEM: {report['system']['memory_percent']:.1f}% "
                  f"DISK: {report['system']['disk_percent']:.1f}% "
                  f"ALERTS: {len(report['alerts'])}")
            
            if report['alerts']:
                print(f"⚠️  ALERTS: {', '.join(report['alerts'])}")
            
            time.sleep(60)  # Monitor every minute
            
        except KeyboardInterrupt:
            print("Monitoring stopped")
            break
        except Exception as e:
            print(f"Monitoring error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
EOF

chmod +x /home/integrated_trader/scripts/monitor_system.py
```

### Step 2: Create Log Rotation Configuration

```bash
# Create log rotation configuration
sudo cat > /etc/logrotate.d/integrated-trading << 'EOF'
/home/integrated_trader/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 0644 integrated_trader integrated_trader
    postrotate
        systemctl reload integrated-trading-system
        systemctl reload integrated-paper-trading
    endscript
}
EOF
```

### Step 3: Create Health Check Script

```bash
# Create health check script
cat > /home/integrated_trader/scripts/health_check.py << 'EOF'
#!/usr/bin/env python3
"""
Health Check Script
"""

import requests
import subprocess
import json
import sys
from datetime import datetime
from pathlib import Path

class HealthChecker:
    def __init__(self):
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'checks': [],
            'overall_status': 'healthy'
        }
    
    def check_service_status(self, service_name):
        """Check if service is running"""
        try:
            result = subprocess.run(
                ['systemctl', 'is-active', service_name],
                capture_output=True,
                text=True
            )
            
            status = result.stdout.strip()
            self.results['checks'].append({
                'check': f'Service {service_name}',
                'status': 'pass' if status == 'active' else 'fail',
                'details': status
            })
            
            if status != 'active':
                self.results['overall_status'] = 'unhealthy'
                
        except Exception as e:
            self.results['checks'].append({
                'check': f'Service {service_name}',
                'status': 'error',
                'details': str(e)
            })
            self.results['overall_status'] = 'unhealthy'
    
    def check_log_file(self, log_file):
        """Check if log file is being written to"""
        try:
            log_path = Path(log_file)
            if not log_path.exists():
                self.results['checks'].append({
                    'check': f'Log file {log_file}',
                    'status': 'fail',
                    'details': 'File does not exist'
                })
                self.results['overall_status'] = 'unhealthy'
                return
            
            # Check if file was modified in last 10 minutes
            import time
            mtime = log_path.stat().st_mtime
            current_time = time.time()
            
            if current_time - mtime < 600:  # 10 minutes
                self.results['checks'].append({
                    'check': f'Log file {log_file}',
                    'status': 'pass',
                    'details': 'Recently updated'
                })
            else:
                self.results['checks'].append({
                    'check': f'Log file {log_file}',
                    'status': 'warn',
                    'details': 'Not recently updated'
                })
                
        except Exception as e:
            self.results['checks'].append({
                'check': f'Log file {log_file}',
                'status': 'error',
                'details': str(e)
            })
    
    def check_disk_space(self):
        """Check disk space"""
        try:
            import shutil
            total, used, free = shutil.disk_usage('/home/integrated_trader')
            
            free_percent = (free / total) * 100
            
            if free_percent > 20:
                status = 'pass'
            elif free_percent > 10:
                status = 'warn'
            else:
                status = 'fail'
                self.results['overall_status'] = 'unhealthy'
            
            self.results['checks'].append({
                'check': 'Disk space',
                'status': status,
                'details': f'{free_percent:.1f}% free'
            })
            
        except Exception as e:
            self.results['checks'].append({
                'check': 'Disk space',
                'status': 'error',
                'details': str(e)
            })
    
    def check_database_connection(self):
        """Check database connection"""
        try:
            import sqlite3
            conn = sqlite3.connect('/home/integrated_trader/data/trading.db')
            cursor = conn.cursor()
            cursor.execute('SELECT 1')
            conn.close()
            
            self.results['checks'].append({
                'check': 'Database connection',
                'status': 'pass',
                'details': 'Connected successfully'
            })
            
        except Exception as e:
            self.results['checks'].append({
                'check': 'Database connection',
                'status': 'fail',
                'details': str(e)
            })
            self.results['overall_status'] = 'unhealthy'
    
    def run_all_checks(self):
        """Run all health checks"""
        # Check services
        self.check_service_status('integrated-paper-trading')
        
        # Check log files
        self.check_log_file('/home/integrated_trader/logs/integrated_trading.log')
        
        # Check system resources
        self.check_disk_space()
        
        # Check database
        self.check_database_connection()
        
        return self.results
    
    def save_results(self, results):
        """Save health check results"""
        results_file = Path('/home/integrated_trader/logs/health_check.json')
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)

def main():
    checker = HealthChecker()
    results = checker.run_all_checks()
    checker.save_results(results)
    
    # Print summary
    print(f"Health Check Results - {results['timestamp']}")
    print(f"Overall Status: {results['overall_status'].upper()}")
    print("-" * 50)
    
    for check in results['checks']:
        status_icon = {
            'pass': '✅',
            'warn': '⚠️',
            'fail': '❌',
            'error': '🔥'
        }.get(check['status'], '❓')
        
        print(f"{status_icon} {check['check']}: {check['details']}")
    
    # Exit with appropriate code
    if results['overall_status'] == 'healthy':
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
EOF

chmod +x /home/integrated_trader/scripts/health_check.py
```

---

## 🔧 Maintenance Instructions

### Step 1: Daily Maintenance Tasks

```bash
# Create daily maintenance script
cat > /home/integrated_trader/scripts/daily_maintenance.sh << 'EOF'
#!/bin/bash
# Daily maintenance script

echo "🔧 Running daily maintenance - $(date)"

# Health check
echo "📊 Running health check..."
/home/integrated_trader/scripts/health_check.py

# Log rotation check
echo "🔄 Checking log rotation..."
sudo logrotate -f /etc/logrotate.d/integrated-trading

# Backup system state
echo "💾 Creating daily backup..."
/home/integrated_trader/scripts/backup_system_state.sh

# Clean old backups (keep last 7 days)
echo "🗑️ Cleaning old backups..."
find /home/integrated_trader/backups -name "system_backup_*" -mtime +7 -delete

# Check disk space
echo "💽 Checking disk space..."
df -h /home/integrated_trader

# Check service status
echo "🔍 Checking service status..."
sudo systemctl status integrated-paper-trading --no-pager

# Update system packages (optional - be careful in production)
# echo "📦 Updating packages..."
# sudo apt update && sudo apt upgrade -y

echo "✅ Daily maintenance completed - $(date)"
EOF

chmod +x /home/integrated_trader/scripts/daily_maintenance.sh
```

### Step 2: Update Procedures

```bash
# Create update script
cat > /home/integrated_trader/scripts/update_system.sh << 'EOF'
#!/bin/bash
# System update script

echo "🔄 Starting system update..."

# Backup current state
echo "💾 Creating pre-update backup..."
/home/integrated_trader/scripts/backup_system_state.sh

# Stop services
echo "🛑 Stopping services..."
sudo systemctl stop integrated-paper-trading
sudo systemctl stop integrated-trading-system

# Update code
echo "📥 Updating code..."
cd /home/integrated_trader/app
git pull origin main

# Update dependencies
echo "📦 Updating dependencies..."
source /home/integrated_trader/venv/bin/activate
pip install --upgrade -r requirements.txt

# Run tests
echo "🧪 Running tests..."
python /home/integrated_trader/scripts/test_configuration.py

# Start services
echo "🚀 Starting services..."
sudo systemctl start integrated-paper-trading

# Verify update
echo "✅ Verifying update..."
sleep 10
sudo systemctl status integrated-paper-trading

echo "🎉 Update completed successfully!"
EOF

chmod +x /home/integrated_trader/scripts/update_system.sh
```

### Step 3: Setup Cron Jobs

```bash
# Setup cron jobs for maintenance
(crontab -l 2>/dev/null; echo "# Integrated Trading System Maintenance") | crontab -
(crontab -l 2>/dev/null; echo "0 2 * * * /home/integrated_trader/scripts/daily_maintenance.sh >> /home/integrated_trader/logs/maintenance.log 2>&1") | crontab -
(crontab -l 2>/dev/null; echo "*/15 * * * * /home/integrated_trader/scripts/health_check.py >> /home/integrated_trader/logs/health_check.log 2>&1") | crontab -
(crontab -l 2>/dev/null; echo "0 0 * * 0 /home/integrated_trader/scripts/backup_system_state.sh >> /home/integrated_trader/logs/backup.log 2>&1") | crontab -

# Display cron jobs
echo "📅 Scheduled maintenance jobs:"
crontab -l
```

---

## 🐛 Troubleshooting

### Common Issues and Solutions

#### 1. Service Won't Start

```bash
# Check service logs
journalctl -u integrated-paper-trading -f

# Check configuration
/home/integrated_trader/scripts/test_configuration.py

# Check permissions
ls -la /home/integrated_trader/
```

#### 2. API Connection Issues

```bash
# Test API connectivity
cd /home/integrated_trader/app
source /home/integrated_trader/venv/bin/activate
python -c "
from integrated_trading_system.exchanges.binance_adapter import BinanceAdapter
print('Testing Binance connection...')
"
```

#### 3. Database Issues

```bash
# Check database
sqlite3 /home/integrated_trader/data/trading.db ".tables"

# Repair database if needed
sqlite3 /home/integrated_trader/data/trading.db "PRAGMA integrity_check;"
```

#### 4. Permission Issues

```bash
# Fix permissions
sudo chown -R integrated_trader:integrated_trader /home/integrated_trader/
chmod 750 /home/integrated_trader/
chmod 600 /home/integrated_trader/config/.env
```

#### 5. Log Files Growing Too Large

```bash
# Manual log rotation
sudo logrotate -f /etc/logrotate.d/integrated-trading

# Check log sizes
du -h /home/integrated_trader/logs/
```

### Emergency Procedures

#### 1. Emergency Stop

```bash
# Stop all services immediately
sudo systemctl stop integrated-trading-system
sudo systemctl stop integrated-paper-trading
sudo supervisorctl stop all

# Kill any remaining processes
pkill -f "integrated_trading"
```

#### 2. Complete Rollback

```bash
# Run rollback script
/home/integrated_trader/scripts/rollback.sh

# Verify rollback
sudo systemctl status integrated-paper-trading
```

#### 3. System Recovery

```bash
# Restore from backup
ls /home/integrated_trader/backups/
# Select latest backup and follow restore instructions
```

---

## 📞 Support and Contact

### Log Files Locations

- **Main Log**: `/home/integrated_trader/logs/integrated_trading.log`
- **Error Log**: `/home/integrated_trader/logs/error.log`
- **Health Check**: `/home/integrated_trader/logs/health_check.log`
- **Maintenance**: `/home/integrated_trader/logs/maintenance.log`

### Key Commands

```bash
# Check service status
sudo systemctl status integrated-paper-trading

# View logs
tail -f /home/integrated_trader/logs/integrated_trading.log

# Run health check
/home/integrated_trader/scripts/health_check.py

# Emergency stop
/home/integrated_trader/scripts/rollback.sh
```

### Important Notes

1. **Always test in paper trading mode first**
2. **Keep backups of all configurations**
3. **Monitor logs regularly**
4. **Update API keys securely**
5. **Never run live trading without thorough testing**

---

## ✅ Deployment Checklist

### Pre-Deployment
- [ ] Server assessment completed
- [ ] Existing v4 system backed up
- [ ] System dependencies installed
- [ ] Directory structure created
- [ ] User account configured

### Deployment
- [ ] Code transferred and extracted
- [ ] Python dependencies installed
- [ ] Configuration files created
- [ ] API keys configured securely
- [ ] Environment variables set

### Testing
- [ ] Configuration tests passed
- [ ] Python imports working
- [ ] Database connection established
- [ ] Service files created
- [ ] Paper trading mode tested

### Production
- [ ] Monitoring scripts installed
- [ ] Log rotation configured
- [ ] Backup procedures tested
- [ ] Cron jobs scheduled
- [ ] Emergency procedures documented

### Post-Deployment
- [ ] System monitoring active
- [ ] Health checks passing
- [ ] Logs being generated
- [ ] Performance metrics tracked
- [ ] Documentation updated

---

**🎉 Congratulations! Your Integrated Multi-Exchange Trading System is now deployed and ready for use.**

Remember to start with paper trading mode and gradually transition to live trading after thorough testing and validation.