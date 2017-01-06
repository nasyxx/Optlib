#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0103
"""
  @Version: {version}
  @Author: Nasy
  @Date: Dec 29, 2016
  @email: sy_n@me.com
  @file: optlib/tools/option_init.py
  @license: MIT

  An Excited Python Script
"""

import math
from warnings import warn


def init_option(**kwgs):
    """Initialize An Option.
    """
    option = {}

    # k & s
    try:
        option['k'] = float(kwgs['k'])
        option['s'] = float(kwgs['s'])
    except KeyError as e:
        warn_message = {
            's': 'No Strike Price',
            'k': 'No Underlying Asset Price'
        }
        raise KeyError('Initialize the Option False. '
                       '{e}'.format(e=warn_message[e]))

    # t
    try:
        option['t'] = float(kwgs['D']) / 365 \
            if 'D' in kwgs else float(kwgs['day'])
        if 't' in kwgs:
            print('Prefer using "day" to "t"', DeprecationWarning)
    except KeyError:
        try:
            option['t'] = float(kwgs['t'])
        except KeyError:
            option['t'] = float(90 / 365)
            warn('No "T" or "day" set, use default "t = 90/365"',
                 DeprecationWarning)
    # flag, type, r, sigma
    option = {
        **option,
        **{
            'flag': kwgs.get('flag', 'c'),
            'type': kwgs.get('type', 0),
            'r': kwgs.get('r', 0.03),
            'sigma': kwgs.get('sigma', 0.25)
        }
    }

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
    return d1(**option) - option['sigma'] * option['t'] ** 0.5


__all__ = ['init_option', 'd1', 'd2']

if __name__ == '__main__':
    pass
