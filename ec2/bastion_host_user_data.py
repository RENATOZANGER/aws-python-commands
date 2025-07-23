#!/bin/bash
yum update -y # Update system packages
yum install nc -y # Install Netcat, used for port forwarding

# Create the systemd service directly
echo '[Unit]
Description=Bastion Host Port Forwarding Service
After=network.target # Ensures the service starts after the network is fully functional

[Service]
# Executes the nc commands. "sh -c" allows multiple commands in one line.
# "wait" is crucial for systemd to monitor these background processes.
ExecStart=/bin/sh -c "/usr/bin/nc -K -l -p 9090 -c \"/usr/bin/nc endpoint_aurora 8035\" & /usr/bin/nc -K -l -p 9091 -c \"/usr/bin/nc endpoint_redis 6106\" & wait"
Restart=always # Automatically restarts the service in case of failure
RestartSec=5 # Waits 5 seconds before attempting to restart
Type=simple # Service type, default. 'wait' is important here.
StandardOutput=journal # Redirects standard output to journalctl (for logs)
StandardError=journal  # Redirects errors to journalctl (for logs)

[Install]
WantedBy=multi-user.target' > /etc/systemd/system/bastion.service

systemctl daemon-reload    # Reload systemd configurations
systemctl enable bastion.service # Enable the service to start on boot
systemctl start bastion.service  # Start the service immediately
