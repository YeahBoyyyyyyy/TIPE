import numpy as np
import matplotlib.pyplot as plt

layer_outputs = [[4.8, 1.21, 2.385],
                 [8.9, -1.81, 0.2],
                 [1.41, 1.051, 0.026]]

exp_values = np.exp(layer_outputs)

norm_values = exp_values / np.sum(exp_values, axis=1, keepdims=True)

print(norm_values)
print(np.sum(norm_values))








'''
# Ceci est le softmax il permet à des sorties de neuronnes d'être cohérentes puisque cela rééquilibre les
# valeurs de sortie 
## CECI EST APPELE LA FONCTION SOFTMAX
layer_output = [4.8, 1.21, 2.385]

exp_values = np.exp(layer_output)

norm_values = exp_values / np.sum(exp_values)

print(norm_values)

####

import numpy as np

np.random.seed(0)

X = [[1.2, 3, 2.1, 2],
    [2.3, 4.0, -3.1, 0.3],
    [3.0, -2.1, -1.1, 2.6]]

class Layer_Dense:
    def __init__(self, n_inputs, n_neurons):
        self.weights = 0.1*np.random.randn(n_inputs, n_neurons)
        self.biases = np.zeros((1, n_neurons))
    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases

layer1 = Layer_Dense(4,6)
layer2 = Layer_Dense(6,2)

layer1.forward(X)
print(layer1.output)
layer2.forward(layer1.output)
print(layer2.output)

weights = [[2.5, -0.5, 1.7, -3],
          [0.5, -1.32, 2.1, -0.2],
          [3, -0.8, -1.4, 3]]

biases = [3 ,1 ,0.5]

weights2 = [[0.1, -0.14, 0.5],
          [-0.5, 0.12, -0.33],
          [-0.44, 0.73, -0.13]]

biases2 = [-1, 2, -0.5]

layer1_outputs = np.dot(inputs, np.array(weights).T) + biases
layer2_outputs = np.dot(layer1_outputs, np.array(weights2).T) + biases

print(layer2_outputs)

layer_outputs = []
for neuron_weights, neuron_bias in zip(weights, biases):
    neuron_output = 0
    for n_input, weight in zip(inputs, neuron_weights):
        neuron_output += n_input*weight
    neuron_output += neuron_bias
    layer_outputs.append(neuron_output)

print(layer_outputs)
output = [inputs[0]*weights[0][0] + inputs[1]*weights[0][1] + inputs[2]*weights[0][2] + inputs[3]*weights[0][3] + biases[0],
          inputs[0]*weights[1][0] + inputs[1]*weights[1][1] + inputs[2]*weights[1][2] + inputs[3]*weights[1][3] + biases[1],
          inputs[0]*weights[2][0] + inputs[1]*weights[2][1] + inputs[2]*weights[2][2] + inputs[3]*weights[2][3] + biases[2]]
'''