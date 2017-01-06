#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
  @Author: Nasy
  @Date: Dec 29, 2016
  @email: sy_n@me.com
  @file: optlib/option/option.py
  @license: MIT

  An Excited Python Script
"""
from optlib.option.greeks import Greeks
from optlib.option.price import Price
from optlib.tools import COLOR_CODES, RESET_COLOR, init_option


class Option:
    """Initialize An Option
    """

    def __init__(self, **kwgs):
        """Initialize this option.
        """
        self.option = init_option(**kwgs)
        print(self)

    def __repr__(self):
        """Option Repr
        """
        res = dict(
            h_r1='=' * 31 + '\n',
            h_r2='+' + '-' * 29 + '+\n',
            k=['K', self.option['k']],
            s=['S', self.option['s']],
            r=['Risk-Free Rate', self.option['r']],
            t=['T', self.option['t']],
            sigma=['σ', self.option['sigma']],
            type='American' if self.option['type'] else 'European',
            flag='Call Option' if self.option['flag'] is 'c' else 'Put Option',
        )
        return ('{h_r1}| '.format(**res) + COLOR_CODES['yellow'] +
                'The {type} {flag:<14} |'.format(**res) + RESET_COLOR +
                '\n{h_r1}'
                '| {k[0]:<15}| {k[1]:<10} |\n{h_r2}'
                '| {s[0]:<15}| {s[1]:<10} |\n{h_r2}'
                '| {r[0]:<15}| {r[1]:<10} |\n{h_r2}'
                '| {sigma[0]:<15}| {sigma[1]:<10.8f} |\n{h_r2}'
                '| {t[0]:<15}| {t[1]:<10} |\n{h_r2}\n\n'.format(**res) +
                self.greeks.__repr__() + '\n\n' + self.price.__repr__())

    @property
    def price(self):
        """The Price of this Option
        """
        return Price(**self.option)

    @property
    def greeks(self):
        """The Greeks of this Option
        """
        return Greeks(**self.option)

__all__ = ['Option']


if __name__ is '__main__':
    pass
