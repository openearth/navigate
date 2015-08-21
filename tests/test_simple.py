import unittest

import numpy as np

import navigate.algorithms


class TestAlgorithms(unittest.TestCase):
    """just works"""
    def test_ones(self):
        N = navigate.algorithms.N
        img = np.ones((N, N))
        x = np.arange(N)
        y = np.arange(N)
        extent = (0, 10, 0, 10)
        data = {
            'x': x,
            'y': y,
            'img': img,
            'extent': extent
        }
        options = {
            'min-depth': 0.3
        }
        results = navigate.algorithms.navigate(data, options)
        self.assertEqual(results['distance'], 0.0)
