# Start with a Python 3.10 base image
FROM python:3.10

# Set the working directory in the Docker container
WORKDIR /app

# Copy the contents of your application into the container
COPY . /app

# Install system dependencies, including LaTeX packages, GTK 3, and GObject introspection libraries
RUN apt-get update && apt-get install -y \
    gnuplot \
    texlive-latex-base \
    texlive-latex-recommended \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-science \
    libgirepository1.0-dev \
    libgtk-3-dev \  
    gir1.2-gtk-3.0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Command to run your application
CMD ["python", "main.py"]

