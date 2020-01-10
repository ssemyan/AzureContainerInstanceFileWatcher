# Get the small python 3.6 image
FROM python:3.6-slim

# Create directories to watch and hold the python script
RUN mkdir -p /tmp/watch
RUN mkdir -p /tmp/processed
RUN mkdir -p /home/watcher

WORKDIR /home/watcher

# Copy the script
COPY watcher.py .

# Run python unbuffered so we can see the output in docker logs
CMD [ "python", "-u", "./watcher.py" ]
