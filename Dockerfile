# Set base image (host OS)
FROM python:3.9-slim-buster

# By default, listen on port 5000
EXPOSE 5000/tcp

# Set the working directory in the container
WORKDIR /app

# Copy the templates into the app
COPY templates /app/templates/
COPY helpers /app/helpers/
COPY static /app/static/

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Installing native files to run numpy
# RUN apk --no-cache add musl-dev linux-headers g++

# Install any dependencies
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY application.py .

# Specify the command to run on container start
CMD [ "python", "./application.py" ]