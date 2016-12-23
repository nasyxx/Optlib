#!/usr/bin/python3
# -*- coding: utf-8 -*-
# pylint: disable=C0103, R0912, R0915
"""
  @Author: Nasy
  @Date: Dec 22, 2016
  @email: sy_n@me.com
  @file: optlib/tools/__init__.py
  @license: MIT

  An Excited Python Script
"""

import math


def init_option(**kwgs):
    """Initialize An Option.
    """
    option = {}
    try:
        option['k'] = float(kwgs['k'])
        option['s'] = float(kwgs['s'])
    except KeyError as e:
        print(e)
        if e is 'k':
            raise KeyError('Initialize the Option False. No Strike Price')
        elif e is 's':
            raise KeyError('Initialize the Option False. '
                           'No Underlying Asset Price')
    try:
        option['t'] = float(kwgs['day'] / 365)
    except KeyError:
        try:
            option['t'] = float(kwgs['t'])
        except KeyError:
            option['t'] = float(90 / 365)
            print('No times set. Use default 90/365 years')
    try:
        option['sigma'] = float(kwgs['sigma'])
    except KeyError:
        option['sigma'] = float(0.25)
        print('No sigma set. Use default 0.25')
    # try:
    #     option['u'] = float(kwgs['u'])
    #     option['d'] = float(kwgs['d'])
    # except KeyError as e:
    #     if e is 'u':
    #         try:
    #             option['d'] = float(kwgs['d'])
    #             print('No "u" set, initialize it while "u * d = 1"')
    #             option['u'] = float(1 / option['d'])
    #         except KeyError:
    #             print('No "u" or "d" set, initialize it with bsm')
    #             option['d'] = math.e ** (
    #                 -option['sigma'] * math.sqrt(option['t'])
    #             )
    #             option['u'] = math.e ** (
    #                 option['sigma'] * math.sqrt(option['t'])
    #             )
    #     else:
    #         print('No "d" set, initialize it while "u * d = 1"')
    #         option['d'] = float(1 / option['u'])
    try:
        option['r'] = float(kwgs['r'])
    except KeyError:
        option['r'] = float(0.03)
        print('No risk-free rate set. Use default 0.03')
    try:
        option['flag'] = kwgs['flag']
    except KeyError:
        option['flag'] = 'c'
        print('No flag set. Use default CALL')
    try:
        option['type'] = kwgs['type']
    except KeyError:
        option['type'] = 0
    return option


def d1(**kwgs):
    """Calculate the d1 component
    """
    option = init_option(**kwgs)
    numerator = math.log(option['s'] / option['k']) + (
        option['r'] +
        (option['sigma'] ** 2) / 2.0
    ) * option['t']
    denominator = option['sigma'] * (option['t'] ** 0.5)
    return numerator / denominator


def d2(**kwgs):
    """Calculate the d2 component
    """
    option = init_option(**kwgs)
    return d1(**option) - option['sigma'] * option['t']**0.5


def main():
    """main function
    """
    D1 = d1(k=28, s=30, t=1, r=0.04, sigma=0.71)
    D2 = d2(k=28, s=30, t=1, r=0.04, sigma=0.71)

    print(D1)
    print(D2)

if __name__ == '__main__':
    main()
