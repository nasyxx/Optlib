#!/usr/bin/python3
# -*- coding: utf-8 -*-
# pylint: disable=C0103
"""
  @Author: Nasy
  @Date: Dec 22, 2016
  @email: sy_n@me.com
  @file: optlib/tools/__init__.py
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
    # flag, type, r
    option = {
        **option,
        **{
            'flag': kwgs['flag'] if 'flag' in kwgs else 'c',
            'type': kwgs['type'] if 'type' in kwgs else 0,
            'r': kwgs['r'] if 'r' in kwgs else float(0.03)
        }
    }

    # sigma, u, d
    def _s_ud(m):
        """sigma, u & d
        """
        if m is 0:
            print('No "sigma" or "u, d" set, use default sigma 0.25')
            print(m)
            return 0.25
        elif m is 1:
            if ('u' in kwgs and 'd' in kwgs) or 'u' in kwgs:
                sigma = math.log(kwgs['u']) / math.sqrt(kwgs['t'])
            elif 'd' in kwgs:
                sigma = -math.log(kwgs['d']) / math.sqrt(kwgs['t'])
            print('No "sigma" but "u" or "d" set, calculate "sigma" '
                  'with Black-Scholes-Merton. sigma={s}'.format(s=sigma))
            print(m)
            return sigma
        elif m is 2:
            if 'd' in kwgs:
                u = 1 / kwgs['d']
            elif 'sigma' in kwgs:
                u = math.e**(kwgs['sigma'] * math.sqrt(kwgs['t']))
            print('No "u" but "d" or "sigma" set, calculate "u" '
                  'with Black-Scholes-Merton while u*d = 1. u={u}'.format(u=u))
            print(m)
            return u
        elif m is 3:
            u = math.e**(0.25 * math.sqrt(kwgs['t']))
            print('No "u", "d" or "sigma" set, calculate "u" '
                  'with Black-Scholes-Merton while sigma is default 0.25. '
                  'u={u}'.format(u=u))
            print(m)
            return u
        elif m is 4:
            if 'u' in kwgs:
                d = 1 / kwgs['u']
            elif 'sigma' in kwgs:
                d = math.e**(-kwgs['sigma'] * math.sqrt(kwgs['t']))
            print('No "d" but "u" or "sigma" set, calculate "d" '
                  'with Black-Scholes-Merton while u*d = 1. d={d}'.format(d=d))
            print(m)
            return d
        elif m is 5:
            d = math.e**(-0.25 * math.sqrt(kwgs['t']))
            print('No "u", "d" or "sigma" set, calculate "d" '
                  'with Black-Scholes-Merton while sigma is default 0.25. '
                  'd={d}'.format(d=d))
            print(m)
            return d

    option = {
        **option,
        **{
            'sigma': float(kwgs['sigma']) if 'sigma' in kwgs else (
                _s_ud(1) if 'u' in kwgs or 'd' in kwgs else _s_ud(0)
            ),
            'u': float(kwgs['u']) if 'u' in kwgs else (
                _s_ud(2) if 'd' in kwgs or 'sigma' in kwgs else _s_ud(3)
            ),
            'd': float(kwgs['d']) if 'd' in kwgs else (
                _s_ud(4) if 'u' in kwgs or 'sigma' in kwgs else _s_ud(5)
            ),
        },
    }
    # try:
    #     option['sigma'] = float(kwgs['sigma'])
    # except KeyError:
    #     try:
    #         option['u'] = float(kwgs['u'])
    #         option['d'] = float(kwgs['d'])
    #     except KeyError as e:
    #         if (e is 'u') and 'd' not in kwgs:
    #             warn('No "u" or "d" set, calculate them with bsm',
    #                  DeprecationWarning)
    #             option['d'] = math.e ** (
    #                 -option['sigma'] * math.sqrt(option['t'])
    #             )
    #             option['u'] = math.e ** (
    #                 option['sigma'] * math.sqrt(option['t'])
    #             )
    #         elif e is 'u':

    # option = {}
    # try:
    #     option['k'] = float(kwgs['k'])ipyt
    #     option['s'] = float(kwgs['s'])
    # except KeyError as e:
    #     print(e)
    #     if e is 'k':
    #         raise KeyError('Initialize the Option False. No Strike Price')
    #     elif e is 's':
    #         raise KeyError('Initialize the Option False. '
    #                        'No Underlying Asset Price')
    # try:
    #     option['t'] = float(kwgs['day'] / 365)
    # except KeyError:
    #     try:
    #         option['t'] = float(kwgs['t'])
    #     except KeyError:
    #         option['t'] = float(90 / 365)
    #         print('No times set. Use default 90/365 years')
    # try:
    #     option['sigma'] = float(kwgs['sigma'])
    # except KeyError:
    #     option['sigma'] = float(0.25)
    #     print('No sigma set. Use default 0.25')
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
    # try:
    #     option['r'] = float(kwgs['r'])
    # except KeyError:
    #     option['r'] = float(0.03)
    #     print('No risk-free rate set. Use default 0.03')
    # try:
    #     option['flag'] = kwgs['flag']
    # except KeyError:
    #     option['flag'] = 'c'
    #     print('No flag set. Use default CALL')
    # try:
    #     option['type'] = kwgs['type']
    # except KeyError:
    #     option['type'] = 0
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
