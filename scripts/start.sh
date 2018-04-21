#!/usr/bin/env bash

docker pull guitarmind/tesseract-web-service
docker run --rm -d -p 1688:1688 guitarmind/tesseract-web-service

# make sure image is available
docker run -p 8080:8080 --rm science-parse:latest
