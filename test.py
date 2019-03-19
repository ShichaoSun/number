from generate_re_dict import generate_re_from_grammar_file, tag_sentence
import collections

if __name__ == "__main__":
    d = generate_re_from_grammar_file("resource/grammar")
    s = "第一，我有两个苹果，大约4斤多，第2，有一大堆梨,5/6的人没有来上课，3.5亿人受伤,-3.5e10是什么"
    # s = "分辨率是1920*1080"
    res = tag_sentence(s, d)
    res_word = collections.OrderedDict()
    for k, v in res.items():
        temp_l = []
        for vv in v:
            temp_l.append(s[vv[0]:vv[1]])
        res_word[k] = temp_l
    for k in res.keys():
        print(k, res[k], res_word[k])
