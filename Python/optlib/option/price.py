#!/usr/bin/python3
# -*- coding: utf-8 -*-
# pylint: disable=C0103, E0401
"""
  @Author: Nasy
  @Date: Dec 22, 2016
  @email: sy_n@me.com
  @file: optlib/options/price.py
  @license: MIT

  An Excited Python Script
"""
import math

import numpy as np
import optlib.tools as optool
from scipy.stats import norm


def bsm(**option):
    """The Black-Scholes-Merton Price
    """
    option = optool.init_option(**option)
    d1 = optool.d1(**option)
    d2 = optool.d2(**option)
    if option['flag'] is 'c':
        return option['s'] * norm.cdf(d1) - option['k'] * math.exp(
            -option['r'] * option['t']
        ) * norm.cdf(d2)
    else:
        return option['k'] * math.exp(
            -option['r'] * option['t']
        ) * norm.cdf(-d2) - option['s'] * norm.cdf(-d1)


def monte_carlo(n=100000000, **option):
    """The Monte Carlo Simulation Price
    """
    option = optool.init_option(**option)
    n_randn = np.random.standard_normal(n)

    st = option['s'] * np.exp(
        (option['r'] - 0.5 * option['sigma']**2) * option['t'] +
        option['sigma'] * np.sqrt(option['t']) * n_randn
    )
    if option['flag'] is 'c':
        ht = np.maximum(st - option['k'], 0)
    else:
        ht = np.maximum(option['k'] - st, 0)
    return np.exp(-option['r'] * option['t']) * np.sum(ht) / n


def main():
    """main function
    """
    import doctest
    if not doctest.testmod().failed:
        print("Doctest passed")


if __name__ is '__main__':
    main()
