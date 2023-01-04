# -*- coding: utf-8 -*-
"""Classe do Agente Inteligente
Código adaptado de https://github.com/keon/deep-q-learning/blob/master/dqn.py
"""

import random
#import gym
import numpy as np
#import tensorflow as tf
#vmamlight
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from random import choice
import time
import sys

from ambiente import Ambiente
from configuracao import ConfiguraVariaveis

EPISODES = 20
TIMESTEPS = 32
TARG = []
TARGF = []
LISTARECOMP = []
LISTAACAO = []
LISTAMEDIAS = []


class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.985
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(128, input_dim=self.state_size, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def memorize(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # returns action

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma *
                          np.amax(self.model.predict(next_state)[0]))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=1)
            TARG.append(target)
            TARGF.append(target_f)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
            print("epsilon:", self.epsilon)

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)


if __name__ == "__main__":
    # env = gym.make('CartPole-v1')
    env = Ambiente()
    var_ambiente = ConfiguraVariaveis()

    #state_size = env.observation_space.shape[0]
    state_size = env.tamEstado(var_ambiente)

    #action_size = env.action_space.n
    action_size = env.tamAcao()

    agent = DQNAgent(state_size, action_size)

    # agent.load("./save/cartpole-dqn.h5")

    done = False
    batch_size = 16

    # estado s0 inicialiado com -1
    estado = []
    saidaDQN = open("../python_influxdb/DQNOut.txt", "w")
    saidaDQN.write("")
    saidaDQN.close()
    env.salvarLog("logDQNOut.txt", "w", "Log DQNout")
    env.salvarLog("logRecompensa.txt", "w","Log Recompensa")
    env.salvarLog("logSaidaPasso.txt", "w", "Log Saída Passo")
    cont = 0
    for e in range(EPISODES):
        tempoIni = time.time()
        #state = env.reset()
        state = env.inicializaEstado()

        state = np.reshape(state, [1, state_size])

        for t in range(TIMESTEPS):
            env.configEspelhamento()
            time.sleep(10)
            action = agent.act(state)
            env.interageAmbiente(action, cont)
            time.sleep(30)
            cont += 1
            setazero = open("../python_influxdb/file.txt", "w")
            setazero.write("0")
            setazero.close()
            time.sleep(10)
            next_state, reward, medias = env.passos(action)
            time.sleep(5)

            if t == TIMESTEPS - 1:
                done = True
                print("done", done)

            next_state = np.reshape(next_state, [1, state_size])
            agent.memorize(state, action, reward, next_state, done)
            state = next_state
            print("e:", e, "t:", t)
            env.fechaJanelaEbpf()
            time.sleep(5)

            LISTAACAO.append(action)
            LISTARECOMP.append(reward)
            LISTAMEDIAS.append(medias)
            if len(agent.memory) > batch_size:
                agent.replay(batch_size)
            if e % 10 == 0:
                agent.save("../python_influxdb/cartpole-dqn.h5")
            tempoFim = time.time()
            tempoEpisodio = (tempoFim - tempoIni)

            if done:
                print("episode: {}/{}, score: {}, e: {:.2}, action: {}, episodeTime: {}, reward: {}, listacao: {}, listareward: {}, medias: {}"
                      .format(e, EPISODES, t, agent.epsilon, action, tempoEpisodio, reward, LISTAACAO, LISTARECOMP, LISTAMEDIAS))
                env.saidaDQN(e, EPISODES, t, agent.epsilon, action,
                             tempoEpisodio, reward, LISTAACAO, LISTARECOMP, LISTAMEDIAS)
                break

        done = False
        cont += 1
        print(LISTAACAO)
        print(LISTARECOMP)
        LISTAACAO = []
        LISTARECOMP = []
        LISTAMEDIAS = []
