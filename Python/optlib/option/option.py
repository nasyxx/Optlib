#!/usr/bin/python3
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
from optlib.tools import init_option


class Option:
    """Initialize An Option
    """

    def __init__(self, **kwgs):
        """Initialize this option.
        """
        self.option = init_option(**kwgs)
        self.price = Price(**self.option)
        self.greeks = Greeks(**self.option)

__all__ = ['Option']


if __name__ is '__main__':
    pass
