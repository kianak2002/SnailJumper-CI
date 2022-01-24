import copy
import random
import numpy as np

from player import Player
from matplotlib import pyplot as plt


class Evolution:
    def __init__(self):
        self.game_mode = "Neuroevolution"
        self.max_fitness = []
        self.avg_fitness = []
        self.min_fitness = []

    def next_population_selection(self, players, num_players):
        """
        Gets list of previous and current players (μ + λ) and returns num_players number of players based on their
        fitness value.

        :param players: list of players in the previous generation
        :param num_players: number of players that we return
        """
        # TODO (Implement top-k algorithm here)
        # '''ejbariiiiiiiii'''
        # players.sort(key=lambda x: x.fitness, reverse=True)  # sort descending
        # self.max_fitness.append(players[0].fitness)
        # self.min_fitness.append(players[num_players-1].fitness)
        # sum = 0
        # for i in range(len(players)):
        #     sum += players[i].fitness
        # self.avg_fitness.append(sum/len(players))
        # return players[: num_players]
        # TODO (Additional: Implement roulette wheel here)
        # TODO (Additional: Implement SUS here)

        # TODO (Additional: Learning curve)
        #  Q-TOURNAMENT
        '''emtiaziiiiiiiii'''
        Q = 5
        best_Q = []
        for i in range(num_players):
            Q_list = []
            for j in range(Q):
                Q_list.append(random.choice(players))
            Q_list.sort(key=lambda x: x.fitness, reverse=True)
            best_Q.append(Q_list[0])
        best_Q.sort(key=lambda x: x.fitness, reverse=True)
        self.max_fitness.append(best_Q[0].fitness)
        self.min_fitness.append(best_Q[num_players - 1].fitness)
        sum = 0
        for i in range(len(best_Q)):
            sum += best_Q[i].fitness
        self.avg_fitness.append(sum / len(best_Q))

        # print(self.max_fitness)
        # print(self.min_fitness)
        # print(self.avg_fitness)
        # plt.plot(self.avg_fitness, label="avg")
        # plt.plot(self.max_fitness, label='max')
        # plt.plot(self.min_fitness, label='min')
        # plt.show()

        return best_Q

    def generate_new_population(self, num_players, prev_players=None):
        """
        Gets survivors and returns a list containing num_players number of children.

        :param num_players: Length of returning list
        :param prev_players: List of survivors
        :return: A list of children
        """

        first_generation = prev_players is None
        if first_generation:
            return [Player(self.game_mode) for _ in range(num_players)]
        else:
            new_players = []
            '''emtiaziiiiiiiiiiii'''
            Q = 300
            best_Q = []
            for i in range(num_players):
                Q_list = []
                for j in range(Q):
                    Q_list.append(random.choice(prev_players))
                Q_list.sort(key=lambda x: x.fitness, reverse=True)
                best_Q.append(Q_list[0])
            parents = best_Q
            '''ejbariiiiiiiiiiiii'''
            # parents = prev_players  # parents
            #  cross over interchange
            for i in range(num_players):
                parent1 = random.choice(parents)
                parent2 = random.choice(parents)
                W1 = np.zeros((parent1.nn.layer2, parent1.nn.layer1))
                W2 = np.zeros((parent1.nn.layer3, parent1.nn.layer2))
                b1 = np.zeros((parent1.nn.layer2, 1))
                b2 = np.zeros((parent1.nn.layer3, 1))
                # cross over  for W1
                for j in range(len(parent1.nn.W1)):
                    if j % 2 == 0:
                        W1[j] = parent1.nn.W1[j]
                    else:
                        W1[j] = parent2.nn.W1[j]
                # cross over  for W2
                for j in range(len(parent1.nn.W2)):
                    if j % 2 == 0:
                        W2[j] = parent1.nn.W2[j]
                    else:
                        W2[j] = parent2.nn.W2[j]
                # cross over  for b1
                for j in range(len(parent1.nn.b1)):
                    if j % 2 == 0:
                        b1[j] = parent1.nn.b1[j]
                    else:
                        b1[j] = parent2.nn.b1[j]
                # cross over  for b2
                for j in range(len(parent1.nn.b2)):
                    if j % 2 == 0:
                        b2[j] = parent1.nn.b2[j]
                    else:
                        b2[j] = parent2.nn.b2[j]
                child = self.clone_player(parent1)
                #   mutation
                W1 = self.mutation(W1)
                W2 = self.mutation(W2)
                b1 = self.mutation(b1)
                b2 = self.mutation(b2)

                child.nn.W1 = W1
                child.nn.W2 = W2
                child.nn.b1 = b1
                child.nn.b2 = b2
                new_players.append(child)  # children

            return new_players

    '''
    chooses randomly with the probability of 0.2 to change some of cells of each children made
    it reset randomly a cell to zero
    '''

    def mutation(self, new_players):
        k = random.randint(0, len(new_players[0]) * len(new_players))  # change how many cells
        for j in range(len(new_players)):
            for i in range(k):
                yes_no = random.choices([0, 1], weights=(80, 20), k=1)  # yes or no
                if yes_no == 1:
                    change = random.randint(0, len(new_players[0]) * len(new_players))
                    new_players[change % len(new_players[0]), change % len(new_players)] = 0
                    new_players[j][0][change] = 0  # reset to zero
        return new_players

    def clone_player(self, player):
        """
        Gets a player as an input and produces a clone of that player.
        """
        new_player = Player(self.game_mode)
        new_player.nn = copy.deepcopy(player.nn)
        new_player.fitness = player.fitness
        return new_player
