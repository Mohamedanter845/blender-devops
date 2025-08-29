FROM blenderkit/headless-blender:blender-4.4

# Set working directory
WORKDIR /app

# Copy project files
COPY blender/ /app/blender/
COPY textures/ /app/textures/

# Create output dir inside container
RUN mkdir -p /app/output

# Ensure Blender is in PATH permanently
ENV PATH="/home/headless/blender:${PATH}"

# Define mount point for renders
VOLUME ["/renders"]

# Install Python3 + pip + Flask
RUN apt-get update && apt-get install -y python3 python3-pip && \
    pip3 install flask --break-system-packages && \
    rm -rf /var/lib/apt/lists/*

# Copy the web server script
COPY webserver.py /app/webserver.py

# Expose port 8080
EXPOSE 8080

# Start Flask server
CMD ["python3", "/app/webserver.py"]

