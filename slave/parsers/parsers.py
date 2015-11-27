# encoding=utf-8

import jieba
import jieba.analyse
import jieba.posseg


class BaseParser(object):
    def __init__(self):

        # read stopwords
        stopwords_file = open("slave/parsers/stopwords")
        # stopwords_file = open("stopwords")
        stopwords = []
        for line in stopwords_file.readlines():
            stopwords.append(line.strip())
        self.stopwords = set(stopwords)

        jieba.enable_parallel(4)

    def segment(self, content):
        raise NotImplementedError


class JiebaParser(BaseParser):
    """
        segment content using jieba
    """

    def segment(self, content, cut_all=True):
        word_list = list(jieba.cut(content), cut_all)

        # use dict to count term frequency
        # TODO take position into account
        word_dict = {}
        for word in word_list:
            if word.encode("utf-8")  in self.stopwords or len(word) == 0:
                continue
            if word in word_dict:
                word_dict[word] += 1
            else:
                word_dict[word] = 1
        word_dict = sorted(word_dict.items(), key=lambda d: d[1], reverse=True)

        # change dict to list
        # format: [{"term":word, "tf":2},{...}]
        terms = []
        for word_tuple in word_dict:
            terms.append({'term': word_tuple[0], 'tf': word_tuple[1]})

        return terms

test = JiebaParser()
print '的' in test.stopwords

setence = "Sloriac的个人博客 当前网页 不支持 你正在使用的浏览器. 为了正常的访问, 请 升级你的浏览器. Sloriac的个人博客 所谓成就，就是在喜欢的领域达到一定的境界"
terms = test.segment(setence)
for term in terms:
    print term['term'], term['tf']