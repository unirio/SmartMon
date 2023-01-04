# -*- coding: utf-8 -*-
# import subprocess
# import time
import numpy as np


class Agente:

    def __init__(self):
        #from . import Ambiente
        pass

    def recebeRecompensa(self):
        print("Agente: Metodo recebeRecompensa")

    def lerArquivoSaida(self):
        arquivo = open("/home/debora.job/projetos/proj5/frame1.txt", "r")
        resultado = arquivo.read()
        arquivo.close()

    def resultadoAmbiente(self, resultadoAmbiente):
        self.lerArquivoSaida()

    """
    Escolha da alta ou baixa telemetria será feita de acordo com o
    valor randômico que enviar para ambiente
    """

    def executaAcao(self):
        print("Agente: Dentro de ExecutaAção()")

        valor = np.random.normal()
        if(valor < 0.5):
            valor = 0
            return valor
        else:
            valor = 1
            return valor
