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

from optlib.tools.option_init import d1, d2, init_option

__all__ = ['d1', 'd2', 'init_option']


def main():
    """main function
    """
    import doctest
    if not doctest.testmod().failed:
        print("Doctest passed")

if __name__ == '__main__':
    main()
