#!/usr/bin/python3
# -*- coding: utf-8 -*-
# pylint: disable=C0103
"""
  @Author: Nasy
  @Date: Dec 22, 2016
  @email: sy_n@me.com
  @file: optlib/option/greeks.py
  @license: MIT

  An Excited Python Script
"""
import math

from optlib.tools import d1, d2, init_option
from scipy.stats import norm


class Greeks:
    """Greeks
    """

    def __init__(self, **kwgs):
        self.option = init_option(**kwgs)
        self.d1 = d1(**self.option)
        self.d2 = d2(**self.option)
        self._d_d1 = 1 / (2 * math.pi) ** 0.5 * (
            math.exp(- (self.d1 ** 2) / 2))

    def __repr__(self):
        """Greeks Repr.
        """
        res = dict(
            title='The Option Greeks',
            delta=['Delta(Δ)', self.delta],
            theta=['Theta(Θ)', self.theta],
            rho=['rho(ρ)', self.rho],
            gamma=['Gamma(Γ)', self.gamma],
            vega=['Veta(ν)', self.vega],
            h_r1='=' * 40 + '\n',
            h_r2='|' + '-' * 38 + '|\n'
        )
        return ('{title:<40}\n{h_r1}'
                '| {delta[0]:<10}| {delta[1]:<24} |\n{h_r2}'
                '| {theta[0]:<10}| {theta[1]:<24} |\n{h_r2}'
                '| {rho[0]:<10}| {rho[1]:<24} |\n{h_r2}'
                '| {gamma[0]:<10}| {gamma[1]:<24} |\n{h_r2}'
                '| {vega[0]:<10}| {vega[1]:<24} |\n{h_r2}'
                .format(**res))

    @property
    def delta(self):
        """Greek Delta
        """
        option = self.option
        if option['flag'] is 'c':
            return norm.cdf(self.d1)
        else:
            return -norm.cdf(self.d1)

    @property
    def theta(self):
        """Greek Theta
        """
        option = self.option
        if option['flag'] is 'c':
            return -(
                option['s'] * self._d_d1 * option['sigma']
            ) / (
                2 * (option['t'] ** (1 / 2))
            ) - (
                option['r'] * option['k'] * math.exp(
                    -option['r'] * option['t']
                ) * norm.cdf(self.d2)
            )
        else:
            return -(
                option['s'] * self._d_d1 * option['sigma']
            ) / (
                2 * (option['t'] ** (1 / 2))
            ) - (
                option['r'] * option['k'] * math.exp(
                    -option['r'] * option['t']
                ) * norm.cdf(-self.d2)
            )

    @property
    def rho(self):
        """Greek rho
        """
        option = self.option
        if option['flag'] is 'c':
            return option['t'] * option['k'] * math.exp(
                -option['r'] * option['t']
            ) * norm.cdf(self.d2) * .01
        else:
            return option['t'] * option['k'] * math.exp(
                -option['r'] * option['t']
            ) * norm.cdf(-self.d2) * .01

    @property
    def gamma(self):
        """Greek Gamma
        """
        option = self.option
        return (self._d_d1) / (
            option['s'] * option['sigma'] *
            (option['t'] ** (1 / 2))
        )

    @property
    def vega(self):
        """Greek Vega
        """
        option = self.option
        return option['s'] * (option['t'] ** (1 / 2)) * self._d_d1


def main():
    """main function
    """
    pass


if __name__ is '__main__':
    main()
