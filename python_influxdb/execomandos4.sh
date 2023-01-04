#!/usr/bin/env bash
for pid in $(ps -ef | grep /home/sdn/python_influxdb/execomandos3.sh | awk '{print $2}'); do kill -9 $pid; done
