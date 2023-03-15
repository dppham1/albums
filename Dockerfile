FROM python:3

# Set up the Python environment
WORKDIR /usr/src/weecare
COPY albums ./albums
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose the port
EXPOSE 80

# Set the entry point
CMD [ "flask", "--app" , "albums", "run", "--host", "0.0.0.0", "--port", "80", "--no-reload"]