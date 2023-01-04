#!/usr/bin/env bash
#vai diretorio raiz
#cd /home/ub181/
cd /home/sdn/
#pior forma de fazer isso, arrumar outro jeito
echo "alterar@2020" | sudo -S echo "arquivo execomandos3"

#echo mirroring_add 500 4 | simple_switch_CLI --thrift-port `cat /tmp/bmv2-s12-thrift-port`
#sleep 3s
#sudo python BPFCollector/InDBClient.py -d 1 veth_2 &
#echo "$!" 
#exit 0

pwd &

echo $! >/tmp/my-app.pid
exit 0
