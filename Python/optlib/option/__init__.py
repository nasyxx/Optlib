#!/usr/bin/python3
# -*- coding: utf-8 -*-
# pylint: disable=C0103, E0401
"""
  @Author: Nasy
  @Date: Dec 22, 2016
  @email: sy_n@me.com
  @file: optlib/options/__init__.py
  @license: MIT

  An Excited Python Script
"""

from optlib.option.price import bsm, monte_carlo
from optlib.tools import d1, d2, init_option


class Option:
    """Initialize An Option
    """

    def __init__(self, **kwgs):
        """Initialize this option
        """
        self.option = init_option(**kwgs)
        self.d1 = d1(**self.option)
        self.d2 = d2(**self.option)

    def price(self, method='bsm'):
        """Calculate this option price

        Default method is 'Black-Scholes-Merton'
        """
        if method is 'bsm':
            return bsm(**self.option)
        elif method is 'mc':
            return monte_carlo(**self.option)
        else:
            pass


def main():
    """main func
    """
    option = Option(k=28, s=30, t=1, r=0.04, sigma=0.71)
    print(option)


if __name__ == '__main__':
    main()
