import re


def token_in_line(token_list, line):
    for token in token_list:
        if token in line:
            return True
    return False


def tag_cn_num(tag_list, l_taged, line):
    tag_f = tag_list[0]
    line_l = len(line)
    for l_i in range(line_l):
        if l_taged[l_i] == 'w' and line[l_i] in tag_f:
            l_taged[l_i] = 'f'
    tag_g = tag_list[1]
    for l_i in range(line_l):
        if l_taged[l_i] == 'w' and line[l_i] in tag_g:
            l_taged[l_i] = 'g'
    tag_i = tag_list[2]
    for l_i in range(line_l):
        if l_taged[l_i] == 'w' and line[l_i] in tag_i:
            l_taged[l_i] = 'i'
    tag_j = tag_list[3]
    for l_i in range(line_l):
        if l_taged[l_i] == 'w' and line[l_i] in tag_j:
            l_taged[l_i] = 'j'
    tag_k = tag_list[4]
    for l_i in range(line_l):
        if l_taged[l_i] == 'w' and line[l_i] in tag_k:
            l_taged[l_i] = 'k'
    if "零" in line:
        pos = re.search("零", line).start()
        if pos > 0 and l_taged[pos - 1] == 'g' and pos + 1 < len(line) and l_taged[pos +1] == 'f':



def find_arabic_num(sentence):
    pattern = re.compile("[-+]?(\d+(\.\d*)?)([eE][-+]?\d+)?([\/:](\d+(\.\d*)?)([eE][-+]?\d+)?)?%?")
    seg = re.search(pattern, sentence)
    seg_list = []
    while seg:
        seg_list.append((seg.start(), seg.end()))
        seg = re.search(pattern, sentence[seg.end():])
    return seg_list

if __name__ == "__main__":
    with open("resource/tokens", "r") as fo:
        tokens = fo.read().split(" ")
    with open("resource/CN", "r") as fo:
        f = fo.read().split(" ")
    with open("resource/Magnitude", "r") as fo:
        g = fo.read().split(" ")
    with open("resource/CFC", "r") as fo:
        i = fo.read().split(" ")
    with open("resource/CRP", "r") as fo:
        j = fo.read().split(" ")
    with open("resource/ONP", "r") as fo:
        k = fo.read().split(" ")
    tag_l = f + g + i + j + k
    with open("resource/baike/part-r-00000.txt", "r") as fo:
        for l in fo:
            if token_in_line(tokens, l):  # every quantity relationship takes the number as the center
                sen = ['w' for i in range(len(l))]
                # a tag list for the sentence and 'w' represents the word doesn't have tag
                arabic = find_arabic_num(l)
                for i in arabic:
                    for j in range(i[0], i[1]):
                        if sen[j] == 'w':
                            sen[j] = 'a'  # 'a' represent the word is arabic number
                comma = re.search(",", l)
                while comma:
                    if (comma.start() > 0 and sen[comma.start() - 1] == 'a') and (comma.start() < len(sen) and sen[comma.start() + 1] == 'a'):
                        sen[comma.start()] = 'a'
                    comma = re.search(",", l)
                tag_cn_num(tag_l, sen, l)



