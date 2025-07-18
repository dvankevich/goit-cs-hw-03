#!/bin/bash

docker run --rm -it -v $(pwd):/data rtsp/mongosh mongoimport --uri mongodb://172.17.0.1:27017 --collection cats --file /data/cats_data.json --jsonArray