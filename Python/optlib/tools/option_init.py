#!/usr/bin/python3
# -*- coding: utf-8 -*-
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
                  'with CRR method. sigma={s}'.format(s=sigma))
            print(m)
            return sigma
        elif m is 2:
            if 'd' in kwgs:
                u = 1 / kwgs['d']
            elif 'sigma' in kwgs:
                u = math.e**(kwgs['sigma'] * math.sqrt(kwgs['t']))
            print('No "u" but "d" or "sigma" set, calculate "u" '
                  'with CRR method. u={u}'.format(u=u))
            print(m)
            return u
        elif m is 3:
            u = math.e**(0.25 * math.sqrt(kwgs['t']))
            print('No "u", "d" or "sigma" set, calculate "u" '
                  'with CRR method while sigma is default 0.25. '
                  'u={u}'.format(u=u))
            print(m)
            return u
        elif m is 4:
            if 'u' in kwgs:
                d = 1 / kwgs['u']
            elif 'sigma' in kwgs:
                d = math.e**(-kwgs['sigma'] * math.sqrt(kwgs['t']))
            print('No "d" but "u" or "sigma" set, calculate "d" '
                  'with CRR method. d={d}'.format(d=d))
            print(m)
            return d
        elif m is 5:
            d = math.e**(-0.25 * math.sqrt(kwgs['t']))
            print('No "u", "d" or "sigma" set, calculate "d" '
                  'with CRR method while sigma is default 0.25. '
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
    import doctest
    if not doctest.testmod().failed:
        print("Doctest passed")
