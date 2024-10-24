# Use a base image with Python
FROM python:3.11

# Set the working directory
WORKDIR /app

# Install required packages for Chrome and other dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    libnss3 \
    libxss1 \
    libappindicator3-1 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libgbm-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


# Add Google's official GPG key
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - 

# Set up the Google repository
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list

# Install Google Chrome
RUN apt-get update && apt-get install -y google-chrome-stable

# Install Python dependencies (add your requirements.txt if you have one)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8080

# Command to run the application
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]




# # Use an official Python runtime as a parent image
# FROM python:3.12-slim

# # Set the working directory in the container
# WORKDIR /app

# # Copy the current directory contents into the container at /app
# COPY . /app

# # Install required packages
# RUN apt-get update && apt-get install -y \
#     wget \
#     curl \
#     gnupg \
#     unzip \
#     && rm -rf /var/lib/apt/lists/*

# # Install Google Chrome
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
#     sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' && \
#     apt-get -y update && \
#     apt-get install -y google-chrome-stable

# # Install ChromeDriver matching the installed version of Chrome
# RUN apt-get update && apt-get install -y \
#     chromium-driver \
#     && ln -s /usr/bin/chromedriver /usr/local/bin/chromedriver

# # Set display port to avoid crash
# ENV DISPLAY=:99

# # Install Python dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Expose port 8080 for Google Cloud Run
# EXPOSE 8080

# # Set environment variables for Streamlit to work properly
# ENV PYTHONUNBUFFERED=1
# ENV STREAMLIT_SERVER_PORT=8080
# ENV STREAMLIT_SERVER_HEADLESS=true

# # Run the Streamlit app
# ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]









