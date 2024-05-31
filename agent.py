from neural_network import NeuralNetwork
import numpy as np

class Agent:
    def __init__(self):
        self.neural_network = NeuralNetwork(input_size=200, hidden_size=100, output_size=4)

    def get_action(self, state):
        output = self.neural_network.forward(state)
        return np.argmax(output)

    def mutate(self):
        self.neural_network.mutate()

    def crossover(self, other):
        child = Agent()
        child.neural_network = self.neural_network.crossover(other.neural_network)
        return child
