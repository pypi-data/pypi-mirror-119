#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test.py
@Contact :   haoheliu@gmail.com
@License :   (C)Copyright 2020-2100

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
9/14/21 11:02 AM   Haohe Liu      1.0         None
'''

from voicefixer import VoiceFixer

voicefixer = VoiceFixer()

voicefixer.restore(input="/Users/liuhaohe/Downloads/p361_056.wav",
                   output="/Users/liuhaohe/Downloads/p361_056_out.wav",
                   cuda=False)