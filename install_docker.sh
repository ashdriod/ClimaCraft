#!/bin/bash

# Update the apt package index and install packages to allow apt to use a repository over HTTPS:
sudo apt-get update
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common \
    gnupg-agent -y

# Add Docker’s official GPG key:
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Verify that you now have the key with the fingerprint
# 9DC8 5822 9FC7 DD38 854A E2D8 8D81 803C 0EBF CD88, by searching for the last 8 characters of the fingerprint.
sudo apt-key fingerprint 0EBFCD88

# Set up the stable repository:
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

# Update the apt package index:
sudo apt-get update

# Install the latest version of Docker Engine and containerd:
sudo apt-get install docker-ce docker-ce-cli containerd.io -y

# Post-installation steps to manage Docker as a non-root user
sudo groupadd docker
sudo usermod -aG docker $USER

# Echo a completion message
echo "Docker installation completed successfully!"
