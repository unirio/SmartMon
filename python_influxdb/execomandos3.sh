#!/usr/bin/env bash
cd /home/sdn/
echo "alterar@2020" | sudo -S echo "arquivo execomandos3"
echo mirroring_add 500 4 | simple_switch_CLI --thrift-port `cat /tmp/bmv2-s12-thrift-port`
sleep 3s
sudo python BPFCollector/InDBClient.py -d 1 veth_2

