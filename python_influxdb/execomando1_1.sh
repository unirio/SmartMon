#!/usr/bin/env bash
cd /home/sdn/
echo "alterar@2020" | sudo -S mn -c
echo h1 iperf -c h2 -u -t 10  | sudo -E $ONOS_ROOT/tools/test/topos/bmv2-demo.py --onos-ip=127.0.0.1 --pipeconf-id=org.onosproject.pipelines.int



