#!/usr/bin/python3
# -*- coding: utf-8 -*-
# pylint: disable=C0103
"""
  @Author: Nasy
  @Date: Dec 22, 2016
  @email: sy_n@me.com
  @file: optlib/options/price.py
  @license: MIT

  An Excited Python Script
"""

import numpy as np
from optlib.tools import d1, d2, init_option
from scipy.stats import norm


class Price:
    """The Option Price.
    """
    _mc_n = 10000000

    def __init__(self, **kwgs):
        """Initialize the option.
        """
        self.option = init_option(**kwgs)
        self.d1 = d1(**self.option)
        self.d2 = d2(**self.option)

    def __repr__(self):
        """Price Repr.
        """
        res = dict(
            title='The Option Price',
            bsm=['B-S-M', self.bsm],
            mc=['Monte Carlo', self.monte_carlo],
            h_r1='=' * 40 + '\n',
            h_r2='|' + '-' * 38 + '|\n'
        )
        return ('{title:<40}\n{h_r1}'
                '| {bsm[0]:<14}| {bsm[1]:<20} |\n{h_r2}'
                '| {mc[0]:<14}| {mc[1]:<20} |\n{h_r2}'
                .format(**res))

    @property
    def bsm(self):
        """The Black-Scholes-Merton Price
        """
        option = self.option
        if option['flag'] is 'c':
            return option['s'] * norm.cdf(self.d1) - option['k'] * np.exp(
                -option['r'] * option['t']
            ) * norm.cdf(self.d2)
        else:
            return option['k'] * np.exp(
                -option['r'] * option['t']
            ) * norm.cdf(-self.d2) - option['s'] * norm.cdf(-self.d1)

    @property
    def monte_carlo(self):
        """The Monte Carlo Simulation Price.

        Notes:
            Default simulation number is 10000000.
            To change the simulation number, do
                `Price.monte_carlo = new_number`
        """
        n = self._mc_n
        option = self.option
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

    @monte_carlo.setter
    def monte_carlo(self, value):
        """Change Monte Carlo Simulation number.

        The Value must be an integer
        """
        if isinstance(value, int):
            self._mc_n = value
            return 'Set the Monte Carlo Simulation number as {}'.format(value)
        else:
            raise TypeError('Monte Carlo Simulation number must be an integer')


def main():
    """main function
    """
    import doctest
    if not doctest.testmod().failed:
        print("Doctest passed")


if __name__ is '__main__':
    main()
