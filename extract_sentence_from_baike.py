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
        pos = re.search("零", line)
        end_pos = 0
        while pos:
            position = end_pos + pos.start()
            end_pos = end_pos + pos.end()
            if position > 0 and l_taged[position - 1] == 'g' and position + 1 < len(line) and l_taged[position +1] == 'f':
                l_taged[position] = 'h'
            else:
                l_taged[position] = 'f'
            pos = re.search("零", line[end_pos:])
    if "十" in line:
        pos = re.search("十", line)
        end_pos = 0
        while pos:
            position = end_pos + pos.start()
            end_pos = end_pos + pos.end()
            if position > 0 and l_taged[position - 1] == 'w' and position + 1 < len(line) and l_taged[position + 1] == 'w':
                l_taged[position] = 'f'
            elif position == 0 and position + 1 < len(line) and l_taged[position + 1] == 'w':
                l_taged[position] = 'f'
            elif position + 1 == len(line) and position - 1 > 0 and l_taged[position - 1] == 'w':
                l_taged[position] = 'f'
            else:
                l_taged[position] = 'g'
            pos = re.search("十", line[end_pos:])
    tag_pos = re.search("w[^w]w", ''.join(l_taged))
    end_pos = 0
    while tag_pos:
        tag_position = end_pos + tag_pos.start()
        end_pos += tag_pos.end()
        if l_taged[tag_position + 1] == 'i' or l_taged[tag_position + 1] == 'j' or l_taged[tag_position + 1] == 'k':
            l_taged[tag_position + 1] = 'w'
        tag_pos = re.search("w[^w]w", ''.join(l_taged[end_pos:]))
    return l_taged


def find_arabic_num(sentence):
    pattern = re.compile("[-+]?(\d+(\.\d*)?)([eE][-+]?\d+)?([\/:](\d+(\.\d*)?)([eE][-+]?\d+)?)?%?")
    seg = re.search(pattern, sentence)
    seg_list = []
    end_pos = 0
    while seg:
        seg_list.append((end_pos + seg.start(), end_pos + seg.end()))
        end_pos += seg.end()
        seg = re.search(pattern, sentence[end_pos:])
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
    tag_l = []
    tag_l.append(f)
    tag_l.append(g)
    tag_l.append(i)
    tag_l.append(j)
    tag_l.append(k)
    with open("resource/baike/part-r-00000.txt", "r") as fo:
        for l in fo:
            l = l[:-1]
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
                line_taged = tag_cn_num(tag_l, sen, l)
                n_pos = re.search("[^w]", ''.join(line_taged))
                if n_pos:
                    print(l, ''.join(line_taged))
