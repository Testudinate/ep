#!/usr/bin/env python
# coding:utf-8
'''

''' 

def select(object,property,value):
    '''
    '''
    if object:
        for c in object:
            if c.properties[property]==value:
                return c