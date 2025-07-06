#!/bin/bash
# Automated Deployment Script for Integrated Multi-Exchange Trading System
# Version: 1.0.0
# Author: Integrated Trading System Team

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DEPLOY_USER="integrated_trader"
DEPLOY_HOME="/home/${DEPLOY_USER}"
APP_DIR="${DEPLOY_HOME}/app"
BACKUP_DIR="${DEPLOY_HOME}/backups"
LOG_FILE="/tmp/deployment.log"

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1" | tee -a "$LOG_FILE"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1" | tee -a "$LOG_FILE"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
}

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================${NC}"
}

# Check if running as root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        print_error "This script must be run as root"
        exit 1
    fi
}

# Backup existing system
backup_existing_system() {
    print_header "BACKING UP EXISTING SYSTEM"
    
    local backup_timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_path="${BACKUP_DIR}/pre_deployment_backup_${backup_timestamp}"
    
    print_status "Creating backup directory: $backup_path"
    mkdir -p "$backup_path"
    
    # Backup existing bot directories
    print_status "Searching for existing bot installations..."
    for dir in $(find /home /opt /root -name "*bot*" -type d 2>/dev/null | head -10); do
        if [ -d "$dir" ]; then
            print_status "Backing up: $dir"
            cp -r "$dir" "$backup_path/" 2>/dev/null || print_warning "Failed to backup $dir"
        fi
    done
    
    # Backup existing services
    print_status "Backing up existing services..."
    mkdir -p "$backup_path/services"
    for service in $(systemctl list-units --type=service | grep -E "(bot|trading)" | awk '{print $1}' | head -10); do
        if [ -n "$service" ]; then
            systemctl show "$service" > "$backup_path/services/${service}.conf" 2>/dev/null || true
        fi
    done
    
    # Backup crontab
    print_status "Backing up crontab..."
    crontab -l > "$backup_path/crontab.txt" 2>/dev/null || echo "No crontab found"
    
    print_status "Backup completed: $backup_path"
}

# Install system dependencies
install_dependencies() {
    print_header "INSTALLING SYSTEM DEPENDENCIES"
    
    print_status "Updating package lists..."
    apt update
    
    print_status "Installing required packages..."
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
        logrotate \
        build-essential \
        libssl-dev \
        libffi-dev \
        python3-setuptools
    
    print_status "System dependencies installed successfully"
}

# Create user and directories
setup_user_environment() {
    print_header "SETTING UP USER ENVIRONMENT"
    
    # Create user if doesn't exist
    if ! id "$DEPLOY_USER" &>/dev/null; then
        print_status "Creating user: $DEPLOY_USER"
        useradd -m -s /bin/bash "$DEPLOY_USER"
        usermod -aG sudo "$DEPLOY_USER"
    else
        print_status "User $DEPLOY_USER already exists"
    fi
    
    # Create directory structure
    print_status "Creating directory structure..."
    sudo -u "$DEPLOY_USER" mkdir -p "$DEPLOY_HOME"/{app,logs,config,data,backups,scripts,monitoring}
    
    # Set proper permissions
    chown -R "$DEPLOY_USER:$DEPLOY_USER" "$DEPLOY_HOME"
    chmod 750 "$DEPLOY_HOME"
    
    print_status "User environment setup completed"
}

# Setup Python environment
setup_python_environment() {
    print_header "SETTING UP PYTHON ENVIRONMENT"
    
    # Create virtual environment
    print_status "Creating Python virtual environment..."
    sudo -u "$DEPLOY_USER" python3 -m venv "$DEPLOY_HOME/venv"
    
    # Activate and upgrade pip
    print_status "Upgrading pip..."
    sudo -u "$DEPLOY_USER" bash -c "source $DEPLOY_HOME/venv/bin/activate && pip install --upgrade pip setuptools wheel"
    
    print_status "Python environment setup completed"
}

