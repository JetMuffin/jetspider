# encoding=utf-8

import jieba
import jieba.analyse

class BaseParser(object):
    def __init__(self):
        pass

    def segment(self, content):
        raise NotImplementedError


class JiebaParser(BaseParser):
    """
        segment content using jieba
    """

    def segment(self, content, cut_all=True):
        word_list = list(jieba.cut(content, cut_all=True))

        terms = {}
        for word in word_list:
            if word in terms:
                terms[word] += 1
            else:
                terms[word] = 1

        # Todo filter stopwords
        return sorted(terms.items(), key=lambda d: d[1], reverse=True)

