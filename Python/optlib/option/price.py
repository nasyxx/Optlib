#!/usr/bin/env python3
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
from optlib.tools import COLOR_CODES, RESET_COLOR, d1, d2, init_option
from scipy.stats import norm


class Price:
    """The Option Price.
    """
    _mc_n = 10000000
    _bopm_n = 1000

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
            title=COLOR_CODES['yellow'] + 'The Option Price' + RESET_COLOR,
            bsm=['B-S-M', self.bsm],
            mc=['Std Monte Carlo', self.monte_carlo],
            h_r1='=' * 40 + '\n',
            h_r2='+' + '-' * 17 + '+' + '-' * 22 + '+\n',
            crr_rn=['CRR Risk-Nature', self.crr_rn[-1][0]],
        )
        return ('{h_r1}| {title:<50}|\n{h_r1}'
                '| {bsm[0]:<16}| {bsm[1]:<20} |\n{h_r2}'
                '| {mc[0]:<16}| {mc[1]:<20} |\n{h_r2}'
                '| {crr_rn[0]:<16}| {crr_rn[1]:<20} |\n{h_r2}'
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
    def crr_rn(self):
        """CRR Risk-Nature Method Price
        """
        option = self.option
        n = self._bopm_n
        dt = option['t'] / n
        u = np.exp(option['sigma'] * dt ** 0.5)
        d = 1 / u  # math.exp(-option['sigma'] * dt ** 0.5)
        p = (np.exp(option['r'] * dt) - d) / (u - d)
        print(p)

        # The pricd binomial tree
        price_tree = np.array(
            [option['s'] * u ** i * d ** (n - i) for i in range(n + 1)]
        )[::-1]

        # The Option Price value_tree
        if option['flag'] is 'c':
            value_tree = np.maximum(price_tree - option['k'], 0)
        else:
            value_tree = np.maximum(option['k'] - price_tree, 0)

        # The value at earlier times
        option_price = [[*value_tree]]
        for i in range(n, 0, -1):
            value_tree[:i] = np.exp(-option['r'] * dt) * (
                p * value_tree[:i] +
                (1 - p) * value_tree[1:i + 1]
            )
            price_tree = price_tree * d
            if option['type']:
                if option['flag'] is 'p':
                    value_tree[:i] = np.maximum(option['k'] - price_tree[:i],
                                                value_tree[:i])
                else:
                    value_tree[:i] = np.maximum(price_tree[:i] - option['k'],
                                                value_tree[:i])
            option_price.append([*value_tree[:i]])
        return option_price

    @crr_rn.setter
    def crr_rn(self, value):
        """Change The N of binomial tree.

        The Value must be an integer
        """
        if isinstance(value, int):
            self._bopm_n = value
            return 'Set the N of binomial tree as {}'.format(value)
        else:
            raise TypeError('The N of binomial tree must be an integer')

    @property
    def monte_carlo(self):
        """The Standard Monte Carlo Simulation Price.

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


if __name__ is '__main__':
    pass
