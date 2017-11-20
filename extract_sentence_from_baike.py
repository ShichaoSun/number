import re
import time


def token_in_line(token_list, line):
    for token in token_list:
        if token in line:
            return True
    return False


def tag_cn_num(tag_list, l_taged, line):
    flag = [0 for i in range(len(l_taged))]
    for i in range(len(l_taged)):
        if l_taged[i] != 'w':
            flag[i] = 1
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
    end_pos = 0
    s_taged = ''.join(l_taged)
    pos_r = re.search("a+g+", s_taged)
    while pos_r:
        pos_start = end_pos + pos_r.start()
        end_pos += pos_r.end()
        for i in range(pos_start, end_pos):
            flag[i] = 1
        pos_r = re.search("a+g+", s_taged[end_pos:])
    pattern = re.compile("((fg+h?)+f?|f)(jf+)?i((fg+h?)+f?|f)(jf+)?|k?((fg+h?)+f?|f)|g+i(fg+h?)*f?(jf+)?")
    sen_taged = ''.join(l_taged)
    tag_pos = re.search(pattern, sen_taged)
    end_pos = 0
    while tag_pos:
        for i in range(end_pos + tag_pos.start(), end_pos + tag_pos.end()):
            flag[i] = 1
        end_pos += tag_pos.end()
        tag_pos = re.search(pattern, sen_taged[end_pos:])
    for i in range(len(flag)):
        if not flag[i]:
            l_taged[i] = 'w'
    return l_taged


def find_arabic_num(sentence):
    pattern = re.compile("[-+]?(\d+(\.\d*)?)([eE][-+]?\d+)?([\/:](\d+(\.\d*)?)([eE][-+]?\d+)?)?%?‰?")
    seg = re.search(pattern, sentence)
    seg_list = []
    end_pos = 0
    while seg:
        seg_list.append((end_pos + seg.start(), end_pos + seg.end()))
        end_pos += seg.end()
        seg = re.search(pattern, sentence[end_pos:])
    sen = ['w' for i in range(len(sentence))]
    # a tag list for the sentence and 'w' represents the word doesn't have tag
    for i in seg_list:
        for j in range(i[0], i[1]):
            if sen[j] == 'w':
                sen[j] = 'a'  # 'a' represent the word is arabic number
    for i in range(len(sentence)):
        if sentence[i] == ',':
            sen[i] = 't'  # t represent the temp tag
    sen_tag = ''.join(sen)
    if 't' in sen_tag:
        res = re.search("a+(ta{3})+", sen_tag)
        end_pos = 0
        while res:
            res_start = end_pos + res.start()
            res_end = end_pos + res.end()
            end_pos = res_end
            for i in range(res_start, res_end):
                if sen[i] == 't':
                    sen[i] = 'c'
            res = re.search("a+(ta{3})+", sen_tag[end_pos:])
        for i in range(len(sen)):
            if sen[i] == 't':
                sen[i] = 'c'
    return sen


def clear_idioms(tag_list, l_taged, line):
    for word in tag_list:
        if word in line:
            pos = re.search(word, line)
            pos_end = 0
            while pos:
                for pos_i in range(pos_end + pos.start(), pos_end + pos.end()):
                    l_taged[pos_i] = 'w'
                pos_end += pos.end()
                pos = re.search(word, line[pos_end:])
    return l_taged


def tag_q(n_su, q_su, q_co, q, pre, l_taged, q_adv, line):
    def tag(tag_list, label, s_taged, sen):
        tag_list = sorted(tag_list, key=lambda x: len(x), reverse=True)
        for _tag in tag_list:
            if not _tag:
                break
            if _tag in sen:
                pos_end = 0
                pos = re.search(_tag, sen)
                while pos:
                    flag_con = True
                    for pos_i in range(pos_end + pos.start(), pos_end + pos.end()):
                        if l_taged[pos_i] != 'w' and l_taged[pos_i] != 'n':
                            flag_con = False
                            break
                    if flag_con:
                        for pos_i in range(pos_end + pos.start(), pos_end + pos.end()):
                            s_taged[pos_i] = label
                    pos_end += pos.end()
                    pos = re.search(_tag, sen[pos_end:])
        return s_taged
    l_taged = tag(n_su, "p", l_taged, line)
    l_taged = tag(q_su, "t", l_taged, line)
    l_taged = tag(q, "q", l_taged, line)
    l_taged = tag(q_co, "o", l_taged, line)
    l_taged = tag(pre, "s", l_taged, line)
    l_taged = tag(q_adv, "v", l_taged, line)
    taged = ''.join(l_taged)
    flag = [0 for i in range(len(line))]
    position = re.search("s*n+q+n+t*|s*n+v+q+t*|s*n+p*q*t*", taged)
    p_end = 0
    while position:
        for pp in range(p_end + position.start(), p_end + position.end()):
            flag[pp] = 1
        p_end += position.end()
        position = re.search("s*n+q+n+t*|s*n+v+q+t*|s*n+p*q*t*", taged[p_end:])
    for ii in range(len(line)):
        if flag[ii] == 0 and l_taged[ii] != 'n':
            l_taged[ii] = 'w'
    return l_taged


if __name__ == "__main__":
    with open("resource/tokens", "r") as fo:
        tokens = fo.read().split(" ")
    with open("resource/CN", "r") as fo:
        t_f = fo.read().split(" ")
    with open("resource/Magnitude", "r") as fo:
        t_g = fo.read().split(" ")
    with open("resource/CFC", "r") as fo:
        t_i = fo.read().split(" ")
    with open("resource/CRP", "r") as fo:
        t_j = fo.read().split(" ")
    with open("resource/ONP", "r") as fo:
        t_k = fo.read().split(" ")
    t_l = list()
    t_l.append(t_f)
    t_l.append(t_g)
    t_l.append(t_i)
    t_l.append(t_j)
    t_l.append(t_k)
    with open("resource/idioms") as fo:
        t_i = fo.read().split(" ")
    with open("resource/n_suffix") as fo:
        n_suffix = fo.read().split(" ")
    with open("resource/prefix") as fo:
        prefix = fo.read().split(" ")
    with open("resource/q_con") as fo:
        q_con = fo.read().split(" ")
    with open("resource/q_suffix") as fo:
        q_suffix = fo.read().split(" ")
    with open("resource/quantity") as fo:
        quantity = fo.read().split(" ")
    with open("resource/adv") as fo:
        adv = fo.read().split(" ")
    fi = open("sen", "w")
    with open("resource/baike/part-r-00000.txt", "r") as fo:
        for l in fo:
            l = l[:-1]
            if token_in_line(tokens, l):  # every quantity relationship takes the number as the center
                sen = find_arabic_num(l)
                line_taged = tag_cn_num(t_l, sen, l)
                line_taged = clear_idioms(t_i, line_taged, l)
                n_pos = re.search("[^w]", ''.join(line_taged))
                if n_pos:
                    sen_taged = [i for i in line_taged]
                    for i in range(len(l)):
                        if line_taged[i] != 'w':
                            sen_taged[i] = 'n'
                    sen_taged = tag_q(n_suffix, q_suffix, q_con, quantity, prefix, sen_taged, adv, l)
                    for i in range(len(l)):
                        if sen_taged[i] == 'n':
                            sen_taged[i] = line_taged[i]
                    print(l)
                    print(" ".join(sen_taged))
