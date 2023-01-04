# -*- coding: utf-8 -*-

import json


class ConfiguraVariaveis():
    def __init__(self):
        with open('../ag_aleatorio/configura.json') as f:
            self.data = json.load(f)

            self.qtdSwsMin = self.data['qtdSwsMin']
            self.qtdSwsMax = self.data['qtdSwsMax']
            self.valorSws = self.data['valorSws']
            self.nosPossiveis = self.data['nosPossiveis']
            self.qtdMaxPassos = self.data['qtdMaxPassos']

     # retorna a qtd mínima de switches

    def getQtdSwsMin(self):
        var = int(self.qtdSwsMin)
        return var

    # retorna a qtd máxima de switches

    def getQtdSwsMax(self):
        var = int(self.qtdSwsMax)
        return var

    # retorna o a qtd de valores relacionado ao tempo do iperf (ex. 30)

    def getValorSws(self):
        var = int(self.valorSws)
        return var

    # retorna a descrição dos switches que podem ser usados na topologia

    def getNosPossiveis(self):
        return self.nosPossiveis

    # retorna a qtd máxima de iterações que o agente fará para completar um episódio

    def getQtdMaxPassos(self):
        var = int(self.qtdMaxPassos)
        return var
