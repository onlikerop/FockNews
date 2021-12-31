#!/bin/bash

docker rmi onlikerop/focknews

docker build ^
-t ^
onlikerop/focknews .