# Deploy application code
deploy_application() {
    print_header "DEPLOYING APPLICATION CODE"
    
    if [ ! -f "integrated_system_deployment.tar.gz" ]; then
        print_error "Deployment package not found: integrated_system_deployment.tar.gz"
        print_error "Please create the deployment package first"
        exit 1
    fi
    
    print_status "Extracting application code..."
    sudo -u "$DEPLOY_USER" tar -xzf integrated_system_deployment.tar.gz -C "$APP_DIR"
    
    # Install Python dependencies
    print_status "Installing Python dependencies..."
    sudo -u "$DEPLOY_USER" bash -c "
        source $DEPLOY_HOME/venv/bin/activate
        cd $APP_DIR
        pip install -r requirements.txt
        pip install aiohttp websockets python-binance asyncio pandas numpy scipy matplotlib seaborn requests cryptography python-dotenv sqlalchemy psutil click rich tabulate
    "
    
    print_status "Application deployment completed"
}

# Configure environment
configure_environment() {
    print_header "CONFIGURING ENVIRONMENT"
    
    # Create .env file
    print_status "Creating environment configuration..."
    sudo -u "$DEPLOY_USER" cat > "$DEPLOY_HOME/config/.env" << 'EOF'
# Integrated Multi-Exchange Trading System Configuration
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
LOG_FILE=/home/integrated_trader/logs/integrated_trading.log

# Database Configuration
DATABASE_URL=sqlite:///home/integrated_trader/data/trading.db

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

# Performance
EXECUTION_INTERVAL=1.0
DATA_FETCH_INTERVAL=5.0
HEARTBEAT_INTERVAL=30.0

# API Keys (TO BE CONFIGURED MANUALLY)
BINANCE_API_KEY=your_binance_api_key_here
BINANCE_API_SECRET=your_binance_api_secret_here
BINANCE_TESTNET=true

BACKPACK_API_KEY=your_backpack_api_key_here
BACKPACK_API_SECRET=your_backpack_api_secret_here
BACKPACK_TESTNET=true
EOF
    
    # Secure the environment file
    chmod 600 "$DEPLOY_HOME/config/.env"
    
    # Create config.yaml
    print_status "Creating YAML configuration..."
    sudo -u "$DEPLOY_USER" cat > "$DEPLOY_HOME/config/config.yaml" << 'EOF'
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
    testnet: true
    rate_limit: 1200
    order_types: ["LIMIT", "MARKET", "STOP_LOSS", "TAKE_PROFIT"]
    
  backpack:
    enabled: true
    testnet: true
    rate_limit: 600
    order_types: ["LIMIT", "MARKET"]

trading:
  mode: "paper"
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
  min_profit_threshold: 0.001
  max_execution_time: 30
  confidence_threshold: 0.7
  
monitoring:
  heartbeat_interval: 30.0
  health_check_interval: 60.0
  performance_report_interval: 3600.0
EOF
    
    print_status "Environment configuration completed"
}

# Create systemd services
create_services() {
    print_header "CREATING SYSTEMD SERVICES"
    
    # Create paper trading service
    print_status "Creating paper trading service..."
    cat > /etc/systemd/system/integrated-paper-trading.service << 'EOF'
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
    
    # Create main trading service (disabled by default)
    print_status "Creating main trading service..."
    cat > /etc/systemd/system/integrated-trading-system.service << 'EOF'
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
    
    # Reload systemd
    systemctl daemon-reload
    
    print_status "SystemD services created successfully"
}

# Setup monitoring
setup_monitoring() {
    print_header "SETTING UP MONITORING"
    
    # Create log rotation
    print_status "Creating log rotation configuration..."
    cat > /etc/logrotate.d/integrated-trading << 'EOF'
/home/integrated_trader/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 0644 integrated_trader integrated_trader
    postrotate
        systemctl reload integrated-trading-system 2>/dev/null || true
        systemctl reload integrated-paper-trading 2>/dev/null || true
    endscript
}
EOF
    
    # Create monitoring scripts directory
    print_status "Creating monitoring scripts..."
    sudo -u "$DEPLOY_USER" mkdir -p "$DEPLOY_HOME/scripts"
    
    # Copy monitoring scripts from deployment package
    # (These would be included in the deployment package)
    
    print_status "Monitoring setup completed"
}

