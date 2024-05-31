import numpy as np

class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.weights_input_hidden = np.random.randn(input_size, hidden_size)
        self.weights_hidden_output = np.random.randn(hidden_size, output_size)

    def forward(self, inputs):
        hidden = np.dot(inputs, self.weights_input_hidden)
        hidden = np.maximum(0, hidden)  # ReLU activation
        output = np.dot(hidden, self.weights_hidden_output)
        return output

    def mutate(self, mutation_rate=0.01):
        self.weights_input_hidden += mutation_rate * np.random.randn(*self.weights_input_hidden.shape)
        self.weights_hidden_output += mutation_rate * np.random.randn(*self.weights_hidden_output.shape)

    def crossover(self, other):
        child = NeuralNetwork(self.input_size, self.hidden_size, self.output_size)
        child.weights_input_hidden = (self.weights_input_hidden + other.weights_input_hidden) / 2
        child.weights_hidden_output = (self.weights_hidden_output + other.weights_hidden_output) / 2
        return child
