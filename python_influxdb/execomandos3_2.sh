#!/usr/bin/env bash
#vai diretorio raiz
#cd /home/ub181/
cd /home/sdn/
#pior forma de fazer isso, arrumar outro jeito
echo "alterar@2020" | sudo -S echo "arquivo execomandos3"

#inicia mininet
#sudo -E $ONOS_ROOT/tools/test/topos/bmv2-demo.py --onos-ip=127.0.0.1 --pipeconf-id=org.onosproject.pipelines.int

#mirroring_add 500 4
#simple_switch_CLI --thrift-port `cat /tmp/bmv2-s12-thrift-port`
#sudo python BPFCollector/InDBClient.py -d 1 veth_2
#sleep 1m


#Dessa forma escreve no switch
#sudo systemctl stop influxdb
#sleep 3s
#sudo systemctl start influxdb
#sleep 3s
echo mirroring_add 500 4 | simple_switch_CLI --thrift-port `cat /tmp/bmv2-s12-thrift-port`
sleep 3s
sudo python BPFCollector/InDBClient.py -d 1 veth_2 
sleep 3s 
exit &

#sleep 40s
#exit
#dessa forma na mininet
#echo h1 iperf -c h2 -u -t 10000 | sleep 1m  | sudo -E $ONOS_ROOT/tools/test/topos/bmv2-demoIp.py --onos-ip=127.0.0.1 --pipeconf-id=org.onosproject.pipelines.int

#open -a Terminal"'pwd'" 
#gnome-terminal -x "pwd"
#os.system("gnome-terminal -x pwd")
#os.system("gnome-terminal -x python teste.py")