# Test deployment
test_deployment() {
    print_header "TESTING DEPLOYMENT"
    
    # Test Python imports
    print_status "Testing Python imports..."
    sudo -u "$DEPLOY_USER" bash -c "
        source $DEPLOY_HOME/venv/bin/activate
        cd $APP_DIR
        python3 -c 'import sys; sys.path.append(\".\"); from integrated_trading_system.exchanges.binance_adapter import BinanceAdapter; print(\"✅ Binance adapter import successful\")'
    " || print_error "Python imports failed"
    
    # Test configuration
    print_status "Testing configuration files..."
    if [ -f "$DEPLOY_HOME/config/.env" ]; then
        print_status "✅ .env file exists"
    else
        print_error "❌ .env file missing"
    fi
    
    if [ -f "$DEPLOY_HOME/config/config.yaml" ]; then
        print_status "✅ config.yaml file exists"
    else
        print_error "❌ config.yaml file missing"
    fi
    
    # Test service files
    print_status "Testing service files..."
    if [ -f "/etc/systemd/system/integrated-paper-trading.service" ]; then
        print_status "✅ Paper trading service file exists"
    else
        print_error "❌ Paper trading service file missing"
    fi
    
    print_status "Deployment testing completed"
}

# Main deployment function
main() {
    print_header "INTEGRATED MULTI-EXCHANGE TRADING SYSTEM DEPLOYMENT"
    echo "Starting deployment at $(date)" | tee "$LOG_FILE"
    
    # Check prerequisites
    check_root
    
    # Run deployment steps
    backup_existing_system
    install_dependencies
    setup_user_environment
    setup_python_environment
    deploy_application
    configure_environment
    create_services
    setup_monitoring
    test_deployment
    
    print_header "DEPLOYMENT COMPLETED SUCCESSFULLY"
    echo ""
    print_status "🎉 Deployment completed successfully!"
    echo ""
    print_status "Next steps:"
    echo "1. Configure API keys in: $DEPLOY_HOME/config/.env"
    echo "2. Start paper trading service: sudo systemctl start integrated-paper-trading"
    echo "3. Check service status: sudo systemctl status integrated-paper-trading"
    echo "4. View logs: tail -f $DEPLOY_HOME/logs/integrated_trading.log"
    echo ""
    print_warning "⚠️  Remember to:"
    echo "   - Configure your API keys before starting services"
    echo "   - Test thoroughly in paper trading mode"
    echo "   - Monitor logs for any issues"
    echo "   - Keep backups of your configuration"
    echo ""
    print_status "Deployment log saved to: $LOG_FILE"
    echo ""
    print_header "DEPLOYMENT SUMMARY"
    echo "User: $DEPLOY_USER"
    echo "Home: $DEPLOY_HOME"
    echo "App: $APP_DIR"
    echo "Config: $DEPLOY_HOME/config"
    echo "Logs: $DEPLOY_HOME/logs"
    echo "Service: integrated-paper-trading"
    echo ""
}

# Help function
show_help() {
    echo "Integrated Multi-Exchange Trading System Deployment Script"
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  -v, --version  Show version information"
    echo ""
    echo "Prerequisites:"
    echo "  - Run as root"
    echo "  - Have integrated_system_deployment.tar.gz in current directory"
    echo "  - Ubuntu/Debian system with apt package manager"
    echo ""
    echo "Example:"
    echo "  sudo $0"
    echo ""
}

# Parse command line arguments
case "${1:-}" in
    -h|--help)
        show_help
        exit 0
        ;;
    -v|--version)
        echo "Integrated Multi-Exchange Trading System Deployment Script v1.0.0"
        exit 0
        ;;
    *)
        main "$@"
        ;;
esac