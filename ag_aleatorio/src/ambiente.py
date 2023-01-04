# -*- coding: utf-8 -*-
from sre_compile import isstring
from influxdb import InfluxDBClient
from pandas import DataFrame
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import StandardScaler
import numpy as np
from collections import deque
from random import choice
import sys
import os
from configuracao import ConfiguraVariaveis
from agente import Agente

class Ambiente():

    def __init__(self, nome="Ambiente SDN"):
        self.nome = nome
        self.caminhoInfluxdb = "../python_influxdb/"
        self.caminhoNode = "../node_novo/"
        self.mem = deque(maxlen=2000)
        self.estado = 0
        self.contador = 0
        self.mediaLatSalto = 0
        self.mediaLatFluxo = 0
        self.mediaFila = 0    
        self.acao = 0
        self.amediaLatSalto = 0
        self.amediaLatFluxo = 0
        self.amediaFila = 0
        self.pmediaLatSalto = 0
        self.pmediaLatFluxo = 0
        self.pmediaFila = 0
    
    
    # Método para obter o atributo caminho Influxdb
    def getMem(self):
        return self.mem

    def setMem(self, state):
        self.mem.append((state))
    
    # Método para gerar um novo nome
    def setNome(self, novo_nome):
        self.nome = novo_nome

    # Método para obter o atributo nome
    def getNome(self):
        return self.nome

    # Método para gerar um novo caminho
    def setCaminhoInfluxdb(self, novo_caminho):
        self.caminhoInfluxdb = novo_caminho

    # Método para obter o atributo caminho Influxdb
    def getCaminhoInfluxdb(self):
        return self.caminhoInfluxdb

    def setMediaLatSalto(self, salto):
        self.mediaLatSalto = salto

    def getMediaLatSalto(self):
        return self.mediaLatSalto

    def setMediaLatFluxo(self, fluxo):
        self.mediaLatFluxo = fluxo

    def getMediaLatFluxo(self):
        return self.mediaLatFluxo

    def setMediaFila(self, fila):
        self.mediaFila = fila

    def getMediaFila(self):
        return self.mediaFila

    #chamdo do InterageAmbiente
    def setAcao(self, acao):
        self.acao = acao
    #chamado do media
    def getAcao(self):
        return self.acao

    #metodos usados para log
    def getEstado(self):
        return self.estado

    def setEstado(self, state):
        self.estado = state
    
    def setAMediaLatSalto(self, salto):
        self.amediaLatSalto = salto

    def getAMediaLatSalto(self):
        return self.amediaLatSalto

    def setAMediaLatFluxo(self, fluxo):
        self.amediaLatFluxo = fluxo

    def getAMediaLatFluxo(self):
        return self.amediaLatFluxo

    def setAMediaFila(self, fila):
        self.amediaFila = fila

    def getAMediaFila(self):
        return self.amediaFila
    
    def setPMediaLatSalto(self, salto):
        self.pmediaLatSalto = salto

    def getPMediaLatSalto(self):
        return self.pmediaLatSalto

    def setPMediaLatFluxo(self, fluxo):
        self.pmediaLatFluxo = fluxo

    def getPMediaLatFluxo(self):
        return self.pmediaLatFluxo

    def setPMediaFila(self, fila):
        self.pmediaFila = fila

    def getPMediaFila(self):
        return self.pmediaFila


    # Fecha a janela aberta sem bash no final do comando
    def executaComando(self, comando):
        os.system("gnome-terminal -e 'bash -c \""+comando+"\"'")
        print("Ambiente: Depois de executaComando")

    # Configura o espelhamento e levanta coletor
    def configEspelhamento(self):
        comando = "sh " + self.caminhoInfluxdb + "execomandos3.sh"
        print("quarta Janela Configura Espelhamento")
        self.executaComando(comando)

    def fechaJanelaEbpf(self):
        print("Ambiente: fechaJanelaEbpf")
        comando = "sh " + self.caminhoInfluxdb + "execomandos4.sh"
        self.executaComando(comando)

    """Métodos criados para usar com o AgenteAleatorio
    """
    def saidaDQN(self, e, EPISODES, t, action, tempoEpiso, reward, LISTAACAO, LISTARECOMP, medias):
        somaRecompensa = self.somaRecompensa(LISTARECOMP)
        r = []
        r = ["Somatório Recompensa:", somaRecompensa]

        l = []
        l = ["Episode: ", e, "/", EPISODES, "Score: ", t, "ação: ", action, "TempoEpisodio:", tempoEpiso, "Reward:", reward]

        a = []
        a = ["listaacao:", LISTAACAO]

        b = []
        b = ["listaRecompensa:", LISTARECOMP]

        c = []
        c = ["Medias:", medias]
        

        lista = ' '.join(map(str, l))
        lista1 = ' '.join(map(str, a))
        lista2 = ' '.join(map(str, b))
        lista3 = ' '.join(map(str, c))
        lista4 = ' '.join(map(str, r))

        l = lista + '\n' + lista1 + '\n' + lista2 + '\n' + lista3 + '\n'


        if os.path.isfile('logDQNOut.txt'):

            self.salvarLog("logDQNOut.txt", "a", l)
        else:
            self.salvarLog("logDQNOut.txt", "w", l)


        if os.path.isfile('../AGOut.txt'):
            print("é arquivo")
            saidaDQN = open("../python_influxdb/AGOut.txt", "a")
            saidaDQN.write(lista)
            saidaDQN.write("\n")
            saidaDQN.write(lista1)
            saidaDQN.write("\n")
            saidaDQN.write(lista2)
            saidaDQN.write("\n")
            saidaDQN.write(lista3)
            saidaDQN.write("\n")
            saidaDQN.write(lista4)
            saidaDQN.write("\n")
            saidaDQN.close()
        else:
            print("criar arquivo")
            saidaDQN = open("../python_influxdb/AGOut.txt", "w")
            saidaDQN.write(lista)
            saidaDQN.write("\n")
            saidaDQN.write(lista1)
            saidaDQN.write("\n")
            saidaDQN.write(lista2)
            saidaDQN.write("\n")
            saidaDQN.write(lista3)
            saidaDQN.write("\n")
            saidaDQN.write(lista4)
            saidaDQN.write("\n")
            saidaDQN.close()
   
   #tamanho do estado
    def tamEstado(self, var_ambiente):
        qtdSwsMax = var_ambiente.getQtdSwsMax()
        valorSWs = var_ambiente.getValorSws()
        valor = ((3 * qtdSwsMax) + 1) * valorSWs
        return valor

    #verificar se esse metodo está sendo usado"""
    def tamAcao(self):
        # sao duas ações de telemetria
        listaAcao = ["minima", "maxima"]
        return len(listaAcao)

    #inicializa o primeiro estado
    def inicializaEstado(self):
        estado = []
        var_ambiente = ConfiguraVariaveis()
        tamEstado = self.tamEstado(var_ambiente)
        for i in range(tamEstado):
            estado.append(-1)
        self.setMem(estado)
        self.setEstado(-1)
        return estado

    # interage com a interface do INT, aumentando ou diminuindo telemetria

    def interageAmbiente(self, acao, num):
        
        valor = acao
        if num == 0:
            # Na primeira vez que roda INT
            if(valor < 0.5):
                print("Diminui Telementria (medio) = ", valor)
                comando = "node " + self.caminhoNode + "funcao3.js medio"
                self.executaComando(comando)
            else:
                print("Aumenta Telementria (maximo) = ", valor)
                comando = "node " + self.caminhoNode + "funcao3.js"
                self.executaComando(comando)
        else:
            # Os demais INT precisa apagar a interface 
            print("Precisa apagar INT")
            if(valor < 0.5):
                print("Diminui Telementria (medio) = ", valor)
                comando = "node " + self.caminhoNode + "funcao3_1.js medio"
                self.executaComando(comando)
            else:
                print("Aumenta Telementria (maximo) = ", valor)
                comando = "node " + self.caminhoNode + "funcao3_1.js"
                self.executaComando(comando)

    
    def feito(self, var_ambiente):
        cont = 0
        if cont >= var_ambiente.getQtdMaxPassos():
            return True
        else:
            cont += 1
            return False

    
    def passos(self, acao):
        
        if self.getEstado() == -1:
            self.setAMediaLatSalto(0)
            self.setAMediaLatFluxo(0)
            self.setAMediaFila(0)          
            estado = self.grandeVetor()
            self.setPMediaLatSalto(self.getMediaLatSalto())
            self.setPMediaLatFluxo(self.getMediaLatFluxo())
            self.setPMediaFila(self.getMediaFila())
            recompensa = self.recompensa(acao)
            medias = []
            medias = self.mediaImprimir()
            self.setEstado(0)
            print("Passo -1")
            print("AMediaSalto:", self.getAMediaLatSalto(), "AMediaFluxo:",  self.getAMediaLatFluxo(),"AMediaFila", self.getAMediaFila(), "acao", acao, "recompensa:", recompensa)
            print("PMediaSalto:", self.getPMediaLatSalto(), "PMediaFluxo:",  self.getPMediaLatFluxo(),"PMediaFila", self.getPMediaFila(), "acao", acao, "recompensa:", recompensa)
            var = "AMediaSalto: " + str(int(self.getAMediaLatSalto())) + " AMediaFluxo: " + str(int(self.getAMediaLatFluxo())) + " AMediaFila " + str(int(self.getAMediaFila())) + " acao " + str(acao) + " recompensa: " + str(recompensa) + "\n" + "PMediaSalto: " + str(int(self.getPMediaLatSalto())) + " PMediaFluxo: " +  str(int(self.getPMediaLatFluxo())) + " PMediaFila: " + str(int(self.getPMediaFila())) + " acao " +  str(acao) +  " recompensa: " + str(recompensa) + "\n"
            self.salvarLog("logSaidaPasso.txt", "a", var)
            return estado, recompensa , medias
        else:
            self.setAMediaLatSalto(self.getPMediaLatSalto())
            self.setAMediaLatFluxo(self.getPMediaLatFluxo())
            self.setAMediaFila(self.getPMediaFila())
            estado = self.grandeVetor()
            self.setPMediaLatSalto(self.getMediaLatSalto())
            self.setPMediaLatFluxo(self.getMediaLatFluxo())
            self.setPMediaFila(self.getMediaFila())
            recompensa = self.recompensa(acao)
            medias = []
            medias = self.mediaImprimir()
            print("Passo ao longo dos timesteps")
            print("AMediaSalto:", self.getAMediaLatSalto(), "AMediaFluxo:",  self.getAMediaLatFluxo(),"AMediaFila", self.getAMediaFila(), "acao", acao, "recompensa:", recompensa)
            print("PMediaSalto:", self.getPMediaLatSalto(), "PMediaFluxo:",  self.getPMediaLatFluxo(),"PMediaFila", self.getPMediaFila(), "acao", acao, "recompensa:", recompensa)
            var = "AMediaSalto: " + str(int(self.getAMediaLatSalto())) + " AMediaFluxo: " + str(int(self.getAMediaLatFluxo())) + " AMediaFila " + str(int(self.getAMediaFila())) + " acao " + str(acao) + " recompensa: " + str(recompensa) + "\n" + "PMediaSalto: " + str(int(self.getPMediaLatSalto())) + " PMediaFluxo: " +  str(int(self.getPMediaLatFluxo())) + " PMediaFila: " + str(int(self.getPMediaFila())) + " acao " +  str(acao) +  " recompensa: " + str(recompensa) + "\n"
            self.salvarLog("logSaidaPasso.txt", "a", var)
            return estado, recompensa , medias


    def calculaMedias(self, salto, fluxo, fila):

        aux = 0
        mediaS = 0
        for i in salto:
            aux = aux + i
            #print("aux", aux)

        mediaS = aux / len(salto)
        self.setMediaLatSalto(mediaS)
        #print("mediaS:", mediaS)
        #print(self.getMediaLatSalto())

        aux2 = 0
        mediaF = 0
        for i in fluxo:
            aux2 = aux2 + i
            #print("aux2", aux2)
        mediaF = aux2 / len(fluxo)
        self.setMediaLatFluxo(mediaF)
        #print(self.getMediaLatFluxo())

        v = 0.0
        c = 0.0
        m = 0.0
        for i in fila:
            if i != 0.0:
                v = v + i
                #qtd de elementos diferentes de zero na fila
                c = c + 1
                #print("valores na fila", i, c)
                    
            if v == 0.0:
                self.setMediaFila(v)
                #print("valores na fila", v)
            else:
                m = v/c
                self.setMediaFila(m)
                #print("media valores na fila", m)


    def recompensa(self, acao):
        x = 1
        y = 1000
        z = 1000
     

        mediaLatenciaSalto = int(self.getAMediaLatSalto())
        mediaLatenciaFluxo = int(self.getAMediaLatFluxo())
        mediaTamanhoFila = int(self.getAMediaFila())

        if mediaTamanhoFila == 0 and mediaLatenciaSalto == 0 and mediaLatenciaFluxo == 0:
            #print("0 - Estado Inicial -> recompensa 0")
            if (acao == 0):
                self.salvarLog("logRecompensa.txt", "a", "0 - Estado Inicial  -> recompensa 0 - Ação -> 0")
                self.salvarLog("logSaidaPasso.txt", "a", "0 - Estado Inicial  -> recompensa 0 - Ação -> 0")
            else:
                self.salvarLog("logRecompensa.txt", "a", "0 - Estado Inicial  -> recompensa 0 - Ação -> 1")
                self.salvarLog("logSaidaPasso.txt", "a", "0 - Estado Inicial  -> recompensa 0 - Ação -> 1")

            return 0

        if mediaTamanhoFila >= x and mediaLatenciaSalto >= y and mediaLatenciaFluxo >= z:
            if(acao == 0):
                #print("1 - Telemetria Media -> recompensa -10")
                self.salvarLog("logRecompensa.txt", "a", "1 - Telemetria Media  -> recompensa -10 - Ação -> 0")
                self.salvarLog("logSaidaPasso.txt", "a", "1 - Telemetria Media  -> recompensa -10 - Ação -> 0")
                return -10
            else:
               # print("2 - Telemetria Alta  -> recompensa 10")
                self.salvarLog("logRecompensa.txt", "a", "2 - Telemetria alta  -> recompensa 10 - Ação -> 1")
                self.salvarLog("logSaidaPasso.txt", "a", "2 - Telemetria alta  -> recompensa 10 - Ação -> 1")
                return 10
        else:
            if mediaTamanhoFila >= x and (mediaLatenciaSalto < y or mediaLatenciaFluxo < z):
                if(acao == 0):
                    #print("3 - Telemetria Media -> recompensa -10")
                    self.salvarLog("logRecompensa.txt", "a", "3 - Telemetria Media -> recompensa -10 - Ação -> 0")
                    self.salvarLog("logSaidaPasso.txt", "a", "3 - Telemetria Media -> recompensa -10 - Ação -> 0")
                    return -10
                else:
                    #print("4 - Telemetria Alta -> recompensa 10")
                    self.salvarLog("logRecompensa.txt", "a", "4 - Telemetria Alta -> recompensa 10 - Ação -> 1")
                    self.salvarLog("logSaidaPasso.txt", "a", "4 - Telemetria Alta -> recompensa 10 - Ação -> 1")
                    return 10
            else:
                if mediaTamanhoFila < x and (mediaLatenciaSalto >= y or mediaLatenciaFluxo >= z):
                    if(acao == 0):
                        #print("5 - Telemetria Media -> recompensa -10")
                        self.salvarLog("logRecompensa.txt", "a", "5 - Telemetria Media -> recompensa -10 - Ação -> 0")
                        self.salvarLog("logSaidaPasso.txt", "a", "5 - Telemetria Media -> recompensa -10 - Ação -> 0")
                        return -10
                    else:
                        #print("6 - Telemetria Alta -> recompensa 10")
                        self.salvarLog("logRecompensa.txt", "a", "6 - Telemetria Alta -> recompensa 10 - Ação -> 1")
                        self.salvarLog("logSaidaPasso.txt", "a", "6 - Telemetria Alta -> recompensa 10 - Ação -> 1")
                        return 10
                else:
                    if mediaTamanhoFila < x and mediaLatenciaSalto < y and mediaLatenciaFluxo < z:
                        if(acao == 0):
                            #print("7 - Telemetria Media -> recompensa 10")
                            self.salvarLog("logRecompensa.txt", "a", "7 - Telemetria Media -> recompensa 10 - Ação -> 0")
                            self.salvarLog("logSaidaPasso.txt", "a", "7 - Telemetria Media -> recompensa 10 - Ação -> 0")
                            return 10
                        else:
                            #print("8 - Telemetria Alta -> recompensa -10") 
                            self.salvarLog("logRecompensa.txt", "a", "8 - Telemetria Alta -> recompensa -10 -  Ação -> 1")
                            self.salvarLog("logSaidaPasso.txt", "a", "8 - Telemetria Alta -> recompensa -10 -  Ação -> 1")
                            return -10

  

    def salvarLog(self, nomeArq, tipo, conteudo):

        if isstring(conteudo):
            print("SalvarLOG texto conteudo")
        else:
            print("SalvarLOG vetor")
            conteudo = np.array2string(conteudo, precision=3,
                              separator=',', suppress_small=True)
        
        arquivo = open(nomeArq, tipo)
        arquivo.write(conteudo)
        arquivo.write("\n")
        arquivo.close()
  

    

    def somaRecompensa(self, LISTARECOMP):
        somaRec = 0
        res = list(map(int, LISTARECOMP))
        for i in res:
            somaRec += i
        return somaRec

    def mediaImprimir(self):
        salto = int(self.getMediaLatSalto())
        fluxo = int(self.getMediaLatFluxo())
        fila = int(self.getMediaFila())
        return salto, fluxo, fila
        
    def qtdMaxPassos(self):

        var_ambiente = ConfiguraVariaveis()
        tam = var_ambiente.getQtdMaxPassos()
        return tam


    def preencherSw(self, tipo, strtipo, var_ambiente):
        sws_usados = self.swsUsados(strtipo)
        tam_vetor = self.tamanhoVetor(tipo)
        # aqui pode retornar uma lista de sws não estão sendo usados mas que são possiveis
        nos_possiveis = var_ambiente.getNosPossiveis()
        lista_final = [x for x in nos_possiveis if x not in sws_usados]
        # transformando os valores das lista para inteiros
        for i in range(0, len(lista_final)):
            lista_final[i] = int(lista_final[i])
        tam = len(sws_usados)
        # deixando o ultimo valor dos sws_usados como inteiro
        ultimo = int(sws_usados[tam-1])
        zeros = np.zeros(var_ambiente.getValorSws(), dtype=float)
   
        if ultimo < lista_final[0]:
            aux = self.preencheZeros(tipo, tam_vetor, var_ambiente)
            aux.extend(zeros)
            return aux
        else:
            aux = self.preencheZeros(tipo, tam_vetor, var_ambiente)
            t = len(aux)
            posicao = t - var_ambiente.getValorSws()
            c = 0
            ini = []
            for i in aux:
                ini.append(i)
                c = c + 1
                if c == posicao:
                    ini.extend(zeros)

            return ini


    def comparaPathVet(self, var_ambiente):
        lista = self.conexaoBD("fluxo")
        av = []
        bv = var_ambiente.getNosPossiveis()
        for i in lista[0][1]:
            for j in bv:
                if i.find(j) != -1:
                    f = i.count(j)
                    av.append(f)
                else:
                    f = 0
                    av.append(f)
        return av


    def swsUsados(self, tipo):
        tabelas = self.conexao()
        tam = len(tabelas)
        count = 0
        tabela = []
        for i in range(0, tam):
            tabela1 = (lambda k: k[u"name"])(tabelas[count])
            tabela.append(tabela1)
            count = count + 1

        vetor = self.posicaoConexaoBD(tabela, tipo)
        count = vetor[0]
        tam = len(vetor)
        tab = []
        for i in range(0, tam):
            tabela1 = tabela[count]
            tab.append(tabela1)
            count = count + 1
        texto = []
        for j in tab:
            aux = j.split(",")
            texto.append(aux)

        vetor = []
        for x in texto:
            if tipo == "salto":
                vetor.append(x[3])
            else:
                if tipo == "fila":
                    vetor.append(x[1])

        vet = []
        for y in vetor:
            aux = y.split("=", 2)
            vet.append(aux[1])
        return vet

 
    def preencheZeros(self, fila, vet, var_ambiente):
        nova = []
        c = 0
        for i in fila:
            if vet[c] >= var_ambiente.getValorSws():
                nova.extend(i)
            else:
                nova.extend(i)
                zeros = np.zeros(
                    (var_ambiente.getValorSws() - vet[c]), dtype=float)
                nova.extend(zeros)
            c = c+1
        return nova

    def fila(self, var_ambiente):
        fila = self.conexaoBD("fila")
        if fila is not False:
            vetor = np.array(fila, dtype=object)
            vet = vetor.tolist()
            qtdSwsUsados = self.swsUsados("fila")
            tamvet = self.tamanhoVetor(fila)
            for i in tamvet:
                if i > var_ambiente.getValorSws():
                    vet = self.novaListaTamMax(
                        tamvet, vet, var_ambiente)
                    tamvet = self.tamanhoVetor(vet)

            if var_ambiente.getQtdSwsMax() == len(qtdSwsUsados):
                fila_completa = self.preencheZeros(vet, tamvet, var_ambiente)
                return fila_completa

            else:
                fila_completa = self.preencherSw(vet, "fila", var_ambiente)
                return fila_completa

        else:
            fila_vazia = np.zeros(
                var_ambiente.getValorSws() * var_ambiente.getQtdSwsMax(), dtype=float)
            return fila_vazia

    def conexao(self):
        client = InfluxDBClient(host='localhost', port='8086')
        client.switch_database("INTdatabase")
        tabelas = client.get_list_measurements()
        if not tabelas:
            return False
        else:
            return tabelas

    def posicaoConexaoBD(self, tabela, tipo):
        var_ambiente = ConfiguraVariaveis()
        qtdMaxSw = var_ambiente.getQtdSwsMax()
        vet_f_h_l = []
        vet_f_s = []
        vet_p_t_u = []
        vet_q_o = []
        j = 0
        for i in tabela:
            if (i.startswith('flow_hop_latency')):
                vet_f_h_l.append(j)
                j = j + 1

            else:
                if i.startswith('flow_stat'):
                    vet_f_s.append(j)
                    j = j + 1
                else:
                    if i.startswith('port_tx_utilize'):
                        vet_p_t_u.append(j)
                        j = j + 1
                    else:
                        if i.startswith('queue_occupancy'):
                            vet_q_o.append(j)
                            j = j + 1


        vet_f_h_l_1 = []
        for i in vet_f_h_l:
            if i < qtdMaxSw:
                vet_f_h_l_1.append(i)
        vet_f_s_1 = []
        f = qtdMaxSw-2

        vet_f_s_1.append(vet_f_s[f])
        if tipo == "salto":
            return vet_f_h_l
        else:
            if tipo == "fluxo":
                return vet_f_s
            else:
                if tipo == "porta":
                    return vet_p_t_u
                else:
                    if tipo == "fila":
                        return vet_q_o

    def verificaTabelas(self, var_ambiente):
        if self.conexao() is False:
            var = var_ambiente.getQtdSwsMax()
            valor = ((3 * var) + 1) * 30
            sem_tabela = []
            sem_tabela = np.zeros(valor)
            return sem_tabela
        else:
            return True

    def conexaoBD(self, tipo):
        tabelas = self.conexao()
        if not tabelas:
            return False
        else:
            tam = len(tabelas)
            count = 0
            tabela = []
            for i in range(0, tam):
                tabela1 = (lambda k: k[u"name"])(tabelas[count])
                tabela.append(tabela1)
                count = count + 1

            if tipo == "salto":
                vet_f_h_l = self.posicaoConexaoBD(tabela, "salto")
                if vet_f_h_l:
                   return self.conexaoBDVetor(vet_f_h_l, "vazio")
                else:
                   return False
            if tipo == "fluxo":
                vet_f_s = self.posicaoConexaoBD(tabela, "fluxo")
                if vet_f_s:
                    return self.conexaoBDVetor(vet_f_s, "vet_f_s")
                else:
                    return False

            if tipo == "porta":
                vet_p_t_u = self.posicaoConexaoBD(tabela, "porta")
                if vet_p_t_u:
                    return self.conexaoBDVetor(vet_p_t_u, "vazio")
                else:
                    return False

            if tipo == "fila":
                vet_q_o = self.posicaoConexaoBD(tabela, "fila")
                if vet_q_o:
                    return self.conexaoBDVetor(vet_q_o, "vazio")
                else:
                    return False

    def conexaoBDVetor(self, vetor, tipo):
        client = InfluxDBClient(host='localhost', port='8086')
        client.switch_database("INTdatabase")
        tabelas = client.get_list_measurements()
        if not tabelas:
            return False
        else:
            count = vetor[0]
            tabela = []
            frame = []
            for i in vetor:
                tabela1 = (lambda k: k[u"name"])(tabelas[count])
                tabela.append(tabela1)
                count = count + 1
                result = client.query('SELECT * FROM "' + tabela1 + '"')
                umResult = list(result.get_points())
                frame1 = DataFrame(umResult)
                if tipo == "vet_f_s":
                    lista = frame1.flow_latency, frame1.path
                    frame.append(lista)
                else:
                    lista = frame1.value
                    frame.append(lista)
        return frame

    def tamanhoVetor(self, vetor):
        vet = []
        aux = []
        for i in vetor:
            cont = 0
            for y in i:
                cont += 1
            vet.append(cont)
        return vet

    def latenciaSalto(self, var_ambiente):
        latencia_salto = self.conexaoBD("salto")

        if latencia_salto is not False:
            vetor = np.array(latencia_salto, dtype=object)
            vet = vetor.tolist()
            tamvet = []
            tamvet = self.tamanhoVetor(vetor)
            qtdSwsUsados = self.swsUsados("salto")
            for i in tamvet:
                if i > var_ambiente.getValorSws():
                    vet = self.novaListaTamMax(
                        tamvet, vet, var_ambiente)
                    tamvet = self.tamanhoVetor(vet)

            if var_ambiente.getQtdSwsMax() == len(qtdSwsUsados):
                salto_completa = self.preencheZeros(vet, tamvet, var_ambiente)
                return salto_completa

            else:
                salto_completa = self.preencherSw(
                    vet, "salto", var_ambiente)
                return salto_completa
        else:
            salto_vazia = np.zeros(var_ambiente.getValoresSw(
            ) * var_ambiente.getQtdSwsMax(), dtype=float)
            return salto_vazia

    def trataVetorPath(self, lista, var_ambiente):
        av = []
        bv = []
        av = self.comparaPathVet(var_ambiente)
        for i in av:
            bv.append(float(i))
        n = len(lista[0][1])
        transforma_lista = []
        tam_lista = len(bv)
        for i in range(n):
            ini = int(i*tam_lista/n)
            fim = int((i+1)*tam_lista/n)
            transforma_lista.append(bv[ini:fim])
        return transforma_lista

    def listaTamMax(self, lista):
        aux = []
        for i in range(0, len(lista)):
            aux.append(lista[i])
        del aux[30:len(lista)]
        return aux

    def testeListaTamMax(self, aux):
        c = 0
        aux1 = []
        for x in aux:
            if c <= 29:
                aux1.append(x)

            else:
                print("Erro - maior que trinta")
            c += 1
        return aux1

    def novaListaTamMax(self, tam_vetor, lista, var_ambiente):
        var_amb = var_ambiente.getValorSws()
        aux = []
        c = 0
        for i in tam_vetor:
            if i <= var_amb:
                aux.extend(lista[c])
                aux.extend(np.zeros(var_amb-i))
            else:
                aux.extend(self.testeListaTamMax(lista[c]))
            c += 1
     
        nova = [aux[i:i+var_amb] for i in range(0, len(aux), var_amb)]
        t = self.tamanhoVetor(nova)
        return nova

    def tratarLista(self, lista,  var_ambiente):
        nova = []
        nova1 = []     
        for i in lista[0][0]:
            nova.append(i)

        trata_vetor_path = self.trataVetorPath(lista, var_ambiente)
        tam_novo = len(trata_vetor_path)
        if len(nova) <= var_ambiente.getValorSws():
            for i in range(0, tam_novo):
                nova1.append(nova[i])
                nova1.extend(trata_vetor_path[i])
            sw_zeros = np.zeros(
                (var_ambiente.getValorSws() - tam_novo) * (var_ambiente.getQtdSwsMax() + 1))
            nova1.extend(sw_zeros)

        else:
            lista_tam_max = self.listaTamMax(nova)
            tam_novo = len(lista_tam_max)
            for i in range(0, tam_novo):
                nova1.append(lista_tam_max[i])
                nova1.extend(trata_vetor_path[i])

        return(nova1)

    def latenciaFluxo(self, var_ambiente):
        flow_hop_latency = self.conexaoBD("fluxo")
        if flow_hop_latency is not False:
            vetor = np.array(flow_hop_latency)
            vet = self.tratarLista(vetor, var_ambiente)
        return vet

    def escreveArquivo(self, vetor):
        arquivo = open("frame.txt", "w")
        vet = np.array2string(vetor, precision=3,
                              separator=',', suppress_small=True)
        arquivo.write(vet)
        arquivo.close()

    def normalizaDados(self, grandevetor):
        scaler = MinMaxScaler()
        rescaled = scaler.fit_transform(grandevetor)
        np.set_printoptions(precision=4)
        return rescaled

    def padroniza(self, grande_vetor):
        scaler = StandardScaler().fit(grande_vetor)
        rescaled = scaler.transform(grande_vetor)
        np.set_printoptions(precision=4)
        return rescaled

    def normaliza(self, grande_vetor):
        scaler = Normalizer().fit(grande_vetor)
        rescaled = scaler.transform(grande_vetor)
        np.set_printoptions(precision=4)
        return rescaled

    def escreveArquivo1(self, vetor):
        arquivo = open("frame1.txt", "w")
        vet = np.array2string(vetor, precision=3,
                              separator=',', suppress_small=True)
        arquivo.write(vet)
        arquivo.write("\n")
        arquivo.close()

    def preparaDadoNormaliza(self, vetor):
        aux = np.array(vetor, dtype=float)
        aux1 = aux.reshape(-1, 1)
        vetor_normalizado = self.normalizaDados(aux1)
        tam = len(vetor_normalizado)
        auxi = np.reshape(vetor_normalizado, [1, tam])
        return auxi

    
    def preencheValores(self):
        saidaDeque = self.getMem()
        saida = choice(saidaDeque)
        return saida


    def grandeVetor(self):
        var_ambiente = ConfiguraVariaveis()
        verifica_Tabelas = self.verificaTabelas(var_ambiente)
        if verifica_Tabelas is not True:
            self.escreveArquivo1(verifica_Tabelas)
            saida = self.preencheValores()
            self.contador += 1
            return saida
        else:
            latencia_salto = self.latenciaSalto(var_ambiente)
            latencia_salto_normalizado = self.preparaDadoNormaliza(
                latencia_salto)
            latencia_fluxo = self.latenciaFluxo(var_ambiente)
            fluxo = np.asarray(latencia_fluxo, dtype=object)
            latencia_fluxo_normalizado = self.preparaDadoNormaliza(fluxo)
            fila = self.fila(var_ambiente)
            fila_normalizada = self.preparaDadoNormaliza(fila)
            self.calculaMedias(latencia_salto, latencia_fluxo, fila)
            grande_vetor = np.concatenate(
                (latencia_salto, fluxo, fila), axis=None)
            grande_vetor_separados = np.concatenate(
                (latencia_salto_normalizado, latencia_fluxo_normalizado, fila_normalizada), axis=None)
            aux = np.array(grande_vetor, dtype=float)
            aux1 = grande_vetor.reshape(-1, 1)
            grande_vetor_normalizado = self.normalizaDados(aux1)
            tam = len(grande_vetor_normalizado)
            auxi = np.reshape(grande_vetor_normalizado, [1, tam])
            self.salvarLog("logGrandeVetorNorma.txt", "a", auxi)
            self.escreveArquivo1(auxi)
            self.salvarLog("logGrandeVetor.txt", "w", aux)
            self.escreveArquivo(aux)
            self.setMem(auxi)
        return auxi

