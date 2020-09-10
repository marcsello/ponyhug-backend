#!/usr/bin/env bash

docker build -t registry.kmlabz.com/ponyhug/backend .
docker push registry.kmlabz.com/ponyhug/backend
