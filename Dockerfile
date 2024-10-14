# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install required packages
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get -y update && \
    apt-get install -y google-chrome-stable

# Install ChromeDriver matching the installed version of Chrome
RUN apt-get update && apt-get install -y \
    chromium-driver \
    && ln -s /usr/bin/chromedriver /usr/local/bin/chromedriver

# Set display port to avoid crash
ENV DISPLAY=:99

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080 for Google Cloud Run
EXPOSE 8080

# Set environment variables for Streamlit to work properly
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_PORT=8080
ENV STREAMLIT_SERVER_HEADLESS=true

# Run the Streamlit app
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]






# # Use an official Python runtime as a parent image
# FROM python:3.12-slim

# # Set the working directory in the container
# WORKDIR /app

# # Copy the current directory contents into the container at /app
# COPY . /app

# # Install any needed packages specified in requirements.txt
# RUN apt-get update && apt-get install -y \
#     wget \
#     curl \
#     gnupg \
#     unzip \
#     && rm -rf /var/lib/apt/lists/*
# # install google chrome
# # Install Google Chrome and match it with the correct ChromeDriver version
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
# RUN apt-get -y update
# RUN apt-get install -y google-chrome-stable=114.0.5735.90-1
    
#     # Install the matching version of ChromeDriver for Chrome 114
# RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
# RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
# # set display port to avoid crash
# ENV DISPLAY=:99
# RUN pip install --no-cache-dir -r requirements.txt

# # Expose port 8080 for Google Cloud Run
# EXPOSE 8080

# # Set environment variables for Streamlit to work properly
# ENV PYTHONUNBUFFERED=1
# ENV STREAMLIT_SERVER_PORT=8080
# ENV STREAMLIT_SERVER_HEADLESS=true

# # Run the Streamlit app
# CMD ["streamlit", "run", "app_with_json.py", "--server.port=8080", "--server.enableCORS=false"]



