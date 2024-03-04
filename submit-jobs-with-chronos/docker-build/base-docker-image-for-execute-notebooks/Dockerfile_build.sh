#! /bin/bash

TAG=registry-clustergpu.recas.ba.infn.it/<username>/<image-name>:<image_version>
docker build -t $TAG .
docker push $TAG