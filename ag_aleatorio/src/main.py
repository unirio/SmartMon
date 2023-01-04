#Classe principal que faz a orquestração do Agente Aleatório
# -*- coding: utf-8 -*-
import time
import sys
from ambiente import Ambiente
from agente import Agente


# Cria as instancias das classes
ambiente = Ambiente()
agente = Agente()

EPISODES = 20
TIMESTEPS = 64
TARG = []
TARGF = []
LISTARECOMP = []
LISTAACAO = []
LISTAMEDIAS = []


estado = []
saidaAg = open("../python_influxdb/AGOut.txt", "w")
saidaAg.write("")
saidaAg.close()
done = False
ambiente.salvarLog("logDQNOut.txt", "w", "Log DQNout")
ambiente.salvarLog("logRecompensa.txt", "w","Log Recompensa")
ambiente.salvarLog("logSaidaPasso.txt", "w", "Log Saída Passo")
cont = 0
j = 0
for e in range(EPISODES):
    tempoIni = time.time()
    state = ambiente.inicializaEstado()

    for i in range(TIMESTEPS):
        print("i:", i)
        ambiente.configEspelhamento()
        time.sleep(10)        
        action = agente.executaAcao()
        ambiente.interageAmbiente(action, cont)
        

        print("Agente - e:", e, "t:", i, "acao:", action, "cont:", cont)
        time.sleep(30)
        cont += 1
        setazero = open("../python_influxdb/file.txt", "w")
        setazero.write("0")
        setazero.close()
        time.sleep(10)
        next_state, reward, medias = ambiente.passos(action)
        time.sleep(5)
        
        if i == TIMESTEPS - 1:
            done = True        
        state = next_state
        ambiente.fechaJanelaEbpf()
        time.sleep(5)
        LISTAACAO.append(action)
        LISTARECOMP.append(reward)
        LISTAMEDIAS.append(medias)
        tempoFim = time.time()
        tempoEpisodio = (tempoFim - tempoIni)

        if done:
            print("episode: {}/{}, score: {}, action: {}, episodeTime: {}, reward: {}, listacao: {}, listareward: {}, medias: {}"
                      .format(e, EPISODES, i, action, tempoEpisodio, reward, LISTAACAO, LISTARECOMP, LISTAMEDIAS))
            ambiente.saidaDQN(e, EPISODES, i, action, tempoEpisodio, reward, LISTAACAO, LISTARECOMP, LISTAMEDIAS)
            break

    done = False
    cont += 1
    LISTAACAO = []
    LISTARECOMP = []
    LISTAMEDIAS = []