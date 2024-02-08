#!/bin/bash

# Start the Docker service
sudo service docker start

cd ..

# building
sudo docker build -t voitra -f Docker/Dockerfile . #

# Run the Docker container
sudo docker run -it --rm -v ~/tracks:/bot/app/tracks -p 443:443 --env-file .env voitra