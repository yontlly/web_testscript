# -*- coding: utf-8 -*-
"""
@Time : 2022/12/15 13:09
@Auth : tj
@Function : 实现关联的装饰器
"""


def get_relations(func):
    def wrapper(*args, **kwargs):
        s = args[0]
        params = list(args)
        for i in range(1, len(params)):
            param = params[i]
            for key in s.relations:
                r_key = '{' + key + '}'
                param = param.replace(r_key, s.relations.get(key))
            params[i] = param
        res = func(*params, **kwargs)
        return res

    return wrapper