#
# tag_list = ["dn",
#             "PoFQ",
#             "PrCW",
#             "PrFQ",
#             "quantifier",
#             "SD",
#             "SP",
#             "SW",
#             "zj",
#             "ln"]
#
# fea_re = {
#     "dn": "a",
#     "PoFQ": "b",
#     "PrCW": "c",
#     "PrFQ": "d",
#     "number": "e",
#     "quantifier": "f",
#     "SD": "i",
#     "SP": "j",
#     "SW": "k",
#     "zj": "l",
#     "ln": "m",
#     "an": "n",
#     "0": "0"    # represent the string is not the string related to number
# }
#
# re_fea = {
#     "a": "dn",
#     "b": "PoFQ",
#     "c": "PrCW",
#     "d": "PrFQ",
#     "e": "number",
#     "f": "quantifier",
#     "i": "SD",
#     "j": "SP",
#     "k": "SW",
#     "l": "zj",
#     "m": "ln",
#     "n": "an",
#     "0": "text"
# }
#
#
# def find_cut_an(sen):
#     """
#     by given the sentence to find the number and tag an using the re
#     :param sen:the string of a sentence
#     :return: the list of string which is taged 0 or an and its tag
#     """
#     ans = re.findall(r"\d+\.\d+|\d+", sen)
#     if len(ans) == 0:
#         return [sen], ["0"]
#     sen_ph = []
#     sen_tag = []
#     last_end = 0
#     for i in range(len(ans)):
#         i_p = re.search(ans[i], sen)
#         i_start = i_p.start()
#         i_end = i_p.end()
#         if i == 0 and i_start != 0:
#             sen_ph.append(sen[:i_start])
#             sen_tag.append("0")  # 0 represent the none tag
#         elif i != 0 and last_end < i_start:
#             sen_ph.append(sen[last_end:i_start])
#             sen_tag.append("0")  # 0 represent the none tag
#         last_end = i_end
#         sen_ph.append(sen[i_start:i_end])
#         sen_tag.append(fea_re["an"])
#         if i == len(ans) - 1 and i_end != len(sen):
#             sen_ph.append(sen[i_end:])
#             sen_tag.append("0")  # 0 represent the none tag
#     return sen_ph, sen_tag
#
#
# def find_cut_by_list(sen, l, tag):
#     """
#     :param sen: the string of the part of a sentence
#     :param l: a list which contains the all words of the tag
#     :param tag: the tag will be tagged
#     :return: the list of the sentence and the tag
#     """
#     sen_ph = []
#     sen_tag = []
#     max_s = 0
#     for i in l:
#         if len(i) > max_s:
#             max_s = len(i)
#     i = 0
#     last_i = 0
#     while i < len(sen):
#         flag = True
#         for j in range(max_s)[::-1]:
#             if flag and i+j < len(sen) and sen[i:i+j+1] in l:
#                 flag = False
#                 if last_i < i:
#                     sen_ph.append(sen[last_i:i])
#                     sen_tag.append("0")
#                 sen_ph.append(sen[i:i+j+1])
#                 sen_tag.append(tag)
#                 last_i = i + j + 1
#                 i += (j + 1)
#         if flag:
#             i += 1
#     if last_i < len(sen):
#         sen_ph.append(sen[last_i:])
#         sen_tag.append("0")
#     return sen_ph, sen_tag
#
#
# def tag_sen(sen, tag_l):
#     """
#     tag the sentence
#     :param sen: the sentence to tag
#     :param tag_l: the list of tag
#     :return: the sbu-string of the sentence and its tag
#     """
#     sen_ph, sen_tag = find_cut_an(sen)
#     for t in tag_l:
#         file = codecs.open("resource/"+t, "r", "utf-8")
#         tab = file.readline().split()
#         temp_ph = []
#         temp_tag = []
#         for sen_s, sen_t in zip(sen_ph, sen_tag):
#             if sen_t == "0":
#                 tt_ph, tt_tag = find_cut_by_list(sen_s, tab, fea_re[t])
#                 temp_ph += tt_ph
#                 temp_tag += tt_tag
#             else:
#                 temp_ph.append(sen_s)
#                 temp_tag.append(sen_t)
#         sen_ph = temp_ph
#         sen_tag = temp_tag
#     return sen_ph, sen_tag
#
#
# def tag_num(sen_ph, fea_str):
#     """
#     tag the number
#     :param sen_ph:  the sub-string of the sentence
#     :param fea_str: the feature sting of the sentecn
#     :return: the sub-string and its tag
#     """
#     # tag the chinese number
#     ans = re.search(r"(ia[m])+l[im]+|(ia[m])+l(ia[m])+|(ia[m])+|i", fea_str)
#     # 小数/比分/整数/单个数字
#     while ans is not None:
#         temp_ph = []
#         i_start = ans.start()
#         i_end = ans.end()
#         temp_ph += sen_ph[:i_start]
#         temp_ph.append("".join(sen_ph[i_start:i_end]))
#         temp_ph += sen_ph[i_end:]
#         temp_fea = fea_str[:i_start] + "e" + fea_str[i_end:]
#         sen_ph = temp_ph
#         fea_str = temp_fea
#         ans = re.search(r"(ia[m])+l[im]+|(ia[m])+l(ia[m])+|(ia[m])+|i", fea_str)
#     # tag the number + chinese number  eg,1.5亿
#     ans = re.search(r"na", fea_str)
#     while ans is not None:
#         temp_ph = []
#         i_start = ans.start()
#         i_end = ans.end()
#         temp_ph += sen_ph[:i_start]
#         temp_ph.append("".join(sen_ph[i_start:i_end]))
#         temp_ph += sen_ph[i_end:]
#         temp_fea = fea_str[:i_start] + "e" + fea_str[i_end:]
#         sen_ph = temp_ph
#         fea_str = temp_fea
#         ans = re.search(r"na", fea_str)
#     # tag the special number 十
#     ans = re.search(r"a", fea_str)
#     while ans is not None:
#         temp_ph = []
#         i_start = ans.start()
#         i_end = ans.end()
#         if sen_ph[i_start] == u"十" and fea_str[i_start+1] == "f":
#             temp_ph += sen_ph[:i_start]
#             temp_ph += sen_ph[i_end:]
#             temp_fea = fea_str[:i_start] + "e" + fea_str[i_end:]
#             sen_ph = temp_ph
#             fea_str = temp_fea
#         else:
#             fea_str = fea_str[:i_start] + "0" + fea_str[i_end:]
#         ans = re.search(r"na", fea_str)
#     fea_str = fea_str.replace("n", "e")
#     return sen_ph, fea_str
#
#
# def clean_tag(sen_ph, fea_str):
#     """
#     save the right cnqp , delete the obvious error
#     delete the obvious error
#     :param sen: the sentence
#     :param sen_ph:  the sub-string of the sentence
#     :param fea_str: the feature sting of the sentecn
#     :return: the sub-string and its tag
#     """
#     temp_fea = ""
#     temp_ph = []
#     ans = re.search(r"[^0]*e[^0]*", fea_str)
#     while ans is not None:
#         i_start = ans.start()
#         i_end = ans.end()
#         if i_start != 0:
#             temp_ph.append("".join(sen_ph[:i_start]))
#             temp_fea += "0"
#         last_i = i_end
#         temp_ph += sen_ph[i_start:i_end]
#         temp_fea += fea_str[i_start:i_end]
#         sen_ph = sen_ph[i_end:]
#         fea_str = fea_str[i_end:]
#         ans = re.search(r"[^0]*e[^0]*", fea_str)
#     if len(sen_ph) != 0:
#         temp_ph.append("".join(sen_ph))
#         temp_fea += "0"
#     sen_ph = temp_ph
#     fea_str = temp_fea
#     return sen_ph, fea_str
#
#
# def tag(sen, tl):
#     sen_ph, sen_t = tag_sen(sen, tl)
#     sen_ph, sen_t = tag_num(sen_ph, "".join(sen_t))
#     sen_ph, sen_t = clean_tag(sen_ph, sen_t)
#     return sen_ph, sen_t
#
# a_ph, a_t = tag(s, tag_list)
#
# for ii in range(len(a_ph)):
#     print(a_ph[ii], re_fea[a_t[ii]])
