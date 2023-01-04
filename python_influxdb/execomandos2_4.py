import time
import os


def rodarIperf(sinal):
    
    while True:
        sinal = open("../python_influxdb/file.txt", "r")
        sinalInt = sinal.readline()
        line = sinalInt.strip()
        sinal.close()
        if line == "1":
            
            os.system("iperf -c 10.0.0.3 -t 30 -u -b 3M")

            continue 
 
        

        time.sleep(0.1)

	


if __name__ == '__main__':
     sinalINT = open("../python_influxdb/file.txt", "r")
     rodarIperf(sinalINT)
     sinalINT.close()
