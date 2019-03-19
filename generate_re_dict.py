# coding=utf-8
import re
import collections


def sort_grammar(grammar):
    sort_temp = collections.OrderedDict()
    while len(sort_temp) != len(grammar):
        for key, value in grammar.items():
            if key not in sort_temp:
                if len(re.findall("\$[^$]+\$", value)) == 0:
                    sort_temp[key] = 0
                else:
                    val_list = re.findall("\$[^$]+\$", value)
                    val_flag = False
                    val_temp = 0
                    for val in val_list:
                        if val[1: -1] not in sort_temp:
                            val_flag = True
                            break
                        elif val_temp < sort_temp[val[1: -1]]:
                            val_temp = sort_temp[val[1: -1]]
                    if not val_flag:
                        sort_temp[key] = val_temp + 1
    sort_g = collections.OrderedDict()
    counter = 0
    while len(sort_g) != len(grammar):
        for key, value in sort_temp.items():
            if value == counter:
                sort_g[key] = grammar[key]
        counter += 1
    return sort_g


def generate_re_from_grammar_file(grammar_file):
    """
    get the dict(tag : re) from the grammar file
    """
    grammar = {}
    f = open(grammar_file, "r")
    for l in f:
        ls = l.strip()
        if ls[:2] == "//" or len(ls) == 0:
            continue
        l_list = ls.split("::")
        if l_list[0] not in grammar:
            grammar[l_list[0]] = [l_list[1]]
        else:
            grammar[l_list[0]].append(l_list[1])

    temp_grammar = {}
    for key, value in grammar.items():
        temp_grammar[key] = "|".join(value)

    grammar = sort_grammar(temp_grammar)

    re_list = [".", "+", "*", "/"]
    dict_re = collections.OrderedDict()
    for key, value in grammar.items():
        var_list = re.findall("\$[^$]+\$", value)
        if len(var_list):
            for var in var_list:
                value = value.replace(var, "(" + dict_re[var[1:-1]] + ")")
        else:
            value = value.split("|")
            for i in range(len(value)):
                if value[i] in re_list:
                    value[i] = "\\" + value[i]
            value = "|".join(value)
        dict_re[key] = value.replace(" ", "")
    return dict_re


def tag_sentence(sentence, grammar):
    tag = collections.OrderedDict()
    for key, value in grammar.items():
        end_pos = 0
        temp_tag = []
        pos = re.search(value, sentence)
        while pos:
            temp_tag.append((end_pos + pos.start(), end_pos + pos.end()))
            end_pos += pos.end()
            pos = re.search(value, sentence[end_pos:])
        if len(temp_tag) > 0:
            tag[key] = temp_tag
    return tag


