#!/bin/bash

docker run \
-p 8000:8000 \
-v /var/www/FockNews/volume:/usr/src/FockNews/volume \
-it --rm \
--name focknews onlikerop/focknews
