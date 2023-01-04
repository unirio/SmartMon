#!/usr/bin/env bash
cd /home/sdn/BPFCollector
echo "alterar@2020" | sudo -S sysctl net/core/bpf_jit_enable
sudo ip link add veth_1 type veth peer name veth_2
sudo ip link set dev veth_1 up
sudo ip link set dev veth_2 up
pip install Cython
sleep 3s
pip install influxdb



