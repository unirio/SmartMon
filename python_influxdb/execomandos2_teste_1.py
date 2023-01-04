import time
import os
#from random import choice
import random


def rodarIperf(sinal):

    lista = [0, 1]
    while True:
        sinal = open("../python_influxdb/espera.txt", "r")
        sinalInt = sinal.readline()
        line = sinalInt.strip()
        sinal.close()

        #saida = choice(lista)
        if line == "1":
            vet = ['5M','20M', '35M', '51M', '45M', '30M', '25M', '10M']
            i = random.choice(vet)
            s = 'iperf -c 10.0.0.4 -t 60 -u -b ' + i
            os.system(s)
            time.sleep(1)
 
            print("banda:", i)
        time.sleep(0.1)


if __name__ == '__main__':
    sinalINT = open("../python_influxdb/espera.txt", "r")
    rodarIperf(sinalINT)
    sinalINT.close()
