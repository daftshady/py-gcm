# -*- coding:utf-8 -*-

def enum(**enums):
    return type('Enum', (), enums)
 
def chunks(l, n):
    return [l[i:i+n] for i in range(0, len(l), n)]
