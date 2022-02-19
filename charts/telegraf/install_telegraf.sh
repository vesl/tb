#!/bin/bash

for instance in $(ls values.telegraf-*.yaml)
do
	release_name=$(echo $instance | awk -F. '{print $2}')
	$(helm list | grep -q $release_name) || helm install $release_name -f $instance influxdata/telegraf
done
