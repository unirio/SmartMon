import time
import os
from random import choice


def rodarIperf(sinal):

    lista = [0, 1]
    tam = 120
    while True:
        sinal = open("/home/sdn/python_influxdb/espera.txt", "r")
        sinalInt = sinal.readline()
        line = sinalInt.strip()
        sinal.close()
        
        #saida = choice(lista)
        
        if line == "1":
            for i in range(0, tam):
                os.system("iperf -c 10.0.0.3 -t {} -u -b 8M", i)
                #time.sleep(3)
                continue
            tam = tam / 2
            
      


if __name__ == '__main__':
    sinalINT = open("/home/sdn/python_influxdb/espera.txt", "r")
    rodarIperf(sinalINT)
    sinalINT.close()
