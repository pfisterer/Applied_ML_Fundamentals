#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 17:08:22 2019

@author: Daniel Wehner
"""

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

# numpy
# -----------------------------------------------------------------------------
import numpy as np

# sklearn
# -----------------------------------------------------------------------------
from sklearn.datasets import make_classification
from sklearn.datasets import make_circles
from sklearn.datasets import make_regression
from sklearn.datasets import make_swiss_roll
from sklearn.datasets import make_moons


# -----------------------------------------------------------------------------
# Class DataCreator
# -----------------------------------------------------------------------------

class DataCreator:
    """
    Class Data Creator.
    """
    
    def make_classification(self, name="circles", n_classes=2):
        """
        Creates a binary classification data set.
        
        :param name:            name of the data set to be generated
                                    - custom
                                    - linear (linearly separable, sklearn)
                                    - circles (sklearn)
                                    - moons (sklearn)
                                    - swiss (swiss roll, sklearn)
        :param n_classes:       number of classes (only needed for name="linear")
        :return:                X, y (data features and labels)
        """
        # cusotm data set
        if name == "custom":
            X = np.asarray([
                [3.00, 1.00], [3.20, 2.20], [3.15, 4.80],
                [3.35, 1.20], [3.05, 3.50], [3.55, 2.85],
                [1.50, 2.25], [2.88, 2.18], [1.95, 4.00],
                [3.01, 2.95], [2.85, 3.01], [5.85, 2.20],
                [4.19, 4.00], [5.15, 3.50], [5.07, 2.89],
                [4.87, 3.54], [4.44, 3.78], [4.48, 3.94],
                [5.51, 3.80]
            ])
            y = np.asarray(
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
            )
            
        # random data generated by sklearn
        elif name == "linear":
            X, y = make_classification(
                n_samples=200, n_features=2, n_redundant=0,
                n_informative=2, n_clusters_per_class=1,
                n_classes=n_classes, class_sep=3.25, random_state=42
            )
            
        # non linear data set
        elif name == "non_linear":
            # define means and covariance matrix
            mean1 = [-1, 2]; mean2 = [1, -1]
            mean3 = [4, -4]; mean4 = [-4, 4]
            covar = [[1.0,0.8], [0.8, 1.0]]
            
            # generate random data
            X = np.random.multivariate_normal(mean1, covar, 50)
            X = np.vstack((X, np.random.multivariate_normal(mean3, covar, 50)))
            X = np.vstack((X, np.random.multivariate_normal(mean2, covar, 50)))
            X = np.vstack((X, np.random.multivariate_normal(mean4, covar, 50)))
            y = np.ones(200); y[100:] = 0
            
        # circular data
        elif name == "circles":
            X, y = make_circles(n_samples=400, factor=0.3, noise=0.2)
            
        # moon data set
        elif name == "moons":
            X, y = make_moons(150, noise=0.07, random_state=21)
            
        # swiss roll data set
        else:
            X, y = make_swiss_roll(2000, 0.00)
        
        return X, y
    
    
    def make_regression(self, name="sine"):
        """
        Creates a regression data set.
        
        :param name:            name of the data set to be used
                                    - custom
                                    - sklearn
                                    - sine
        :return:                X, y (data features and labels)        
        """
        # custom data set
        if name == "custom":
            X = np.array([-1.50, -0.25, 0.00, 1.00, 5.00, 5.50, 10.50, 11.50])
            y = np.array([-1.60, 0.50, 0.80, -2.00, 0.00, 1.00, 3.00, 3.00])
            X = X.reshape(-1, 1)
        
        # random data set generated by sklearn
        elif name == "sklearn":
            X, y = make_regression(n_samples=20, n_features=1, noise=10.0)
        
        # sine wave data set
        elif name == "sine":
            X = np.linspace(0, 5, 100)
            y = np.sin(X * 1.5 * np.pi) + np.random.normal(loc=0, scale=0.25, size=100)
            X = X.reshape(-1, 1)
            
            ind = np.where((X > 1.75) & (X < 3))
            X = np.delete(X, ind, 0)
            y = np.delete(y, ind, 0)
            
        return X, y
    