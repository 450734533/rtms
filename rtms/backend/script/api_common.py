# coding -*- utf-8 -*-

def dict_traversal(dict_result, exk, result_list):
    if isinstance(dict_result, dict):
        for rk in dict_result.keys():
            if rk == exk:
                result_list.append(dict_result[exk])
            dict_traversal(dict_result[rk], exk, result_list)
    else:
        pass
    return result_list, exk


def get_result(dict_expect, dict_result):
    result_list = []
    expect_list = []
    if isinstance(dict_expect, dict):
        for exk in dict_expect.keys():
            result_list, exk = dict_traversal(dict_result, exk, result_list)
            expect_list.append(dict_expect[exk])
    else:
        print 'expect must be dict'
    if result_list == expect_list:
        return True
    else:
        return False

