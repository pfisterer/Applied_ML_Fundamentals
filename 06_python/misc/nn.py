# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 11:17:13 2020

@author: Daniel Wehner
"""

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

import numpy as np

np.random.seed(100)


# -----------------------------------------------------------------------------
# Class Layer
# -----------------------------------------------------------------------------

class Layer:
    """
    Class Layer.
    Represents a layer in the neural network.
    """

    def __init__(self, n_input, n_neurons, activation="sigmoid", weights=None, bias=None):
        """
        Constructor.
        
        :param n_input:                 input size
        :param n_neurons:               number of neurons in the layer.
        :param activation:              type of activation function
                                            - tanh
                                            - sigmoid
        :param weights:                 weights for the layer
        :param bias:                    bias for the layer
        """
        # initialize weights and bias randomly
        self.weights = weights if weights is not None \
            else np.random.rand(n_neurons, n_input)
#        self.bias = bias if bias is not None \
#            else np.random.rand(n_neurons)
        self.activation = activation
        # filled later
        self.p = None
        self.z = None
        self.error = None


    def compute_act(self, x):
        """
        Computes the activation of this layer.
        
        :param x:                       layer input
        :return:                        layer output
        """
        self.p = self.weights @ x.T #+ self.bias
        self.z = self.__act_f(self.p)
        
        return self.z


    def __act_f(self, p):
        """
        Computes the activation for this layer depending on the
        activation function chosen.
        
        :param p:                       preactivation
        :return:                        activation
        """
        # linear activation if no function is given
        if self.activation is None:
            return p
        # tanh
        if self.activation == "tanh":
            return np.tanh(p)
        # sigmoid
        if self.activation == "sigmoid":
            return 1 / (1 + np.exp(-p))
        # relu
        if self.activation == "relu":
            return p * (p > 0)
        

    def d_act_f(self, p):
        """
        Computes the derivative of the activation function chosen.
        
        :param p:                       preactivation
        :return:                        activation derivative
        """
        if self.activation is None:
            return p
        if self.activation == "tanh":
            return 1 - np.tanh(p)**2
        if self.activation == "sigmoid":
            return (1 / (1 + np.exp(-p))) * (1 - (1 / (1 + np.exp(-p))))
        if self.activation == "relu":
            p[np.where(p < 0)] = 0
            return p

        return p


# -----------------------------------------------------------------------------
# Class NeuralNetwork
# -----------------------------------------------------------------------------

class NeuralNetwork:
    """
    Class NeuralNetwork.
    Represents a neural network.
    """

    def __init__(self):
        """
        Constructor.
        """
        # list to hold the layer objects
        self.__layers = []


    def add_layer(self, layer):
        """
        Adds a layer to the neural network.
        
        :param Layer layer:             layer to be appended
        """
        self.__layers.append(layer)
        
        
    def fit(self, X, y, alpha, n_epochs):
        """
        Trains the neural network using backpropagation.
        
        :param X:                       The input values
        :param y:                       The target values
        :param alpha:                   The learning rate
        :param n_epochs:                maximum number of epochs
        """
        y = self.__one_hot(y)
        
        # perform training epochs
        for i in range(n_epochs):
            print("Epoch", i)
            # stochastic gradient descent
            for j in range(len(X)):
                self.__backpropagation(X[j], y[j], alpha)
                
    
    def predict(self, X):
        """
        Computes the prediction for given unseen data.
        
        :param X:                       unseen data instances
        :return:                        predictions for unseen data instances
        """
        pred = []
        
        for x in X:
            y_pred = self.__feed_forward(x)
            pred.append(np.argmax(y_pred, axis=0))
            
        return np.asarray(pred)


    def __feed_forward(self, X):
        """
        Performs a forward pass on the data.
        
        :param X:                       network input
        :return:                        network output
        """
        # go over all layers
        for layer in self.__layers:
            X = layer.compute_act(X)

        return X
    

    def __backpropagation(self, X, y, alpha):
        """
        Performs the backward propagation algorithm and updates the layer weights.
        
        :param X:                       training data instances
        :param y:                       training data labels
        :param alpha:                   learning rate
        """
        # perform forward pass
        y_pred = self.__feed_forward(X)
        # loop over the layers backward
        for i in reversed(range(len(self.__layers))):
            layer = self.__layers[i]

            # output layer
            if layer == self.__layers[-1]:
                layer.error = 2 * (y_pred - y)
            # other layers
            else:
                next_layer = self.__layers[i + 1]
                layer.error = next_layer.error * next_layer.d_act_f(next_layer.p) @ next_layer.weights 

        # update the weights
        for i in range(len(self.__layers)):
            layer = self.__layers[i]
            input_to_use = np.atleast_2d(X if i == 0 else self.__layers[i - 1].z)
            grad = (layer.error * layer.d_act_f(layer.p) * input_to_use.T)
            if layer.weights.shape[1] != grad.shape[1]: grad = grad.T
            layer.weights -= alpha * grad
            
            
    def __one_hot(self, y):
        """
        Computes the one-hot representation of the labels.
        
        :param y:               class labels (without one-hot)
        :return:                one-hot class labels
        """
        y_one_hot = np.zeros((y.size, y.max() + 1))
        y_one_hot[np.arange(y.size), y] = 1
        
        return y_one_hot


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
        
if __name__ == "__main__":
    X = np.asarray([[1, 1]])
    y = np.asarray([1])
    
    # train a neural network
    clf = NeuralNetwork()
#    clf.add_layer(Layer(2, 2, "relu",
#        np.asarray([[0.19, -0.42], [-0.92, -0.28]]),
#        np.asarray([0, 0])))
#    clf.add_layer(Layer(2, 1, "tanh",
#        np.asarray([[0.61, -1.50]]),
#        np.asarray([0])))
#    clf.add_layer(Layer(1, 3, "sigmoid",
#        np.asarray([[1.50], [-0.81], [-0.24]]),
#        np.asarray([0, 0, 0])))
#    clf.add_layer(Layer(3, 2, "sigmoid",
#        np.asarray([[-1.40, -2.20, -0.27], [-0.81, -1.70, -0.73]]),
#        np.asarray([0, 0])))
    clf.add_layer(Layer(2, 2, "relu", np.asarray([[0.19, 0.42], [-0.94, 0.30]])))
    clf.add_layer(Layer(2, 2, "sigmoid", np.asarray([[-1.40, -2.20], [-0.81, -1.70]])))
    clf.fit(X, y, 0.01, 10000)
    
    print(clf.predict(X))
        