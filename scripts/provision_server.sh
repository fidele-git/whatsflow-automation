#!/bin/bash
# Server Provisioning Script for WhatsFlow Automation
# Runs on Ubuntu 20.04/22.04

set -e

echo "=== WhatsFlow Server Provisioning ==="

# 1. Update System
echo "[1/6] Updating system packages..."
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y curl git ufw

# 2. Install Docker & Docker Compose
echo "[2/6] Installing Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
    echo "Docker installed successfully."
else
    echo "Docker already installed."
fi

if ! command -v docker-compose &> /dev/null; then
    sudo apt-get install -y docker-compose-plugin
    echo "Docker Compose installed."
fi

# 3. Setup Firewall
echo "[3/6] Configuring firewall..."
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable

# 4. Clone Repository
echo "[4/6] Setting up application..."
APP_DIR="/home/$USER/whatsflow-automation"

if [ -d "$APP_DIR" ]; then
    echo "Directory exists. Pulling latest changes..."
    cd $APP_DIR
    git pull
else
    echo "Cloning repository..."
    # Note: This requires a token or SSH key to be set up beforehand
    # We'll ask for a token if cloning fails
    if ! git clone https://github.com/fidele-git/whatsflow-automation.git $APP_DIR; then
        echo "Error: Could not clone private repository."
        echo "Please enter your GitHub Personal Access Token (classic) with 'repo' scope:"
        read -s GITHUB_TOKEN
        git clone https://$USER:$GITHUB_TOKEN@github.com/fidele-git/whatsflow-automation.git $APP_DIR
    fi
fi

cd $APP_DIR

# 5. Environment Setup
echo "[5/6] Setting up environment..."
if [ ! -f .env ]; then
    echo "Creating .env file from example..."
    cp .env.example .env
    
    # Generate secure secret key
    SECRET=$(python3 -c "import secrets; print(secrets.token_hex(32))")
    sed -i "s/your-secret-key-here-change-in-production/$SECRET/" .env
    
    echo "IMPORTANT: Please edit .env to configure your email and database settings."
fi

# 6. Start Application
echo "[6/6] Starting application..."
echo "Login to GitHub Container Registry to pull images..."
echo "Enter your GitHub Username:"
read GH_USER
echo "Enter your GitHub Personal Access Token (read:packages scope):"
read -s GH_TOKEN
echo $GH_TOKEN | docker login ghcr.io -u $GH_USER --password-stdin

echo "Pulling latest images..."
docker compose pull
docker compose up -d

echo "=== Provisioning Complete! ==="
echo "Your application should be running on http://$(curl -s ifconfig.me)"
echo "Next steps:"
echo "1. Edit .env file with your email credentials"
echo "2. Run: docker compose exec web python init_pricing.py"
echo "3. Run: docker compose exec web python scripts/create_admin.py"
