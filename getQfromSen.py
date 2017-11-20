# coding=utf-8
import re


GRAMMAR = {
    # file(**) represent the var is denoted in file.
    # string represents the var is denoted by enumeration.
    "adv": "大 小",  # 一大堆苹果、五小队士兵
    "CFC": "分之 比",  # Chinese Fraction Connective
    "CN": "一 二 三 四 五 六 七 八 九 壹 贰 叁 肆 伍 陆 柒 捌 玖 两",  # Chinese Number
    "CRP": "点",  # Chinese Radix Point
    "idioms": "file(resource/idioms)",
    "SMC": "零",  # Skip Magnitude Connective
    "Magnitude": "十 百 千 拾 佰 仟 万 亿",
    "n_suffix": "来 多 余",  # noun suffix
    "ONP": "第",  # Ordinal Number Prefix
    "prefix": "file(resource/prefix)",
    "q_con": "/ * 每",  # quantity connective
    "n_con": "~ 到",
    "q_suffix": "file(resource/q_suffix)",  # quantity suffix
    "quantity": "file(resource/quantity)",
    "tokens":  "十 百 千 万 亿 零 一 二 三 四 五 六 七 八 九 壹 贰 叁 肆 伍 陸 柒 捌 玖 两 0 1 2 3 4 5 6 7 8 9",
    # $**$ represent the var is denoted above.
    # . * + () | ? \d are re grammar representation.
    "arabic_number": "[-+]?(\d+(\.\d*)?)([eE][-+]?\d+)?([\/:](\d+(\.\d*)?)([eE][-+]?\d+)?)?%?‰?|\d+(,\d{3})+",
    "Chinese_number": "(($CN$ $Magnitude$+ $SMC$?)+ $CN$ | $CN$ ) ($CRP$ $CN$+)?",
    "Chinese_Fraction_number": "$Chinese_number$ $CRP$ $Chinese_number$",
    "number": "$arabic_number$ | $Chinese_Fraction_number$ | $Chinese_number$ | $arabic_number$ $Magnitude$",
    "Ordinal Number": "$ONP$ $number$",
    "Quantity_phrase": "$CN$ $adv$ $quantity$ | $prefix$? $number$ $quantity$? $q_suffix$?"
}


def get_re_from_grammar(grammar):
    """
    get the dict(tag : re) from the grammar file
    :param grammar:
    :return:
    """
    re_list = [".", "+", "*", "/"]
    grammar = dict(grammar)
    dict_re = dict()
    for key, value in grammar.items():
        var_list = re.findall("\$[^\$]+\$", value)
        if len(var_list):
            for var in var_list:
                    value = value.replace(var, "(" + dict_re[var[1:-1]] + ")")
        elif len(re.findall(" ", value)):
            value = value.split(" ")
            for i in range(len(value)):
                if value[i] in re_list:
                    value[i] = "\\" + value[i]
            value = "|".join(value)
        elif re.search("file(.+)", value):
            file_pos = value[5:-1]
            with open(file_pos, "r", encoding='utf-8') as fo:
                value = fo.read().split(" ")
                value = "|".join(value)
        dict_re[key] = value.replace(" ", "")
    return dict_re


def tag_sentence(sentence, grammar):
    tag = dict()
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


if __name__ == "__main__":
    g = GRAMMAR
    s = "我有两个苹果，大约4斤多，有一大堆梨。"
    d = get_re_from_grammar(g)
    res = tag_sentence(s, d)
    res_word = dict()
    for k, v in res.items():
        temp_l = []
        for vv in v:
            temp_l.append(s[vv[0]:vv[1]])
        res_word[k] = temp_l
    for k in res.keys():
        print(k, res[k], res_word[k])
