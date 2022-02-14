#!/bin/bash

function usage {
    echo "$0 DOCKERFILE"
    exit 0
}

BDIR=$(dirname $BASH_SOURCE)
source $BDIR/build.vars

[[ ! -f $BDIR/$1 ]] && usage

IMG=$(echo $1 | awk -F. '{print $1}')
docker build -t $IMG -f $1 $BDIR 
docker image tag $IMG $REGISTRY/tb/$IMG
docker image push $REGISTRY/tb/$IMG
echo y | docker system prune -a 
