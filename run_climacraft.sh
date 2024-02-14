#!/bin/bash

# Ensure X11 forwarding is enabled for Docker
xhost +local:docker

# Directory on your host where you want to save the PDF
HOST_PDF_DIR="$HOME/Downloads"

# Ensure the host directory exists
mkdir -p "$HOST_PDF_DIR"

# Run the Docker container with GUI support
CONTAINER_ID=$(docker run -d -e DISPLAY=$DISPLAY \
           -v /tmp/.X11-unix:/tmp/.X11-unix \
           climacraft)

# Wait for the container to finish its task
docker wait $CONTAINER_ID

# Copy only the weather_report.pdf to your host's Download directory
docker cp $CONTAINER_ID:/app/latex/weather_report.pdf "$HOST_PDF_DIR/weather_report.pdf"

# Stop and remove the container
docker rm -f $CONTAINER_ID

# Revoke X11 permissions after the container stops
xhost -local:docker

echo "PDF has been saved to $HOST_PDF_DIR/weather_report.pdf"

