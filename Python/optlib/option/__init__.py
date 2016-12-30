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


from optlib.option.option import Option


def main():
    """main func
    """
    option = Option(k=30, s=30, t=1, r=0.04, sigma=0.71)
    print(option)


if __name__ == '__main__':
    main()
