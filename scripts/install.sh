#!/bin/sh

# Check for binaries
echo "Checking for required binaries..."
for cmd in python3 git nginx systemctl; do
    command -v $cmd >/dev/null 2>&1 || { echo >&2 "$cmd not found."; exit 1; }
done

# check for required python modules
command -v "python3 -m pip" >/dev/null 2>&1 || { echo >&2 "python3 -m pip not found. Please install python3-pip."; exit 1; }
command -v "python3 -m venv" >/dev/null 2>&1 || { echo >&2 "python3 -m venv not found. Please install python3-venv."; exit 1; }

# check for nginx service
systemctl is-active --quiet nginx || { echo "nginx service is not active. Please start the service before running this script."; exit 1; }

# use environment variable instead of user input to allow piping
SERVER_NAME=${SCUOLASYNC_SERVER_NAME:-""}
SKIP_DOWNLOAD=${SCUOLASYNC_NO_DOWNLOAD:-""}
DISABLE_SSL=${SCUOLASYNC_NO_SSL:-""}


if [ -z "$SERVER_NAME" ]; then
    echo "Server name cannot be empty. Set the environment variable SCUOLASYNC_SERVER_NAME."
    exit 1
fi

# Ensure Python version is adequate
PYTHON_VERSION=$(python3 -c "import sys; print('.'.join(map(str, sys.version_info[:2])))")
REQUIRED_VERSION="3.10"
if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "Python 3.10 or higher is required. Found: $PYTHON_VERSION"
    exit 1
fi
# todo: check for python-venv


if [ -z "$SKIP_DOWNLOAD" ]; then
    # Clone the repository
    if [ -d "scuolasync" ]; then
        echo "Directory 'scuolasync' already exists. Remove or rename it before running the script."
        exit 1
    fi

    echo "Cloning the repository..."
    git clone https://github.com/nkoexe/scuolasync.git || { echo "Cloning repository failed."; exit 1; }

    # Set up the virtual environment
    cd scuolasync || { echo "Directory 'scuolasync' not found."; exit 1; }
    echo "Setting up the virtual environment..."
    python3 -m venv env || { echo "Virtual environment creation failed."; exit 1; }

    # Activate the virtual environment
    if [ -f "env/bin/activate" ]; then
        . env/bin/activate
    else
        echo "Virtual environment activation script not found."
        exit 1
    fi

    # Install the dependencies
    echo "Installing dependencies..."
    python3 -m pip install -r requirements.txt --log pip-install.log || { echo "Dependency installation failed. Check pip-install.log for details."; exit 1; }

else
    echo "Skipping download. Please make sure you're inside the repository directory."
fi

# Define the Nginx configuration file content
NGINX_CONF='
server {
        server_name '"$SERVER_NAME"';

        location / {
                include proxy_params;
                proxy_pass http://127.0.0.1:5123/;
                proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto \$scheme;
                proxy_set_header X-Forwarded-Host \$host;
        }

        location /socket.io {
                include proxy_params;
                proxy_http_version 1.1;
                proxy_buffering off;
                proxy_set_header Upgrade \$http_upgrade;
                proxy_set_header Connection \"Upgrade\";
                proxy_pass http://127.0.0.1:5123/socket.io;
        }
}
'

# Save the configuration to the Nginx directory
NGINX_CONF_PATH="/etc/nginx/conf.d/scuolasync.conf"

sudo mkdir -p /etc/nginx/conf.d

echo "Installing Nginx configuration..."
sudo sh -c "echo \"$NGINX_CONF\" > $NGINX_CONF_PATH" || { echo "Failed to write Nginx configuration."; exit 1; }


# Test the Nginx configuration
echo "Testing Nginx configuration..."
sudo nginx -t || { echo "Nginx configuration test failed. Check the configuration and try again."; exit 1; }

# Reload Nginx to apply changes
echo "Reloading Nginx..."
sudo systemctl reload nginx || { echo "Failed to reload Nginx."; exit 1; }

echo "Nginx configuration installed successfully for server name: $SERVER_NAME"

# Disable ssl is not set, proceed with obtaining SSL certificate
if [ -z "$DISABLE_SSL" ]; then
    echo "Obtaining SSL certificate for $SERVER_NAME..."
    command -v certbot >/dev/null 2>&1 || { echo "Certbot is not installed. Please install it before enabling SSL."; exit 1; }

    # Ensure ports 80 and 443 are open
    echo "Checking if UFW is installed to manage ports..."
    if command -v ufw >/dev/null 2>&1; then
        echo "Allowing HTTP and HTTPS traffic through UFW..."
        sudo ufw allow 80/tcp
        sudo ufw allow 443/tcp
    fi

    # Obtain the SSL certificate with certbot
    sudo certbot --nginx -d "$SERVER_NAME" || { echo "Certbot failed to obtain an SSL certificate."; exit 1; }

    # Test and reload Nginx after SSL configuration
    echo "Testing Nginx configuration with SSL..."
    sudo nginx -t || { echo "Nginx configuration test failed after SSL setup. Check the configuration and try again."; exit 1; }

    echo "Reloading Nginx with SSL configuration..."
    sudo systemctl reload nginx || { echo "Failed to reload Nginx with SSL."; exit 1; }

    echo "SSL has been enabled for $SERVER_NAME."
else
    echo "SSL setup skipped. You can run 'certbot --nginx' later to add SSL."
fi

echo "Nginx configuration process completed."


# SYSTEMCTL

# Define variables
REPO_PATH=$(pwd)  # Use current directory as the repo path
VENV_PATH="$REPO_PATH/env"  # Adjust this if your virtual environment path differs
SERVICE_NAME="scuolasync.service"
TARGET_DIR="$HOME/.config/systemd/user"

mkdir -p "$TARGET_DIR"

# Generate the service file dynamically
SERVICE_FILE="$TARGET_DIR/$SERVICE_NAME"
cat <<EOF >"$SERVICE_FILE"
[Unit]
Description=ScuolaSync - Server
After=network.target

[Service]
WorkingDirectory=$REPO_PATH
Environment=PATH=$VENV_PATH/bin:/usr/bin
ExecStart=$VENV_PATH/bin/gunicorn --workers 1 -k gevent --bind 127.0.0.1:5123 sostituzioni.app:app
Restart=always

[Install]
WantedBy=default.target
EOF

echo "Installing service..."
systemctl --user daemon-reload || { echo "Failed to reload systemctl daemon."; exit 1; }
systemctl --user enable "$SERVICE_NAME" || { echo "Failed to enable service."; exit 1; }
systemctl --user start "$SERVICE_NAME" || { echo "Failed to start service."; exit 1; }

echo "Service installed successfully."

echo "Installation completed successfully."

echo ""
if [ -z "$DISABLE_SSL" ]; then
    echo "Head to https://$SERVER_NAME to set up the system."
else
    echo "Head to http://$SERVER_NAME to set up the system."
fi
